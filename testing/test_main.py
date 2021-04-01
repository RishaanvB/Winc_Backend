from main import get_none, flatten_dict


def test_get_none():
    assert get_none() is None


# def test_flatten_dict():

#     assert flatten_dict({"a": 42, "b": 3.14}) == [42, 3.14]
#     assert flatten_dict({"a": {"inner_a": 42, "inner_b": 350}, "b": 3.14}) == [
#         {"inner_a": 42, "inner_b": 350},
#         3.14,
#     ]


def test_flatten_dict_nested():
    assert (
        flatten_dict(
            {
                "a": {
                    "inner_a": 42,
                    "inner_b": 350,
                    "c": {"inner_a": 42, "inner_b": 350},
                },
                "b": 3.14,
            }
        )
        == [42, 350, 42, 350, 3.14]
    )
    assert flatten_dict({"a": [{"inner_inner_a": 42}]}) == [42]
    assert flatten_dict({"a": [1, 2, {"b": 10}]}) == [1, 2, 10]
