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
def user_check(id):
  req = requests.get(
    'http://localhost:3001/user/check' +
    '?idUser=' + str(id)
  )
  return req.text

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
