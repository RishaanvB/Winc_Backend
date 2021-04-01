def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5


import ctypes, os
try:
 is_admin = os.getuid() == 0
except AttributeError:
 is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

print(is_admin) 