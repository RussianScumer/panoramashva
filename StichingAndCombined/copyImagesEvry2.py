import os
import shutil

# Исходная и целевая папки
source_dir = r"C:\OSPanel\domains\TgBot\panoramashva\images6000"
target_dir = r"C:\OSPanel\domains\TgBot\panoramashva\images6002"

# Создаем целевую папку, если она не существует
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Список файлов в исходной папке
files = os.listdir(source_dir)

# Перебираем файлы и копируем каждое второе изображение
for i, file in enumerate(files):
    if i % 2 == 0:  # Копируем каждое второе изображение
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, file)
        shutil.copy2(source_file, target_file)
        print(f"Скопировано: {file}")