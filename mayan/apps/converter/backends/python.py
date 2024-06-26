import io
import logging
import shutil
import struct

from PIL import Image
import pypdf
import sh

from django.utils.translation import gettext_lazy as _

from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import ConverterBase
from ..exceptions import PageCountError
from ..literals import (
    DEFAULT_PDFTOPPM_DPI, DEFAULT_PDFTOPPM_FORMAT, DEFAULT_PDFTOPPM_PATH,
    DEFAULT_PDFINFO_PATH, DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS
)
from ..settings import setting_graphics_backend_arguments

logger = logging.getLogger(name=__name__)
pdftoppm_path = setting_graphics_backend_arguments.value.get(
    'pdftoppm_path', DEFAULT_PDFTOPPM_PATH
)

try:
    command_pdftoppm = sh.Command(path=pdftoppm_path)
except sh.CommandNotFound:
    command_pdftoppm = None
else:
    pdftoppm_format = '-{}'.format(
        setting_graphics_backend_arguments.value.get(
            'pdftoppm_format', DEFAULT_PDFTOPPM_FORMAT
        )
    )

    pdftoppm_dpi = format(
        setting_graphics_backend_arguments.value.get(
            'pdftoppm_dpi', DEFAULT_PDFTOPPM_DPI
        )
    )

    command_pdftoppm = command_pdftoppm.bake(
        pdftoppm_format, '-r', pdftoppm_dpi
    )

pdfinfo_path = setting_graphics_backend_arguments.value.get(
    'pdfinfo_path', DEFAULT_PDFINFO_PATH
)

try:
    command_pdfinfo = sh.Command(path=pdfinfo_path)
except sh.CommandNotFound:
    command_pdfinfo = None


pillow_maximum_image_pixels = setting_graphics_backend_arguments.value.get(
    'pillow_maximum_image_pixels', DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS
)
Image.MAX_IMAGE_PIXELS = pillow_maximum_image_pixels


class Python(ConverterBase):
    def convert(self, *args, **kwargs):
        super().convert(*args, **kwargs)

        if self.mime_type == 'application/pdf' and command_pdftoppm:
            with NamedTemporaryFile() as new_file_object:
                self.file_object.seek(0)
                shutil.copyfileobj(
                    fsrc=self.file_object, fdst=new_file_object
                )
                self.file_object.seek(0)
                new_file_object.seek(0)

                image_buffer = io.BytesIO()
                command_pdftoppm(
                    new_file_object.name, f=self.page_number + 1,
                    l=self.page_number + 1, _out=image_buffer
                )
                image_buffer.seek(0)
                return Image.open(fp=image_buffer)

    def get_page_count(self):
        super().get_page_count()

        if self.mime_type == 'application/pdf' or self.soffice_file:
            if self.soffice_file:
                file_object = self.soffice_file
            else:
                file_object = self.file_object

            return self.get_pypdf_page_count(file_object=file_object)
        else:
            return self.get_pillow_page_count()

    def get_pillow_page_count(self):
        page_count = 1

        try:
            image = Image.open(fp=self.file_object)
        except IOError as exception:
            error_message = _(
                'Exception determining page count using Pillow; %s'
            ) % exception
            logger.error(error_message)
            raise PageCountError(error_message)
        finally:
            self.file_object.seek(0)

        # Get total page count by attempting to seek to an increasing
        # page count number until an EOFError or struct.error exception
        # are raised.
        while True:
            try:
                image.seek(
                    image.tell() + 1
                )
            except EOFError:
                """End of sequence"""
                break
            except struct.error:
                """
                struct.error was raise for a TIFF file converted to JPEG
                GitLab issue #767 "Upload Error: unpack_from requires a
                buffer of at least 2 bytes"
                """
                logger.debug(
                    msg='image page count detection raised struct.error'
                )
                break
            else:
                try:
                    # Even if the image reports multiple frames,
                    # test it to make sure it is valid and supported
                    # before counting it as a valid page.
                    image.getim()
                except OSError as exception:
                    logger.error(
                        'Multi image element not supported; %s',
                        exception
                    )
                    break
                else:
                    page_count += 1

        self.file_object.seek(0)
        return page_count

    def get_pdfinfo_page_count(self, file_object):
        process = command_pdfinfo('-', _in=file_object)

        for line in str(process.stdout).split('\n'):
            if line.startswith('Pages:'):
                line = line.replace('Pages:', '')
                page_count = int(line)
                break

        file_object.seek(0)
        logger.debug('Document contains %d pages', page_count)
        return page_count

    def get_pypdf_page_count(self, file_object):
        try:
            # Try PyPDF to determine the page count.
            pdf_reader = pypdf.PdfReader(
                stream=file_object, strict=False
            )
            page_count = len(pdf_reader.pages)
        except Exception as exception:
            if str(exception) == 'File has not been decrypted':
                # File is encrypted, try to decrypt using a blank
                # password.
                file_object.seek(0)
                pdf_reader = pypdf.PdfReader(
                    stream=file_object, strict=False
                )
                try:
                    pdf_reader.decrypt(password=b'')
                    page_count = len(pdf_reader.pages)
                except Exception as exception:
                    file_object.seek(0)
                    if str(exception) == 'only algorithm code 1 and 2 are supported':
                        # PDF uses an unsupported encryption.
                        # Try poppler-util's pdfinfo.
                        page_count = self.get_pdfinfo_page_count(
                            file_object=file_object
                        )
                        return page_count
                    else:
                        error_message = _(
                            'Exception determining PDF page count; %s'
                        ) % exception
                        logger.error(error_message, exc_info=True)
                        raise PageCountError(error_message)
            elif str(exception) == 'EOF marker not found':
                # PyPDF2 issue: https://github.com/mstamy2/PyPDF2/issues/177
                # Try poppler-util's pdfinfo.
                logger.debug(
                    msg='PyPDF2 GitHub issue #177 : EOF marker not found'
                )
                file_object.seek(0)
                page_count = self.get_pdfinfo_page_count(
                    file_object=file_object
                )
                return page_count
            else:
                error_message = _(
                    'Exception determining PDF page count; %s'
                ) % exception
                logger.error(error_message, exc_info=True)
                raise PageCountError(error_message)
        else:
            logger.debug('Document contains %d pages', page_count)
            return page_count
        finally:
            file_object.seek(0)
