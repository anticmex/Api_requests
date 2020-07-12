import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def get_filename_from_path(file_name):
    word = ''
    for i, word in enumerate(reversed(file_name)):
        if word == '/':
            break
    return file_name[len(file_name) - i:]


def folder_selection(json_list):
    folder_list = []
    for items in json_list['_embedded']['items']:
        if not "." in items['name']:
            folder_list.append(items["name"])
    print("Желаете указать папку для загрузки файла?")
    print(f'Текущие папки на диске:\n{folder_list}')
    question_to_user = \
        input("'y'- да, выбрать; 'n' - нет, загрузить в корень; 'иное' - создать временную папку для загрузки.")
    if question_to_user == 'y':
        folder_name = input("Укажите название папки: ")
    elif question_to_user == 'n':
        folder_name = ''
    else:
        folder_name = 'Временная'
    return folder_name


BASE_URL = 'https://cloud-api.yandex.net:443'
token = input("Введите токен для работы: ")

AUTHOR = {"Authorization": token}
BAS_STRUCTURE_URL = '/v1/disk/resources'
BASE_UPLOAD_URL = BAS_STRUCTURE_URL + '/upload'
DISK_ROOT = {'path': '/'}

disk_folders_request = requests.get(BASE_URL + BAS_STRUCTURE_URL, params=DISK_ROOT, headers=AUTHOR)

disk_folder_upload_name = "/" + folder_selection(disk_folders_request.json()) + "/"

question_to_user = input("Уверены, что хотите загрузить файлы на диск? Наберите 'y' если да: ")

if question_to_user == 'y' or question_to_user == 'у' or question_to_user == 'да' or question_to_user == 'yes':
    Tk().withdraw()
    full_path_filename = askopenfilename()
    filename = get_filename_from_path(full_path_filename)
    disk_pre_upload_params = {'path': disk_folder_upload_name+filename, 'overwrite': 'true'}
    files = {'file': full_path_filename}

    pre_upload_url = requests.get(BASE_URL+BASE_UPLOAD_URL, headers=AUTHOR, params=disk_pre_upload_params)

    upload = requests.put(pre_upload_url.json()['href'], headers=AUTHOR, files=files)
    if upload.status_code < 400:
        print("Загрузка файла прошла успешно!")
    else:
        print("Что-то пошло не так!")