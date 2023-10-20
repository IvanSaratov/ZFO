import argparse
import sys
import os
import unittest

def xor_cipher(text, key):
    # Преобразование текста и ключа в двоичный вид
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    binary_key = ''.join(format(ord(char), '08b') for char in key)

    # Шифрование/расшифрование текста
    encrypted_text = ''
    for i in range(len(binary_text)):
        # Применение XOR-операции к каждому биту текста и ключа
        result_bit = int(binary_text[i]) ^ int(binary_key[i % len(binary_key)])
        encrypted_text += str(result_bit)

    # Преобразование бинарного текста в символы алфавита, знаки препинания и цифры
    # Фактически обратная операция того что делали выше
    decrypted_text = ''
    for i in range(0, len(encrypted_text), 8):
        byte = encrypted_text[i:i+8]
        decrypted_text += chr(int(byte, 2))

    return decrypted_text


def main():
    parser = argparse.ArgumentParser(description="Скрипт для шифрования/расшифрования файла")
    parser.add_argument("filepath", type=str, help="Путь до файла")
    parser.add_argument("key", type=str, help="Секретный ключ")

    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        sys.exit('Файл не найден по пути {}'.format(args.filepath))

    if os.stat(args.filepath).st_size == 0:
        sys.exit("Файл {} пустой".format(args.filepath))

    answer = ""
    with open(args.filepath, "r", encoding="utf-8") as file:
        text = file.read()
        answer = xor_cipher(text, args.key)
        file.close()

    with open(args.filepath, "w", encoding="utf-8") as file:
        file.write(answer)
        file.close()


if __name__ == '__main__':
    main()

class CryptTest(unittest.TestCase):
    def test_crypt_short(self):
        text = "test"
        secret = "секрет"
        self.assertEqual(xor_cipher(xor_cipher(text, secret), secret), text)

    def test_crypt_medium(self):
        text = "testlongword"
        secret = "секрет"
        self.assertEqual(xor_cipher(xor_cipher(text, secret), secret), text)

    def test_crypt_long(self):
        text = "testlongwordlonglonglong"
        secret = "секрет"
        self.assertEqual(xor_cipher(xor_cipher(text, secret), secret), text)

    def test_crypt_space(self):
        text = "testlon gwordlon glon glong"
        secret = "секрет"
        self.assertEqual(xor_cipher(xor_cipher(text, secret), secret), text)