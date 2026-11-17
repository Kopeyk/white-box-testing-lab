import itertools
import pytest
from update_task_status import update_task_status

VALID = {
    "open": ["in_progress", "closed"],
    "in_progress": ["closed", "on_hold"],
    "on_hold": ["in_progress"],
    "closed": [],
}
STATUSES = list(VALID)
ROLES = ["admin", "manager", "user"]


def expected(old, new, role):
    if old == new:
        return "No change"
    if new not in VALID.get(old, []):
        return "Invalid transition"
    if role not in ["admin", "manager"] and new == "closed":
        return "Permission denied"
    return "Updated"


# Усі можливі переходи станів для всіх ролей: 4 x 4 x 3 = 48 тестів
@pytest.mark.parametrize("old,new,role", list(itertools.product(STATUSES, STATUSES, ROLES)))
def test_all_transitions(old, new, role):
    task = {"status": old}
    result = update_task_status(task, new, role)
    assert result == expected(old, new, role)
    assert task["status"] == (new if result == "Updated" else old)


def test_unknown_current_status():       # гілка .get(..., []) для невідомого стану
    assert update_task_status({"status": "archived"}, "open", "admin") == "Invalid transition"


# Мінімальний набір: кожна умова впливає на результат незалежно (MC/DC)
@pytest.mark.parametrize("old,new,role,result", [
    ("open", "open", "admin", "No change"),                 # D1 = T
    ("closed", "open", "admin", "Invalid transition"),      # D1 = F, D2 = T
    ("open", "closed", "user", "Permission denied"),        # A = T, B = T
    ("open", "closed", "manager", "Updated"),               # A = F, B = T (змінено лише A)
    ("open", "in_progress", "user", "Updated"),             # A = T, B = F (змінено лише B)
])
def test_mcdc_minimal(old, new, role, result):
    assert update_task_status({"status": old}, new, role) == result
