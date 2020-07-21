import requests
from pprint import pprint
import time
from tqdm import tqdm


class VkApi:
    # Класс созданный для работы с некоторыми функциями ВК через API

    def __init__(self, token):
        self.token = token
        self.params = {'access_token': token}
        self.base_url = 'https://api.vk.com/method/'

    def __main_url__(self, vk_method):
        # создание базовой URL для VK API

        return self.base_url + vk_method

    def alternative_mutual_friends_finder(self, source_uid, target_uid):
        # Попытка поиска общих друзей в случае если токен пользователя не позволяет получить доступ к просмотру
        # общих друзей запрошенных Юзеров.

        user1_friends = set(self.friends_list(source_uid, 0)['response']['items'])
        user2_friends = set(self.friends_list(target_uid, 0)['response']['items'])

        id_list = []
        for ids in user1_friends & user2_friends:
            id_list.append(ids)

        return f'Список общих друзей пользователя {source_uid} и {target_uid} следующий:\n' \
               f'{self.id_to_name_convertor(id_list)}'

    def friends_list(self, user_id, cheker=1):
        # метод определяющий список друзей пользователя(по user_id)

        self.request_friends = requests.get(
            f'{self.__main_url__("friends.get")}?user_id={user_id}&v=5.21',
            params=self.params
        )
        if cheker == 0:
            return self.request_friends.json()
        else:
            id_list = self.request_friends.json()['response']['items']

            return f'Список друзей пользователя {user_id} следующий:\n {self.id_to_name_convertor(id_list)}'

    def mutual_friends(self, source_uid, target_uid):
        # метод определяющий список общий друзей пользователя(по user_id) и пользователя чей токен применен

        self.mutual_friends = requests.get(
            f'{self.__main_url__("friends.getMutual")}'
            f'?source_uid={source_uid}&target_uid={target_uid}&v=5.21',
            params=self.params
        )

        if 'error' in self.mutual_friends.json():
            return self.alternative_mutual_friends_finder(source_uid, target_uid)
        else:
            id_list = self.mutual_friends.json()['response']
            print(id_list)
            return f'Список общих друзей пользователя {source_uid} и {target_uid} следующий:\n ' \
                   f'{self.id_to_name_convertor(id_list)}'

    def id_to_name_convertor(self, *user_id):
        # позволяет узнать человекочитаемое имя пользователя по его ID vk. и отображение в более-менее красивом виде.

        usersid_name = {}

        if isinstance(user_id[0], list):
            user_id = user_id[0]

        for id in tqdm(user_id):
            req = requests.get(
                f'https://api.vk.com/method/users.get?user_ids={id}&v=5.120',
                params={'access_token': self.token}
            )

            if not 'error' in req.json():
                usersid_name['id' + str(id)] = req.json()['response'][0]['first_name'] + \
                                               " " + \
                                               req.json()['response'][0]['last_name']

            else:
                time.sleep(4)

        return usersid_name


def main():
    token = input("Введите токен для дальнейшей работы: ")
    print("Чтобы Вы хотели получить от программы:")
    print("'1' - список друзей пользователя ВК, '2' - список общих друзей 2х пользователей?")
    user_question = input()
    if user_question == '1':
        print("\nВы успешно выбрали первый вариант!")
        pprint(VkApi(token).friends_list(input("Введите id пользователя ВК: ")))
    elif user_question == '2':
        pprint(VkApi(token).mutual_friends(input("Введите id первого пользователя ВК: "),
                                           input("Введите id второго пользователя ВК: ")))
    else:
        print("Очень жаль, что Вы не определились с выбором. :(")


main()
