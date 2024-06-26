import importlib
import logging

from mayan.apps.storage import storages
from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import DefinedStorage
from ..literals import STORAGE_NAME_SHARED_UPLOADED_FILE
from ..settings import setting_shared_storage_arguments


class CommonStorageSettingsTestCase(BaseTestCase):
    def tearDown(self):
        super().tearDown()
        importlib.reload(storages)

    def test_setting_shared_storage_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_shared_storage_arguments.global_name
            ), value='invalid_value'
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storages)
            defined_storage = DefinedStorage.get(
                name=STORAGE_NAME_SHARED_UPLOADED_FILE
            )
            defined_storage.get_storage_instance()

        self.assertTrue(
            'Unable to initialize' in str(assertion.exception)
        )
        self.assertTrue(
            'shared uploaded' in str(assertion.exception)
        )
