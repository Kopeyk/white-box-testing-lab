import pytest
from validate_input import validate_input


# MC/DC: 4 умови -> 5 тестів
@pytest.mark.parametrize("user,password,result", [
    ("", "Abcdefg1", "Missing user"),      # C1 = T
    ("oleg", "Abc1", "Weak password"),     # C1 = F, C2 = T
    ("oleg", "Abcdefg1", "Valid"),         # C2 = F, C3 = T, C4 = T
    ("oleg", "Abcdefgh", "Invalid"),       # C3 = F (змінено лише C3)
    ("oleg", "abcdefg1", "Invalid"),       # C4 = F (змінено лише C4)
])
def test_mcdc(user, password, result):
    assert validate_input(user, password) == result


# Межа довжини пароля для умови len(password) < 8
def test_password_length_boundary():
    assert validate_input("oleg", "Abcdef1") == "Weak password"   # 7 символів
    assert validate_input("oleg", "Abcdefg1") == "Valid"          # 8 символів
