import requests

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
  return req.text

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
    '&idUser=' + str(id)
  )
  print('opt_get', req.json())
  return req.json()
