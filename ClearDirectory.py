import os
import shutil

def delete_files_in_folder(folder_path):
    try:
        # Проверяем, существует ли папка
        if not os.path.exists(folder_path):
            print(f"Папка {folder_path} не существует.")
            return

        # Получаем список всех файлов в папке
        files = os.listdir(folder_path)

        # Удаляем каждый файл
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Ошибка при удалении {file_path}. Причина: {e}")

        print(f"Все файлы в папке {folder_path} были удалены.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")