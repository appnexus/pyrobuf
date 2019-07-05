import unittest


# These can't be imported until the test_imported_enums_proto module has been built.
Status = None
MessageID = None
ExposesInternalEnumConstantsMessageinternal_enum = None
UsesImportedEnumsMessage = None


class ImportedEnumsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Status, MessageID, ExposesInternalEnumConstantsMessageinternal_enum, UsesImportedEnumsMessage
        from test_multi_messages_toplevel_enums_proto import Status, MessageID
        from test_imported_enums_proto import UsesImportedEnumsMessage, ExposesInternalEnumConstantsMessageinternal_enum

    def test_message_id_has_default_of_msg_one(self):
        message = UsesImportedEnumsMessage()
        self.assertEqual(message.message_id, MessageID.MSG_ONE.value)

    def test_status_has_default_of_close(self):
        message = UsesImportedEnumsMessage()
        self.assertEqual(message.status, Status.CLOSE.value)

    def test_internal_enum_constants_exposed(self):
        self.assertEqual(ExposesInternalEnumConstantsMessageinternal_enum.INTERNAL.value, 0)
        self.assertEqual(ExposesInternalEnumConstantsMessageinternal_enum.EXTERNAL.value, 1)
