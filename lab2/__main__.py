import argparse
import os
import sys

# Проверка что директория существует, не пустая, и это не файл
def isEmpty(path):
    if os.path.exists(path) and not os.path.isfile(path):
        return not os.listdir(path)
    else:
        return False

# Получаем ХЭШ сумму по относительному пути до файла
def getHash(filepath):
    with open(filepath, "rb") as file:
        data = file.read()
        return hash(data)
    

# Возвращает все файлы с совпадающей хэш суммой
def scanDirByHash(path, h):
    founded = []
    
    for root, _, files in os.walk(path):
        for file in files:
            if os.stat(os.path.join(root, file)).st_size != 0:
                if getHash(os.path.join(root, file)) == h:
                    founded.append(os.path.join(root, file))

    return founded
            

def main():
    parser = argparse.ArgumentParser(description="Скрипт для сканирования директории файлов и поиска его копий")
    parser.add_argument("dir", type=str, help="Начальная директория")

    args = parser.parse_args()

    # Проверка на существование директории
    if isEmpty(args.dir):
        sys.exit('Директория {} не найдена или пустая'.format(args.dir))

    for root, _, files in os.walk(args.dir):
        for file in files:
            result = scanDirByHash(root, getHash(os.path.join(root, file)))

            if os.path.join(root, file) in result:
                result.remove(os.path.join(root, file))

            if len(result) != 0:
                print("Для файла {} найдены {} копии: ".format(os.path.join(root, file), len(result)))
                for f in result:
                    print(f)


if __name__ == '__main__':
    main()