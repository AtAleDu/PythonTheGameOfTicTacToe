import os
import tempfile
import random


# Функция сортировки вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >=0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Функция слияния двух отсортированных файлов
def merge_sorted_files(file1, file2, outfile):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(outfile, 'w') as of:
        arr1 = [int(line.strip()) for line in f1]
        arr2 = [int(line.strip()) for line in f2]
        arr = merge(arr1, arr2)
        for item in arr:
            of.write(str(item) + '\n')

# Функция слияния двух отсортированных массивов
def merge(arr1, arr2):
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

# Функция внешней сортировки
def external_sort(input_file, M):
    temp_files = []
    with open(input_file, 'r') as f:
        while True:
            lines = f.readlines(M)
            if not lines:
                break
            lines = [int(line.strip()) for line in lines]
            lines = insertion_sort(lines)
            temp_fd, temp_filename = tempfile.mkstemp()
            os.close(temp_fd)
            with open(temp_filename, 'w') as temp_file:
                for line in lines:
                    temp_file.write(f"{line}\n")
            temp_files.append(temp_filename)

    while len(temp_files) > 1:
        temp_file1 = temp_files.pop(0)
        temp_file2 = temp_files.pop(0)
        _, new_temp_file = tempfile.mkstemp()
        merge_sorted_files(temp_file1, temp_file2, new_temp_file)
        temp_files.append(new_temp_file)
        os.remove(temp_file1)
        os.remove(temp_file2)

    os.rename(temp_files[0], 'sorted_data.txt')

# Пример использования
M = 50  # Количество строк, которое можно считать в память

# Создаем файл data.txt для тестирования
with open('data.txt', 'w') as f:
    for _ in range(100):
        f.write(f"{random.randint(1, 1000)}\n")

# Вызываем функцию внешней сортировки
external_sort('data.txt', M)
