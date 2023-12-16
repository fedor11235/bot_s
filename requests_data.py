from functools import reduce

import requests


def parse_filter(name):
    if name == 'forwards_count':
        return 'repost'
    elif name == 'participants_count':
        return 'numberSubscribers'
    elif name == 'avg_post_reach':
        return 'coveragePub'
    elif name == 'daily_reach':
        return 'coverageDay'
    elif name == 'ci_index':
        return 'indexSay'


def get_release_schedule(idUser):
    req = requests.get(
        'http://localhost:3001/opt/release-schedule' +
        '?idUser=' + str(idUser)
    )
    chanels = req.json()
    return chanels


def delete_opt(chanel):
    req = requests.delete(
        'http://localhost:3001/opt/opt-delete' +
        '?chanel=' + str(chanel)
    )
    chanel = req.json()
    return chanel


# user
def get_profile(user_id):
    req = requests.get(
        'http://localhost:3001/user/profile' +
        '?idUser=' + str(user_id)
    )
    profile = req.json()
    return profile


def create_chanel(idUser, idChanel, title, username=''):
    req = requests.get(
        'http://localhost:3001/chanel/create' +
        '?idUser=' + str(idUser) +
        '&idChanel=' + str(idChanel) +
        '&title=' + str(title) +
        '&username=' + str(username)
    )
    status = req.json()
    return status


def user_check(id):
    req = requests.get(
        'http://localhost:3001/user/check' +
        '?idUser=' + str(id)
    )
    return req.json()


def user_get_stat_opt(chanel):
    req = requests.get(
        'http://localhost:3001/opt/stat' +
        '?chanel=' + str(chanel)
    )
    return req.json()


def user_change_message_mod(id, mode):
    requests.get(
        'http://localhost:3001/mode/set' +
        '?idUser=' + str(id) +
        '&mode=' + mode
    )


def user_get_message_mod(id):
    req = requests.get(
        'http://localhost:3001/mode/get' +
        '?idUser=' + str(id)
    )
    return req.json()


# opt
def opt_create(id, chanel):
    req = requests.get(
        'http://localhost:3001/opt/create' +
        '?idUser=' + str(id) +
        '&chanel=' + str(chanel)
    )
    return req.json()


def opt_set(id, data):
    req = requests.post(
        'http://localhost:3001/opt/set' +
        '?idUser=' + str(id),
        data=data
    )
    return req.json()


def opt_get(id):
    req = requests.get(
        'http://localhost:3001/opt/get' +
        '?idUser=' + str(id)
    )
    return req.json()


def recommendations_get():
    req = requests.get(
        'http://localhost:3001/recommendations/get' +
        '?isBot=enable'
    )
    return req.json()


def recommendations_ind_get(id):
    req = requests.get(
        'http://localhost:3001/recommendations/individual' +
        '?idRecommendation=' + str(id)
    )
    return req.json()


def set_tariff_profile(id, tariffPlan, time, is_one='disabled'):
    req = requests.get(
        'http://localhost:3001/user/set' +
        '?idUser=' + str(id) +
        '&tariffPlan=' + tariffPlan +
        '&time=' + str(time) +
        '&isOne=' + str(is_one)
    )
    return req.json()


def set_tariff_temp_profile(id, tariffPlan):
    req = requests.get(
        'http://localhost:3001/user/set/tariff-temp' +
        '?idUser=' + str(id) +
        '&tariffPlan=' + tariffPlan
    )
    return req.json()


def get_opt_into(id):
    req = requests.get(
        'http://localhost:3001/opt/into/get' +
        '?idOpt=' + str(id)
    )
    return req.json()


def set_opt_into(id, idOpt, payload, delete):
    req = requests.post(
        'http://localhost:3001/opt/into/set' +
        '?idUser=' + str(id) +
        '&idOpt=' + str(idOpt) +
        '&isDel=' + str(delete),
        payload
    )
    return req.json()


def set_opt_recommendation_into(id, idOpt, payload, delete='enabled'):
    req = requests.post(
        'http://localhost:3001/opt/into-recommendation/set' +
        '?idUser=' + str(id) +
        '&idOpt=' + str(idOpt) +
        '&isDel=' + str(delete),
        payload
    )
    return req.json()


