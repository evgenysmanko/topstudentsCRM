import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


login = '#'  # #Сюда пишеться логин странциы
password = '#'  # #Сюда пишеться пароль странциыц
vk_session = vk_api.VkApi(login, password)  # # Регистрация
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_members(chat_id):

    data = vk.messages.getConversationMembers(
        peer_id=2000000000 + chat_id,
        fields=['id', 'first_name', 'last_name']
    )
    return data['profiles']


"""
Возвращает список словарей вида [{},{},{}], где {} словарь сданными о пользователе:
 id, first_name, last_name, is_closed, 'can_access_closed'
"""



def add_user(chat_id, user_id):  # #Добавляет пользователя user_id в беседу chat_id(id для бота)
    vk.messages.addChatUser(
        chat_id=chat_id,
        user_id=user_id
    )


def kick_user(chat_id, user_id):  # #Удаляет пользователя user_id из беседы chat_id(id для бота)
    vk.messages.removeChatUser(
        chat_id=chat_id,
        user_id=user_id
    )


def control(request):
    if request.GET.get('kick_btn'):
        kick_user(1, 1)


"""

То, что в скобках у get должно стоять в параметре name 

    <form method="get">
        <input type="submit" class="btn" value="Click" name="kick_btn">
    </form>
    
Но перед этим нужно добавить функцию control в urls.py 
    
"""
def total_chat_list(user_id, *chat_ids):
    chats = []
    for chat_id in chat_ids:
        chat_data=vk.messages.getConversationMembers(
            chat_id=chat_id
        )
        count = chat_data['count']
        for i in range(count):
            if user_id in chat_data['profiles'][i]['id']:
                chats.append(chat_id)
    return chats


"""
Функция total_chat_list возвращает списко бесед пользователя user_id в которых он состоит
из набора *chat_ids
chat_ids — id бесед, по которым идёт поиск (если удобнее - можно передать список)
"""


def total_users(*chat_ids):
    users = []
    for chat_id in chat_ids:
        data = vk.messages.getConversationMembers(chat_id=chat_id)
        for i in range(data['count']):
            try:
                users.append(dict(id=data['profiles'][i]['id'],
                                  first_naem=data['profiles'][i]['first_name'],
                                  last_name=data['profiles'][i]['last_name']))
            except IndexError:
                pass
    return users
