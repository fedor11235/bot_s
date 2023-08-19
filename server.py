import sqlite3, os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
API_TOKEN = os.getenv('API_TOKEN')

app = Flask(__name__)

def print_table():
  sqlite_connection = sqlite3.connect('test.db')
  cursor = sqlite_connection.cursor()
  cursor.execute("SELECT * FROM score")
  rows = cursor.fetchall()

  for row in rows:
    print(row)

  cursor.close()

def insert_varible_into_table(user_id, user_score, username):
  try:
    sqlite_connection = sqlite3.connect('test.db')
    cursor = sqlite_connection.cursor()
    print("Connected to SQLite")

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS score(
        user_id INT PRIMARY KEY,
        username TEXT,
        user_score INT
      );""")

    notWrite  = False
    info = cursor.execute('SELECT * FROM score WHERE user_id=?', (user_id, ))
    user = info.fetchone()

    if user is None:
      sqlite_insert_with_param = """INSERT INTO score
                        (user_score, username, user_id)
                        VALUES (?, ?, ?);"""
    elif user[2] < int(user_score):
      print('update')
      sqlite_insert_with_param = """UPDATE score SET user_score = ?, username =? WHERE user_id = ?"""
    else:
      notWrite = True

    if not notWrite:
      data_tuple = (user_score, username, user_id)
      cursor.execute(sqlite_insert_with_param, data_tuple)
      sqlite_connection.commit()
      print("DB updated")

    cursor.close()

  except sqlite3.Error as error:
    print("Error while working with SQLite", error)
  finally:
    if sqlite_connection:
      sqlite_connection.close()
      print("SQLite connection closed")

def get_top_user_score(user_id):
  sqlite_connection = sqlite3.connect('test.db')
  cursor = sqlite_connection.cursor()
  cursor.execute('''
    SELECT count(name) FROM sqlite_master WHERE type='table' AND name='score'
  ''')

  if cursor.fetchone()[0]==1 :
    cursor.execute("""
      SELECT * FROM score
      ORDER BY user_score DESC
    """)
    top_user = cursor.fetchall()

  else:
    top_user = []

  cursor.close()

  top_10_user = top_user[0:10]

  result = []
  ifUserTop = False

  for user in top_10_user:
    if user[0] == int(user_id):
      ifUserTop = True

  if ifUserTop:
    result = top_10_user

  else:
    for index, user in enumerate(top_user, start=1):
      if user[0] == int(user_id):
        result = [index, user[1], user[2]]

  return result

# TODO прописываем апишку для сохранения счёта, декодировать/кодировать счет, сделать POST запросом
@app.route('/setUserScore', methods=['GET'])
def set_user_score():
  inline_message_id = request.args.get('inline_message_id')
  user_id = request.args.get('user_id')
  user_score = request.args.get('user_score')
  username = request.args.get('username')

  URL = (
    'https://api.telegram.org/bot' +
    API_TOKEN + '/setGameScore' +
    '?user_id=' + user_id +
    '&score=' + user_score
  )

  if inline_message_id:
    URL +=  '&inline_message_id=' + inline_message_id

  else:
    chat_id = request.args.get('chat_id')
    message_id = request.args.get('message_id')
    URL +=  '&chat_id=' + chat_id + '&message_id=' + message_id

  requests.get(URL)

  insert_varible_into_table(user_id, user_score, username)

  return {
    'user_id': user_id,
    'user_score': user_score,
    'username': username
  }

@app.route('/getUserScore', methods=['GET'])
def get_user_score():
  user_id = request.args.get('user_id')
  top_user = get_top_user_score(user_id)
  return top_user

def main():
  app.run(debug=True, host=HOST, port=PORT)

if __name__ == '__main__':
  main()