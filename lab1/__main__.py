import argparse
import os
import sys

# Функция принимает массив байт и высчитывает для них CRC
# Данные брались из таблицы http://reveng.sourceforge.net/crc-catalogue/16.htm
def crc16(data):
    crc = 0xFFFF # Заранее определенный регистр CRC согласно таблице
    poly = 0xA001 # Предопределенный полином обратный по таблице

    for b in data:
        crc ^= b
        for _ in range(8): # Для каждого бита 
            if crc & 0x0001: # Если текущий бит равен 1, выполняем XOR на предопределенный полином
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1 # Иначе смещаем на один бит вправо

    return crc # Возвращаем нашу сумму

# Здесь используется реализация CRC-32/BZIP2
def crc32(data):
    crc = 0xffffffff 
    poly = 0x04C11DB7 # Прямой полиндром

    for b in data:
        crc ^= b << 24
        for _ in range(8):
            if crc & 0x80000000 :
               crc = (crc << 1) ^ poly
            else:
                crc <<= 1
    
    crc = ~crc
    crc &= 0xffffffff

    return crc

def main():
    parser = argparse.ArgumentParser(description="Скрипт для посчитывания checksum файла")
    parser.add_argument("filepath", type=str, help="Путь до файла")

    args = parser.parse_args()

    # Проверка на файл
    if not os.path.exists(args.filepath):
        sys.exit('Файл не найден по пути ' + args.filepath)

    if os.stat(args.filepath).st_size == 0:
        sys.exit("Файл пустой")

    with open(args.filepath, "rb") as file:
        data = file.read()
        print("CRC16 сумма файла {} равна {}".format(args.filepath, crc16(data)))
        print("CRC32 сумма файла {} равна {}".format(args.filepath, crc32(data)))

if __name__ == '__main__':
    main()