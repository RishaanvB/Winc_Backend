import pdb


def get_none():
    return None


def flatten(l1):
    if len(l1) == 1:
        if type(l1[0]) == list:
            result = flatten(l1[0])
        else:
            result = l1
    elif type(l1[0]) == list:
        result = flatten(l1[0]) + flatten(l1[1:])
    else:
        result = (l1[0]) + flatten(l1[1:])
        return result

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



# print(flatten_dict({"a": {"inner_a": 42, "inner_b": 350}, "b": 3.14}), "answer should [42, 350, 3.14]")
print(flatten_dict({"a": [{"inner_inner_a": 42}]}), "print flatten dict")
