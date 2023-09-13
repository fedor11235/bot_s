import requests

def user_check(id):
  req = requests.get(
    'http://localhost:3001/check' +
    '?idUser=' + str(id)
  )
  return req.text

def user_change_message_mod(id, mode):
  requests.get(
    'http://localhost:3001/mode-set' +
    '?idUser=' + str(id) +
    '&mode=' + mode
  )

def user_get_message_mod(id):
  req = requests.get(
    'http://localhost:3001/mode-get' +
    '?idUser=' + str(id) 
  )
  return req.text
