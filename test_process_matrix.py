from process_matrix import process_matrix


def test_empty_matrix():                 # зовнішній цикл: 0 ітерацій
    assert process_matrix([]) == 0


def test_empty_row():                    # цикл по j: 0 ітерацій
    assert process_matrix([[]]) == 0


def test_non_positive_element():         # умова matrix[i][j] > 0 == False
    assert process_matrix([[0, -2]]) == 0


def test_inner_k_one_iteration():        # умова True, цикл по k: 1 ітерація
    assert process_matrix([[1]]) == 0


def test_many_iterations_everywhere():   # 2+ ітерацій на кожному рівні
    # [4] -> k: 0,1,2,3 -> 0+1+2+0 = 3; [-1] пропускається; [2] -> 0+1 = 1
    assert process_matrix([[4, -1], [2]]) == 4
