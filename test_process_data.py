from process_data import process_data


# Statement + branch + condition coverage: один тест проходить усі вузли і ребра CFG
def test_all_statements_and_branches():
    # -1 -> continue (data[i] < 0 == True); 3 -> j = 0 (парне), 1 (непарне), 2 (парне)
    assert process_data([-1, 3]) == 2


# Покриття циклів (0, 1, 2+ ітерацій зовнішнього і внутрішнього циклу)
def test_outer_loop_zero_iterations():
    assert process_data([]) == 0


def test_inner_loop_zero_iterations():
    assert process_data([0]) == 0


def test_inner_loop_one_iteration():
    assert process_data([1]) == 0


def test_inner_loop_many_iterations():
    assert process_data([5]) == 0 + 2 + 4


def test_outer_loop_many_iterations():
    assert process_data([2, -1, 4]) == 0 + (0 + 2)


# Data flow: шлях def(total=0) -> use(return) без переозначення total
def test_du_total_def_to_return():
    assert process_data([-1]) == 0
