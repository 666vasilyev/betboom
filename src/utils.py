import base64

# Исходная строка
def hash_decoder(original_string: str) -> str:
    # Преобразуем строку в байты
    encoded_bytes = original_string.encode('utf-8')

    # Кодируем байты в формат Base64
    return base64.b64encode(encoded_bytes).decode('utf-8')


def hash_coder(encoded_string: str) -> str:
    # Декодируем строку Base64
    decoded_bytes = base64.b64decode(encoded_string)

    # Преобразуем байты в строку
    return decoded_bytes.decode('utf-8')



# эти функции сгенерированы в ChatGPT, на мне никакой ответственности :)
def levenshtein_distance(str1, str2):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1

    # Инициализация матрицы расстояний
    matrix = [[0] * len_str2 for _ in range(len_str1)]

    # Заполнение матрицы базовыми значениями
    for i in range(len_str1):
        matrix[i][0] = i
    for j in range(len_str2):
        matrix[0][j] = j

    # Заполнение матрицы построчно
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  # удаление
                matrix[i][j - 1] + 1,  # вставка
                matrix[i - 1][j - 1] + cost  # замена
            )

    # Расстояние Левенштейна между строками
    return matrix[-1][-1]

def compare_strings(str1, str2, threshold=3):
    distance = levenshtein_distance(str1, str2)
    return distance <= threshold

def find_substring(main_string, substring, threshold=3):
    len_main = len(main_string)
    len_sub = len(substring)

    if len_sub > len_main:
        return False

    for i in range(len_main - len_sub + 1):
        window = main_string[i:i + len_sub]
        distance = levenshtein_distance(window, substring)
        if distance <= threshold:
            return True

    return False

print(find_substring('BetBoom Team', 'BetBoomTeam'))