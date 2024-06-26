import platform

from django.utils.translation import gettext_lazy as _

if platform.system() in ('FreeBSD', 'Darwin'):
    DEFAULT_GPG_PATH = '/usr/local/bin/gpg1'
elif platform.system() == 'OpenBSD':
    DEFAULT_GPG_PATH = '/usr/local/bin/gpg'
else:
    DEFAULT_GPG_PATH = '/usr/bin/gpg1'

DEFAULT_SIGNATURES_BACKEND = 'mayan.apps.django_gpg.backends.python_gnupg.PythonGNUPGBackend'
DEFAULT_DEFAULT_GPG_PATH = {
    'gpg_path': DEFAULT_GPG_PATH,
}
DEFAULT_SIGNATURES_KEYSERVER = 'pool.sks-keyservers.net'

ERROR_MSG_BAD_PASSPHRASE = 'BAD_PASSPHRASE'
ERROR_MSG_GOOD_PASSPHRASE = 'GOOD_PASSPHRASE'
ERROR_MSG_MISSING_PASSPHRASE = 'MISSING_PASSPHRASE'

KEY_TYPES = {
    'pub': _(message='Public'),
    'sec': _(message='Secret')
}

KEY_TYPE_PUBLIC = 'pub'
KEY_TYPE_SECRET = 'sec'

KEY_TYPE_CHOICES = (
    (KEY_TYPE_PUBLIC, _(message='Public')),
    (KEY_TYPE_SECRET, _(message='Secret'))
)

KEY_CLASS_RSA = 'RSA'
KEY_CLASS_DSA = 'DSA'
KEY_CLASS_ELG = 'ELG-E'

KEY_PRIMARY_CLASSES = (
    (
        (KEY_CLASS_RSA), _(message='RSA')
    ),
    (
        (KEY_CLASS_DSA), _(message='DSA')
    )
)

KEY_SECONDARY_CLASSES = (
    (
        (KEY_CLASS_RSA), _(message='RSA')
    ),
    (
        (KEY_CLASS_ELG), _(message='Elgamal')
    )
)

KEYSERVER_DEFAULT_PORT = 11371

OUTPUT_MESSAGE_CONTAINS_PRIVATE_KEY = 'Contains private key'

SIGNATURE_STATE_BAD = 'signature bad'
SIGNATURE_STATE_NONE = None
SIGNATURE_STATE_ERROR = 'signature error'
SIGNATURE_STATE_NO_PUBLIC_KEY = 'no public key'
SIGNATURE_STATE_GOOD = 'signature good'
SIGNATURE_STATE_VALID = 'signature valid'

SIGNATURE_STATES = {
    SIGNATURE_STATE_BAD: {
        'text': _(message='Bad signature.')
    },
    SIGNATURE_STATE_NONE: {
        'text': _(message='Document not signed or invalid signature.')
    },
    SIGNATURE_STATE_ERROR: {
        'text': _(message='Signature error.')
    },
    SIGNATURE_STATE_NO_PUBLIC_KEY: {
        'text': _(
            'Document is signed but no public key is available for '
            'verification.'
        )
    },
    SIGNATURE_STATE_GOOD: {
        'text': _(message='Document is signed, and signature is good.')
    },
    SIGNATURE_STATE_VALID: {
        'text': _(message='Document is signed with a valid signature.')
    }
}
