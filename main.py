import vk_api
from auth import token

vk_session = vk_api.VkApi(token=token)

def get_friends(user_id):
    try:
        response = vk_session.method('friends.get', {'user_id': user_id})
        return response.get('items', [])
    except vk_api.exceptions.ApiError as e:
        if e.code == 18:
            print(f"Пользователь {user_id} был удален или заблокирован.")
        else:
            print(f"Ошибка при получении друзей: {e}")
        return []

def get_deep_friends(user_id, depth=1, max_depth=2):
    if depth > max_depth:
        return {}

    friends = {user_id: get_friends(user_id)}
    for user in friends[user_id]:
        friends_deep = get_deep_friends(user, depth + 1, max_depth)
        friends.update(friends_deep)

    return friends

if __name__ == '__main__':
    targets = [1]
    for user_id in targets:
        with open(str(user_id) + '.txt', 'w+', encoding='utf-8') as file:
            for key, value in get_deep_friends(user_id).items():
                file.write('%s:%s\n' % (key, value))