def upload_promocode(id, promocode):
    req = requests.get(
        'http://localhost:3001/user/upload/promocode' +
        '?idUser=' + str(id) +
        '&promocode=' + str(promocode)
    )
    return req.json()


def set_any_profile(id, data):
    req = requests.post(
        'http://localhost:3001/user/set/profile' +
        '?idUser=' + str(id),
        data=data
    )
    return req.json()


def set_channel(id, category):
    req = requests.get(
        'http://localhost:3001/chanel/user/set-channel' +
        '?idUser=' + str(id) +
        '&category=' + str(category)
    )
    return req.json()


def user_opt(id):
    req = requests.get(
        'http://localhost:3001/user/opt-user' +
        '?idUser=' + str(id)
    )
    return req.json()


def user_recommendation_into(id):
    req = requests.get(
        'http://localhost:3001/user/recommendation-into-user' +
        '?idUser=' + str(id) +
        '&bot=enabled'
    )
    return req.json()


def user_opt_into(id):
    req = requests.get(
        'http://localhost:3001/user/opt-into-user' +
        '?idUser=' + str(id)
    )
    return req.json()


def recommendation_requisites(username):
    req = requests.get(
        'http://localhost:3001/recommendations/requisites' +
        '?username=' + str(username)
    )
    return req.json()


def opt_requisites(channel):
    req = requests.get(
        'http://localhost:3001/opt/requisites' +
        '?channel=' + str(channel)
    )
    return req.json()


def recommendation_set_check(id, chennel, file_id, path_check):
    req = requests.get(
        'http://localhost:3001/recommendations/set-check' +
        '?idUser=' + str(id) +
        '&chennel=' + str(chennel) +
        '&check=' + str(file_id) +
        '&checkPath=' + str(path_check)
    )
    return req.json()


def opt_set_check(id, chennel, file_id, path_check):
    req = requests.get(
        'http://localhost:3001/opt/set-check' +
        '?idUser=' + str(id) +
        '&chennel=' + str(chennel) +
        '&check=' + str(file_id) +
        '&checkPath=' + str(path_check)
    )
    return req.json()


def opt_post_delete(user_id, chennel, opt_type, post_number):
    req = requests.delete(
        'http://localhost:3001/opt/post-delete' +
        '?idUser=' + str(user_id) +
        '&chennel=' + str(chennel) +
        '&type=' + str(opt_type) +
        '&postNumber=' + str(post_number)
    )
    return req.json()


def save_eddit_temp_post(user_id, chennel, opt_type, post_number):
    req = requests.get(
        'http://localhost:3001/opt/post-save-temp' +
        '?chanelEdit=' + str(chennel) +
        '&postId=' + str(post_number) +
        '&optType=' + str(opt_type) +
        '&idUser=' + str(user_id)
    )
    return req.json()


def save_eddit_temp_check(user_id, chennel, opt_type):
    req = requests.get(
        'http://localhost:3001/opt/check-save-temp' +
        '?chanelEdit=' + str(chennel) +
        '&idUser=' + str(user_id) +
        '&optType=' + str(opt_type)
    )
    return req.json()


def edit_post_req(user_id, post):
    req = requests.post(
        'http://localhost:3001/opt/post-edit-temp' +
        '?idUser=' + str(user_id),
        data=post
    )
    return req.json()


def edit_check_req(user_id, check, check_path):
    req = requests.get(
        'http://localhost:3001/opt/check-edit-temp' +
        '?idUser=' + str(user_id) +
        '&check=' + str(check) +
        '&checkPath=' + str(check_path)
    )
    return req.json()


def add_new_post(user_id, data):
    req = requests.post(
        'http://localhost:3001/opt/add-new-post' +
        '?idUser=' + str(user_id),
        data=data
    )
    return req.json()


def map_en(word):
    if word == 'morning':
        return 'утро'
    elif word == 'day':
        return 'день'
    elif word == 'evening':
        return 'вечер'


def parse_view_date(date_array):
    if date_array[0] != '':
        test = list(map(lambda x: x.split('/'), date_array))
        test = list(map(lambda x: x[1] + ' (' + map_en(x[0]) + ')', test))
        test.sort(reverse=True)
        test = reduce(lambda x, y: x + '\n' + y, test)
        return test
    else:
        return ''
