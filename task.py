import random
import copy


def generate_matrix(m, n, min_value, max_value):
    """
    Генерує матрицю розмірності m x n цілих випадкових чисел
    у діапазоні [min_value, max_value] (включно).
    """
    return [[random.randint(min_value, max_value) for _ in range(n)] for _ in range(m)]


def print_matrix(matrix):
    if not matrix:
        print("(порожня матриця)")
        return

    rows = len(matrix)
    cols = len(matrix[0])

    header = "\t" + "\t".join(f"стовпець {j + 1}" for j in range(cols))
    print(header)
    for i in range(rows):
        row_str = "\t".join(str(x) for x in matrix[i])
        print(f"рядок {i + 1}\t{row_str}")


def subtract_row_average(matrix):
    result = []
    for row in matrix:
        average = sum(row) / len(row) if row else 0
        result.append([x - average for x in row])
    return result


def cyclic_shift(matrix, k):
    if not matrix:
        return matrix

    m = len(matrix)
    n = len(matrix[0])
    k_col = k % n if n else 0
    k_row = k % m if m else 0

    shifted_right = [row[-k_col:] + row[:-k_col] if k_col else row[:] for row in matrix]

    result = [shifted_right[(i + k_row) % m] for i in range(m)]
    return result


def remove_rows_cols_with_max(matrix):
    if not matrix:
        return matrix

    max_value = max(max(row) for row in matrix)

    rows_to_remove = {i for i, row in enumerate(matrix) if max_value in row}
    cols_to_remove = {
        j for j in range(len(matrix[0]))
        if any(matrix[i][j] == max_value for i in range(len(matrix)))
    }

    result = [
        [matrix[i][j] for j in range(len(matrix[0])) if j not in cols_to_remove]
        for i in range(len(matrix)) if i not in rows_to_remove
    ]
    return result, max_value


def rotate_90_clockwise_in_place(matrix):
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("Метод розрахований лише на квадратну матрицю (m == n)")

    for layer in range(n // 2):
        first = layer
        last = n - 1 - layer
        for i in range(first, last):
            offset = i - first

            top = matrix[first][i]

            matrix[first][i] = matrix[last - offset][first]

            matrix[last - offset][first] = matrix[last][last - offset]

            matrix[last][last - offset] = matrix[i][last]

            matrix[i][last] = top

    return matrix


def main():
    matrix = generate_matrix(4, 4, 0, 10)
    print("Вихідна матриця:")
    print_matrix(matrix)
    print()

    matrix_centered = subtract_row_average(matrix)
    print("Завдання 1: матриця після віднімання середнього кожного рядка:")
    for row in matrix_centered:
        print(["%.2f" % x for x in row])
    print()

    k = 1
    shifted = cyclic_shift(matrix, k)
    print(f"Завдання 2: циклічний зсув на k={k} вправо та догори:")
    print_matrix(shifted)
    print()

    reduced, max_value = remove_rows_cols_with_max(matrix)
    print(f"Завдання 3: максимальний елемент = {max_value}")
    print("Матриця після видалення рядків і стовпців з максимумом:")
    print_matrix(reduced)
    print()

    square_matrix = generate_matrix(4, 4, 0, 10)
    print("Завдання 4: матриця до обертання:")
    print_matrix(square_matrix)
    rotate_90_clockwise_in_place(square_matrix)
    print("Завдання 4: матриця після обертання на 90° за годинниковою стрілкою:")
    print_matrix(square_matrix)


if __name__ == "__main__":
    main()