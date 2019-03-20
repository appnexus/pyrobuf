def test_has_field():
    from test_many_fields_proto import TestManyFields
    test = TestManyFields()

    # Assert HasField false on clean message
    for field in test.Fields():
        assert not test.HasField(field)

    # Set fields
    for idx, field in enumerate(test.Fields()):
        setattr(test, field, idx)

    # Assert HasField true
    for field in test.Fields():
        assert test.HasField(field)

    # Reset and assert HasField false
    test.reset()

    for field in test.Fields():
        assert not test.HasField(field)
