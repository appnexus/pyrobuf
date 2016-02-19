import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, 'build')


# These can't be imported until the test_imported_enums_proto module has been built.
CLOSE = None
MSG_ONE = None
ExposesInternalEnumConstantsMessage = None
UsesImportedEnumsMessage = None


class ImportedEnumsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib = os.path.join(BUILD, [name for name in os.listdir(BUILD)
                                   if name.startswith('lib')].pop())
        if lib not in sys.path:
            sys.path.insert(0, lib)

        # At this point the test_imported_enums_proto will have been built and can be imported
        global CLOSE, MSG_ONE, UsesImportedEnumsMessage, ExposesInternalEnumConstantsMessage

        from test_multi_messages_toplevel_enums_proto import MSG_ONE, CLOSE
        from test_imported_enums_proto import UsesImportedEnumsMessage, ExposesInternalEnumConstantsMessage

    def test_message_id_has_default_of_msg_one(self):
        message = UsesImportedEnumsMessage()
        self.assertEqual(message.message_id, MSG_ONE)

    def test_status_has_default_of_close(self):
        message = UsesImportedEnumsMessage()
        self.assertEqual(message.status, CLOSE)

    def test_internal_enum_constants_exposed(self):
        self.assertEqual(ExposesInternalEnumConstantsMessage.INTERNAL, 0)
        self.assertEqual(ExposesInternalEnumConstantsMessage.EXTERNAL, 1)
