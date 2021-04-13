import pdb


def get_none():
    return None


# def flatten(l1):
#     if len(l1) == 1:
#         if type(l1[0]) == list:
#             result = flatten(l1[0])
#         else:
#             result = l1
#     elif type(l1[0]) == list:
#         result = flatten(l1[0]) + flatten(l1[1:])
#     else:
#         result = (l1[0]) + flatten(l1[1:])
#         return result

    # recursive case


def flatten_dict(d, iter=None):
    if isinstance(d, dict):
        if iter is None:
            iter = []
        for k, v in sorted(d.items()):
            if not isinstance(v, dict) and not isinstance(v, list):
                iter.append(v)
            if v and not isinstance(v, int) and not isinstance(v, float):
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            flatten_dict(item, iter)
                flatten_dict(v, iter)
    return iter

# antwoord gegeven door docent Donatas Rasiukevicius
def flatten(node, flat_dict=None, prefix=None):
    flat_dict = flat_dict or {}
    if isinstance(node, dict):
        for k, v in node.items():
            if prefix:
                flat_dict = flatten(v, flat_dict, f"{prefix}__{k}")
            else:
                flat_dict = flatten(v, flat_dict, k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if prefix:
                flat_dict = flatten(v, flat_dict, f"{prefix}__{i}")
            else:
                flat_dict = flatten(v, flat_dict, str(i))
    else:
        flat_dict[prefix] = node
    return flat_dict


print(flatten_dict({"a": {"inner_a": 42, "inner_b": 350}, "b": 3.14}), "answer should [42, 350, 3.14]")
print(flatten_dict({"a": [[{"inner_inner_a": 42}]]}), "print flatten dict")


print("")

print(flatten({"a": {"inner_a": 42, "inner_b": 350}, "b": 3.14}), "<----- answer given|||     |||answer should--> [42, 350, 3.14]--")