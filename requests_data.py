import requests
from functools import reduce

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
  

# user
def get_profile(user_id):
  req = requests.get(
    'http://localhost:3002/test/user/profile' +
    '?idUser=' + str(user_id)
  )
  profile = req.json()
  return profile

def create_chanel(idUser, idChanel, title, username=''):
  req = requests.get(
  'http://localhost:3002/test/chanel/create' +
  '?idUser=' + str(idUser) +
  '&idChanel=' + str(idChanel) +
  '&title=' + str(title) +
  '&username=' + str(username)
  )
  status = req.json()
  return status

def user_check(id):
  req = requests.get(
    'http://localhost:3002/test/user/check' +
    '?idUser=' + str(id)
  )
  return req.json()

def user_get_stat_opt(chanel):
  req = requests.get(
    'http://localhost:3002/test/opt/stat' +
    '?chanel=' + str(chanel)
  )
  return req.json()

def user_change_message_mod(id, mode):
  requests.get(
    'http://localhost:3002/test/mode/set' +
    '?idUser=' + str(id) +
    '&mode=' + mode
  )

def user_get_message_mod(id):
  req = requests.get(
    'http://localhost:3002/test/mode/get' +
    '?idUser=' + str(id) 
  )
  return req.json()

# opt
def opt_create(id, chanel):
  req = requests.get(
    'http://localhost:3002/test/opt/create' +
    '?idUser=' + str(id) +
    '&chanel=' + str(chanel)
  )
  return req.json()

# def opt_set(id, chanel, data):
def opt_set(id, data):
  req = requests.post(
    'http://localhost:3002/test/opt/set' +
    '?idUser=' + str(id),
    # '&chanel=' + str(chanel), 
      data=data
  )
  return req.json()

def opt_get(id):
  req = requests.get(
    'http://localhost:3002/test/opt/get' +
    '?idUser=' + str(id)
  )
  return req.json()

def recommendations_get():
  req = requests.get(
    'http://localhost:3002/test/recommendations/get'
  )
  return req.json()

def recommendations_ind_get(id):
  req = requests.get(
    'http://localhost:3002/test/recommendations/individual' +
    '?idRecommendation=' + str(id)
  )
  return req.json()

def set_tariff_profile(id, tariffPlan, time, is_one = 'disabled'):
  req = requests.get(
    'http://localhost:3002/test/user/set' +
    '?idUser=' + str(id) +
    '&tariffPlan=' + tariffPlan +
    '&time=' + str(time) +
    '&isOne=' + str(is_one)
  )
  return req.json()

def set_tariff_temp_profile(id, tariffPlan):
  req = requests.get(
    'http://localhost:3002/test/user/set/tariff-temp' +
    '?idUser=' + str(id) +
    '&tariffPlan=' + tariffPlan
  )
  return req.json()

def get_opt_into(id):
  req = requests.get(
    'http://localhost:3002/test/opt/into/get' +
    '?idOpt=' + str(id)
  )
  return req.json()

def set_opt_into(id, idOpt, payload, delete):
  req = requests.post(
    'http://localhost:3002/test/opt/into/set' +
    '?idUser=' + str(id) +
    '&idOpt=' + str(idOpt) +
    '&isDel=' + str(delete),
    payload
  )
  return req.json()

def set_opt_recommendation_into(id, idOpt, payload, delete = 'enabled'):
  req = requests.post(
    'http://localhost:3002/test/opt/into-recommendation/set' +
    '?idUser=' + str(id) +
    '&idOpt=' + str(idOpt) +
    '&isDel=' + str(delete),
    payload
  )
  return req.json()


def upload_promocode(id, promocode):
  req = requests.get(
    'http://localhost:3002/test/user/upload/promocode' +
    '?idUser=' + str(id) +
    '&promocode=' + str(promocode)
  )
  return req.json()

def set_any_profile(id, data):
  req = requests.post(
    'http://localhost:3002/test/user/set/profile' +
    '?idUser=' + str(id),
    data=data
  )
  return req.json()

def set_channel(id, category):
  req = requests.get(
    'http://localhost:3002/test/chanel/user/set-channel' +
    '?idUser=' + str(id) +
    '&category=' + str(category)
  )
  return req.json()

def user_opt(id):
  req = requests.get(
    'http://localhost:3002/test/user/opt-user' +
    '?idUser=' + str(id)
  )
  return req.json()

def user_recommendation_into(id):
  req = requests.get(
    'http://localhost:3002/test/user/recommendation-into-user' +
    '?idUser=' + str(id)
  )
  return req.json()

def user_opt_into(id):
  req = requests.get(
    'http://localhost:3002/test/user/opt-into-user' +
    '?idUser=' + str(id)
  )
  return req.json()


def recommendation_requisites(username):
  req = requests.get(
    'http://localhost:3002/test/recommendations/requisites' +
    '?username=' + str(username)
  )
  return req.json()


def opt_requisites(channel):
  req = requests.get(
    'http://localhost:3002/test/opt/requisites' +
    '?channel=' + str(channel)
  )
  return req.json()

def recommendation_set_check(id, chennel, file_id, path_check):
  req = requests.get(
    'http://localhost:3002/test/recommendations/set-check' +
    '?idUser=' + str(id) +
    '&chennel=' + str(chennel) +
    '&check=' + str(file_id) +
    '&checkPath=' + str(path_check)
  )
  return req.json()

def opt_set_check(id, chennel, file_id, path_check):
  req = requests.get(
    'http://localhost:3002/test/opt/set-check' +
    '?idUser=' + str(id) +
    '&chennel=' + str(chennel) +
    '&check=' + str(file_id) +
    '&checkPath=' + str(path_check)
  )
  return req.json()

def map_en(word):
  print(word)
  if word == 'morning':
    return 'утро'
  elif word == 'day':
    return 'день'
  elif word == 'evening':
    return 'вечер'

def parse_view_date(date_array):
  # print(date_array)
  if date_array[0] != '':
    test = list(map(lambda x: x.split('/'), date_array))
    # print(test)
    test = list(map(lambda x: x[1] + ' ('+ map_en(x[0])+ ')', test))
    test.sort(reverse=True)
    test = reduce(lambda x, y: x + '\n' + y, test)
    return test
  else:
    return ''
  # reduce(lambda x, y: x + '\n' + y, booking_date)

# def set_profile_opt_chanel(id, chanel):
#   req = requests.get(
#     'http://localhost:3002/test/user/set' +
#     '?idUser=' + str(id) +
#     '&chanel=' + chanel
#   )
#   return req.json() 

