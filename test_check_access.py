import itertools
import pytest
from check_access import check_access

ROLE = {True: "user", False: "guest"}


def expected(a, b, c):
    return (a and b) or c


# Condition Combination Coverage: усі 2^3 = 8 комбінацій
@pytest.mark.parametrize("a,b,c", list(itertools.product([True, False], repeat=3)))
def test_condition_combination(a, b, c):
    assert check_access(ROLE[a], b, c) == expected(a, b, c)


# MC/DC: мінімальний набір N+1 = 4 тести
@pytest.mark.parametrize("role,is_active,is_admin,result", [
    ("user", True, False, True),    # базовий: A=T, B=T, C=F
    ("guest", True, False, False),  # змінюється лише A -> результат змінюється
    ("user", False, False, False),  # змінюється лише B -> результат змінюється
    ("user", False, True, True),    # у парі з попереднім змінюється лише C
])
def test_mcdc(role, is_active, is_admin, result):
    assert check_access(role, is_active, is_admin) is result
