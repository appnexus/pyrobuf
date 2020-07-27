import unittest


TestIsInitialized = None
SubMessage = None
TestWithRequiredSubMessage = None


class MergeFromTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global TestIsInitialized, SubMessage, TestWithRequiredSubMessage
        from test_is_initialized_proto import TestIsInitialized, SubMessage, TestWithRequiredSubMessage

    def test_new_message_is_not_initialized(self):
        message = TestIsInitialized()
        self.assertFalse(message.IsInitialized())

    def test_message_with_all_required_fields_set_is_initialized(self):
        message = TestIsInitialized()
        message.req_field = 1
        self.assertTrue(message.IsInitialized())

    def test_new_message_with_required_submessage_is_not_initialized(self):
        message = TestWithRequiredSubMessage()
        self.assertFalse(message.IsInitialized())

    def test_message_with_initialized_required_submessage_is_initialized(self):
        message = TestWithRequiredSubMessage()
        message.req_sub.req_field = 1
        self.assertTrue(message.IsInitialized())

    def test_message_with_uninitialized_submessage_is_not_initialized(self):
        message = TestIsInitialized()
        message.req_field = 1
        message.sub_message.opt_field = 2
        self.assertFalse(message.IsInitialized())

    def test_message_with_initialized_submessage_is_initialized(self):
        message = TestIsInitialized()
        message.req_field = 1
        message.sub_message.req_field = 2
        self.assertTrue(message.IsInitialized())

    def test_message_with_uninitialized_repeated_submessage_is_not_initialized(self):
        message = TestIsInitialized()
        message.req_field = 1
        message.list_sub.add().opt_field = 2
        self.assertFalse(message.IsInitialized())

    def test_message_with_initialized_repeated_submessage_is_initialized(self):
        message = TestIsInitialized()
        message.req_field = 1
        message.list_sub.add().req_field = 2
        self.assertTrue(message.IsInitialized())
