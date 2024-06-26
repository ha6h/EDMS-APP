from mayan.apps.common.tests.mixins import ManagementCommandTestMixin
from mayan.apps.documents.storages import storage_document_files
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.mime_types.tests.mixins import MIMETypeBackendMixin

from ..literals import COMMAND_NAME_STORAGE_PROCESS

from .mixins import StorageProcessorTestMixin


class StorageProcessManagementCommandTestCase(
    MIMETypeBackendMixin, ManagementCommandTestMixin,
    StorageProcessorTestMixin, GenericDocumentTestCase
):
    _test_management_command_name = COMMAND_NAME_STORAGE_PROCESS

    def _get_test_management_command_keyword_arguments(self, reverse=None):
        keyword_arguments = {
            'app_label': 'documents',
            'defined_storage_name': storage_document_files.name,
            'log_file': str(self.path_test_file),
            'model_name': 'DocumentFile',
            'reverse': reverse
        }
        return keyword_arguments

    def _upload_and_call(self):
        self.defined_storage.dotted_path = 'django.core.files.storage.FileSystemStorage'
        self.defined_storage.kwargs = {
            'location': self.document_storage_kwargs['location']
        }

        self._upload_test_document()

        self.defined_storage.dotted_path = 'mayan.apps.storage.backends.compressedstorage.ZipCompressedPassthroughStorage'
        self.defined_storage.kwargs = {
            'next_storage_backend': 'django.core.files.storage.FileSystemStorage',
            'next_storage_backend_arguments': {
                'location': self.document_storage_kwargs['location']
            }
        }

        self._call_test_management_command(
            **self._get_test_management_command_keyword_arguments()
        )

    def test_storage_processor_command_forwards(self):
        self._upload_and_call()

        with open(file=self._test_document.file_latest.file.path, mode='rb') as file_object:
            self.assertEqual(
                self.mime_type_backend.get_mime_type(
                    file_object=file_object
                ), ('application/zip', 'binary')
            )

        self.assertEqual(
            self._test_document.file_latest.checksum,
            self._test_document.file_latest.checksum_update(save=False)
        )

    def test_processor_forwards_and_reverse(self):
        self._upload_and_call()

        self._call_test_management_command(
            **self._get_test_management_command_keyword_arguments(
                reverse=True
            )
        )

        self.defined_storage.dotted_path = 'django.core.files.storage.FileSystemStorage'
        self.defined_storage.kwargs = {
            'location': self.document_storage_kwargs['location']
        }

        with open(file=self._test_document.file_latest.file.path, mode='rb') as file_object:
            self.assertNotEqual(
                self.mime_type_backend.get_mime_type(
                    file_object=file_object
                ), ('application/zip', 'binary')
            )

        self.assertEqual(
            self._test_document.file_latest.checksum,
            self._test_document.file_latest.checksum_update(save=False)
        )
