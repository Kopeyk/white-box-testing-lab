# white-box-testing-lab

Лабораторна робота 9 «Техніки тест-дизайну "білої скриньки"» (дисципліна «Якість програмного забезпечення та тестування»).

- `process_data.py`, `check_access.py`, `process_matrix.py`, `validate_input.py`, `update_task_status.py` — функції із завдань 1–5, тести `test_*.py`;
- `auth.py`, `test_auth.py` — завдання 6;
- `cfg_tools.py` — побудова CFG (`python cfg_tools.py` створює `cfg/*.png`), цикломатична складність, шляхи виконання;
- `conditions.py` — таблиці комбінацій умов (`itertools.product`).

Запуск:

```
pip install -r requirements.txt
coverage run --branch -m pytest
coverage report -m
coverage html
```
