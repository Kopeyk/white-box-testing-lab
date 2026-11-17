import itertools
from check_access import check_access
from validate_input import validate_input
from auth import authenticate_user

print("Task2: A=role=='user', B=is_active, C=is_admin")
for a, b, c in itertools.product([True, False], repeat=3):
    print(a, b, c, a and b, check_access("user" if a else "guest", b, c))

print("Task4: C1=not user, C2=len<8, C3=digit, C4=upper")
pw = {(False, False, False): "abcdefgh", (False, False, True): "Abcdefgh", (False, True, False): "abcdefg1", (False, True, True): "Abcdefg1",
      (True, False, False): "abc", (True, False, True): "Abc", (True, True, False): "abc1", (True, True, True): "Ab1"}
for c1, c2, c3, c4 in itertools.product([True, False], repeat=4):
    print(c1, c2, c3, c4, repr(pw[(c2, c3, c4)]), validate_input("" if c1 else "oleg", pw[(c2, c3, c4)]))

print("Task6 D1: A=not username, B=not password")
for a, b in itertools.product([True, False], repeat=2):
    print(a, b, a or b, authenticate_user("" if a else "user", "" if b else "pass", {}))
