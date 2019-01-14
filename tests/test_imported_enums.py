import unittest


# These can't be imported until the test_imported_enums_proto module has been built.
CLOSE = None
MSG_ONE = None
ExposesInternalEnumConstantsMessage = None
UsesImportedEnumsMessage = None


class ImportedEnumsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global CLOSE, MSG_ONE, ExposesInternalEnumConstantsMessage, UsesImportedEnumsMessage
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
