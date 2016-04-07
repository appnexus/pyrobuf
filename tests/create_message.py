import sys


if sys.version_info.major == 2:
    import messages.test_message_pb2 as google_test


def create_an_test():
    # print LIB
    import test_message_proto as an_test
    test = an_test.Test()
    test.timestamp = 539395200
    test.field = 10689
    test.string_field = "go goats!"

    for i in range(5):
        test.list_fieldx.append(i * 100)

    test.substruct.field1 = 12345
    test.substruct.field2 = "hello"
    test.substruct.field3.field1 = 1419.67
    test.substruct.field3.ss2_field2 = "goodbye"
    test.substruct.list.append(354.94)

    obj = test.substruct.list_object.add()
    obj.field1 = 3.14159
    obj.ss2_field2 = "pi"

    test.substruct.list_string.append("something")

    test.test_ref.timestamp = 539395200
    test.test_ref.field1 = 1111
    test.test_ref.field2 = 1.2345
    test.test_ref.field3 = "foo"

    obj = test.list_ref.add()
    obj.timestamp = 539395200
    obj.field1 = 1111
    obj.field2 = 1.2345
    obj.field3 = "foo"

    test.another_substruct.string_field = "what's up?"
    test.another_substruct.fixed_string_field = "nothing much"
    test.another_substruct.int_field = 24
    test.another_substruct.another_int_field = 87

    test.another_substruct.substruct_ref.timestamp = 539395200
    test.another_substruct.substruct_ref.field1 = 1111
    test.another_substruct.substruct_ref.field2 = 1.2345
    test.another_substruct.substruct_ref.field3 = "foo"

    test.req_field = -80914
    test.negative_32 = -1

    return test


if sys.version_info.major == 2:
    def create_google_test():
        test = google_test.Test()
        test.timestamp = 539395200
        test.field = 10689
        test.string_field = "go goats!"

        for i in range(5):
            test.list_fieldx.append(i * 100)

        test.substruct.field1 = 12345
        test.substruct.field2 = "hello"
        test.substruct.field3.field1 = 1419.67
        test.substruct.field3.ss2_field2 = "goodbye"
        test.substruct.list.append(354.94)

        obj = test.substruct.list_object.add()
        obj.field1 = 3.14159
        obj.ss2_field2 = "pi"

        test.substruct.list_string.append("something")

        test.test_ref.timestamp = 539395200
        test.test_ref.field1 = 1111
        test.test_ref.field2 = 1.2345
        test.test_ref.field3 = "foo"

        obj = test.list_ref.add()
        obj.timestamp = 539395200
        obj.field1 = 1111
        obj.field2 = 1.2345
        obj.field3 = "foo"

        test.another_substruct.string_field = "what's up?"
        test.another_substruct.fixed_string_field = "nothing much"
        test.another_substruct.int_field = 24
        test.another_substruct.another_int_field = 87

        test.another_substruct.substruct_ref.timestamp = 539395200
        test.another_substruct.substruct_ref.field1 = 1111
        test.another_substruct.substruct_ref.field2 = 1.2345
        test.another_substruct.substruct_ref.field3 = "foo"

        test.req_field = -80914
        test.negative_32 = -1

        return test

    def create_buffer():
        test = create_google_test()
        return test.SerializeToString()
