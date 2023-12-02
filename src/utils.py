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
