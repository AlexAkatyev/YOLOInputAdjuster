import shutil
import os

# Настройки
train_file = 'autosplit_train.txt'        # Текстовый файл со списком путей
validate_file = 'autosplit_val.txt'        # Текстовый файл со списком путей
target_dir = 'separated' # Куда копируем
train_dir = 'train'
validate_dir = 'val'
image_dir = 'images'
label_dir = 'labels'

def copy_from_list(txt_path, destination):
    global target_dir
    global image_dir
    # Создаем папку, если её нет
    img_dir = target_dir + '/' + image_dir + '/' + destination
    lbl_dir = target_dir + '/' + label_dir + '/' + destination
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(lbl_dir, exist_ok=True)

    # Читаем файл со списком
    if not os.path.exists(txt_path):
        print(f"File {txt_path} not found.")
        return

    with open(txt_path, 'r', encoding='utf-8') as f:
        # line.strip() убирает пробелы и символы переноса строки (\n)
        files = [line.strip() for line in f if line.strip()]

    for img_file in files:
        if os.path.isfile(img_file):
            try:
                shutil.copy(img_file, img_dir)
                print(f"Copyed: {os.path.basename(img_file)}")
                lbl_file = img_file.lower().replace('.png', '.txt', -1)
                shutil.copy(lbl_file, lbl_dir)
                print(f"Copyed: {os.path.basename(lbl_file)}")
            except Exception as e:
                print(f"Error of copy {img_file}: {e}")
        else:
            print(f"File not found: {img_file}")


if __name__ == "__main__":
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(target_dir + '/' + image_dir, exist_ok=True)
    os.makedirs(target_dir + '/' + label_dir, exist_ok=True)
    copy_from_list(train_file, train_dir)
    copy_from_list(validate_file, validate_dir)
