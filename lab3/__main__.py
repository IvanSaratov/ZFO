import argparse
import sys
import os

# Вспомогательная функция для конвертирования из bin в str
def bin2str(data):
    str = ''
    for i in range(0, len(data), 8):
        decimal_data = int(data[i:i + 8], 2)
        str = str + chr(decimal_data) 

    return str

# Функция зашифровки/расшифровки текста по представленному ключу
def crypt(text, key):
    # Представляем ключ и текст в двоичный формат
    bin_text = ''.join(format(ord(x), '08b') for x in text)
    bin_key = ''.join(format(ord(x), '08b') for x in key)

    # Шифруем
    bin_result = ''.join('1' if x!=y else '0' for (x,y) in zip(bin_text, bin_key))
    
    # Переводим из двоичного в строки
    result = bin2str(bin_result)
    
    return result


def match(text, alphabet=set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789.,:;!?')):
    return not alphabet.isdisjoint(text.lower())


def main():
    parser = argparse.ArgumentParser(description="Скрипт для шифрования/расшифрования файла")
    parser.add_argument("filepath", type=str, help="Путь до файла")
    parser.add_argument("key", type=str, help="Секретный ключ")
    parser.add_argument("-m", help="При включении дешифрует сообщение, иначе шифрует", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        sys.exit('Файл не найден по пути {}'.format(args.filepath))

    if os.stat(args.filepath).st_size == 0:
        sys.exit("Файл {} пустой".format(args.filepath))

    if not match(args.key):
        sys.exit("Ключ не состоит из русских символов, цифр или знаков припинания")

    with open(args.filepath, "r", encoding="utf-8") as file:
        text = file.read()
        # if not match(text):
        #     sys.exit("Текст не состоит из русских символов, цифр или знаков припинания")

        tmp = crypt(text, args.key)
        new_file_name = ""
        if args.m:
            new_file_name = "{}_encrypted.txt".format(os.path.splitext(args.filepath)[0])
        else:
            new_file_name = "{}_decrypted.txt".format(os.path.splitext(args.filepath)[0])
            
        with open(new_file_name, "w", encoding="utf-8") as write_file:
            write_file.write(tmp)
            write_file.close()

    print(crypt("óqh", args.key))

if __name__ == '__main__':
    main()