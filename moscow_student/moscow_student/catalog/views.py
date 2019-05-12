# coding utf8
from time import *
import vk
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import AuthorizationForm
from .models import SpisokSM
from random import uniform
from moscow_student.moscow_st import VKAuth


def get_members(chat_id):  # #Возвращает список словарей вида [{},{},{}], гле {} словарь сданными о пользователе: id, first_name, last_name, is_closed, 'can_access_closed'

    data = vk.messages.getConversationMembers(
        peer_id=2000000000 + chat_id,
        fields=['id', 'first_name', 'last_name']
    )
    return data['profiles']


# Получает id пользователя и список чатов дирекции. Возращает список бесед, где есть слово 'епартамент'
# vk_session = vk_api.VkApi(token='')  # Регистрация обязательно с помощью aceess_token
# vk = vk_session.get_api()
def get_chats(id, chat_ids):
    data = vk.messages.getChat(chat_ids=chat_ids)
    chats_names = list()
    for chats in data:
        for i in chats["users"]["id"]:
            if id == i:
                try:
                    chats["title"].index('епартамент')
                    chats_names.append(chats["title"])
                except ValueError:
                    pass
    return chats_names


def authorization(request):
    return render(request, 'authorization.html', )


def autolike(request):
    form = AuthorizationForm(request.POST)
    data = "/catalog/success/"
    us_id = ''
    direction_id = [68047328, 1]
    if request.method == 'POST':
        if form.is_valid():
            login = form.cleaned_data['login']
            pass1 = form.cleaned_data['password']
            departament = form.cleaned_data['departament_name']
            # Авторизация пользователя по логину и паролю
            vk_1 = VKAuth(['wall,offline'], '6911940', '5.92', email=login, pswd=pass1)
            vk_1.auth()
            # Получение токена и id пользователя
            token = vk_1.get_token()
            us_id = vk_1.get_user_id()
            str_sm = SpisokSM.objects.all()
            for i in direction_id:
                if us_id == str(i):
                    data = "/catalog/authorization/"
            # Если БД не пустая, то проверка токена на наличие его в БД, если нет записать, если есть удалить и записать
            if str_sm:
                for i in str_sm:
                    if i.user_id != us_id:
                        spisok = SpisokSM()
                        spisok.user_id = us_id
                        spisok.access_token = token
                        spisok.departament = departament
                        spisok.save()
                    else:
                        i.delete()
                        spisok = SpisokSM()
                        spisok.user_id = us_id
                        spisok.access_token = token
                        spisok.departament = departament
                        spisok.save()
            # Если БД пустая, то записать токен
            else:
                spisok = SpisokSM()
                spisok.user_id = us_id
                spisok.access_token = token
                spisok.save()
    return render(request, 'autolike.html', {'form': form, 'url_host': request.get_host() + data})


def success(request):
    return render(request, 'success.html')


def work(request):
    minute = 60
    second = 60
    hour = 5
    while True:
        qwerty = SpisokSM.objects.all()
        n = SpisokSM.objects.all().count()  # Количество участников
        step_time = 1  # Шаг в секундах
        n_min = 30  # кол-во минут в течение которых ставятся лайки
        seconds = 60  # кол-во секунд в 1 минуте
        a = time()  # кол-во секунда с 00:00 01.01.1970  до начала лайктайма
        delta_a = n_min * seconds
        # Список лучайных значений от 0 до delta_a в порядке возрастания
        random_znach = sorted(list([uniform(0, delta_a) for i in range(n)]))
        # Цикл, в котором в течение n_min минут ставятся лайки
        k = 0
        for _ in range(int(delta_a / step_time)):
            try:
                # Если разница между текущем временем и временем начала + рандомное кол-во секунд = 0, то поставить лайк
                if not (int(a + random_znach[k] - time())):
                    N = 15  # Количество постов
                    groups_owner_id = -133029999  # id группы студент москвы -133029999
                    i = qwerty[k]
                    session = vk.Session(access_token=i.access_token)
                    vk_api_1 = vk.API(session, v='5.92')
                    # Получаем id N постов
                    results = vk_api_1.wall.get(owner_id=groups_owner_id, count=N)
                    # Цикл, который простовляет лайки, если их нет
                    try:
                        for i in range(len(results['items'])):
                            if not vk_api_1.likes.isLiked(type="post", owner_id=groups_owner_id,
                                                          item_id=results['items'][i]['id'])['liked']:
                                vk_api_1.likes.add(type="post", owner_id=groups_owner_id,
                                                   item_id=results['items'][i]['id'])
                                sleep(2)
                    except:
                        err1 = "IndexError"
                    k += 1
            except IndexError:
                err = "IndexError"
            sleep(step_time)
        sleep(hour * minute * second)
        qwerty1 = SpisokSM.objects.all()
    return HttpResponseRedirect(request.GET.get('next'))
