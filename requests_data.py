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
  

# user
def get_profile(user_id):
  req = requests.get(
    'http://localhost:3001/user/profile' +
    '?idUser=' + str(user_id)
  )
  profile = req.json()
  return profile

def create_chanel(idUser, idChanel):
  req = requests.get(
  'http://localhost:3001/chanel/create' +
  '?idUser=' + str(idUser) +
  '&idChanel=' + str(idChanel)
  )
  status = req.json()
  return status

def user_check(id):
  req = requests.get(
    'http://localhost:3001/user/check' +
    '?idUser=' + str(id)
  )
  return req.text

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
  return req.text

# def opt_set(id, chanel, data):
def opt_set(id, data):
  req = requests.post(
    'http://localhost:3001/opt/set' +
    '?idUser=' + str(id),
    # '&chanel=' + str(chanel), 
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
    'http://localhost:3001/recommendations/get'
  )
  return req.json()

def recommendations_ind_get(id):
  req = requests.get(
    'http://localhost:3001/recommendations/individual' +
    '?idRecommendation=' + str(id)
  )
  return req.json()
