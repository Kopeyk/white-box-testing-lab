from auth import authenticate_user


# ---- Тести з методички ----
def test_missing_credentials():
    db = {}
    assert authenticate_user("", "pass", db) == "Missing credentials"
    assert authenticate_user("user", "", db) == "Missing credentials"


def test_user_not_found():
    db = {}
    assert authenticate_user("user", "pass", db) == "User not found"


def test_account_locked():
    db = {"user": {"password": "pass", "attempts": 3}}
    assert authenticate_user("user", "pass", db) == "Account locked"


def test_invalid_password():
    db = {"user": {"password": "pass", "attempts": 0}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 1


def test_success():
    db = {"user": {"password": "pass", "attempts": 1}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0


# ---- Додаткові тести для повного покриття (крок 9) ----
def test_both_credentials_missing():
    # Condition Combination: обидві умови першого if істинні одночасно
    assert authenticate_user("", "", {}) == "Missing credentials"


def test_attempts_key_absent():
    # Data flow: def attempts через get(..., 0), коли ключа "attempts" немає
    db = {"user": {"password": "pass"}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0


def test_attempts_boundary_and_lock():
    # Межа attempts >= 3: при 2 спробах вхід ще можливий, третя помилка блокує акаунт
    db = {"user": {"password": "pass", "attempts": 2}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 3
    assert authenticate_user("user", "pass", db) == "Account locked"
