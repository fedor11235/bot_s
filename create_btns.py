import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

data_reservation = ['01.07', '02.07', '03.07', '04.07', '05.07', '06.07', '07.07', '08.07', '09.07', '10.07']
data_reservation_time = [
  ['8:10', '13:10', '18:10'],
  ['9:10', '14:10', '19:10'],
  ['10:10', '15:10', '20:10'],
  ['11:10', '16:10', '21:10'],
  ['12:10', '17:10', '22:10'],
]

def get_opt_create():
  keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='opt_create'), InlineKeyboardButton("Изменить", callback_data='test')]]
  return InlineKeyboardMarkup(keyboard)

def get_reservation_table():
  keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='opt_save'), InlineKeyboardButton("Изменить", callback_data='test')]]
  return InlineKeyboardMarkup(keyboard)

def get_reservation_more_table():
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='test'), InlineKeyboardButton("Утро", callback_data='test'), InlineKeyboardButton("День", callback_data='test'), InlineKeyboardButton("Вечер", callback_data='test')])
  for data in data_reservation:
    keyboard.append([InlineKeyboardButton(data, callback_data='test'), InlineKeyboardButton(" ", callback_data='reservation_morning_' + data), InlineKeyboardButton(" ", callback_data='reservation_day_' + data), InlineKeyboardButton(" ", callback_data='reservation_evening_' + data)])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='test'), InlineKeyboardButton("Потдвердить", callback_data='opt_confirm')])
  return InlineKeyboardMarkup(keyboard)

def get_reservation_time_table():
  keyboard = []
  keyboard.append([InlineKeyboardButton("Утро", callback_data='test'), InlineKeyboardButton("День", callback_data='test'), InlineKeyboardButton("Вечер", callback_data='test')])
  for data_row in data_reservation_time:
    row = []
    for data in data_row:
      row.append(InlineKeyboardButton(data, callback_data='time_' + data))
    keyboard.append(row)
  keyboard.append([InlineKeyboardButton("Потдвердить", callback_data='opt_time')])
  return InlineKeyboardMarkup(keyboard)

def get_btns_pay():
  keyboard = [
    [InlineKeyboardButton("Ввести промокод", callback_data='promocode_enter')],
    [InlineKeyboardButton("30 дней за 0", callback_data='test')],
    [InlineKeyboardButton("90 дней за 0", callback_data='test')],
    [InlineKeyboardButton("365 дней за 0", callback_data='test')],
  ]
  return InlineKeyboardMarkup(keyboard)

def get_user_chanels(chanels_array):
  keyboard = []
  for chanel in chanels_array:
    keyboard.append([InlineKeyboardButton(chanel['idChanel'], callback_data='opt_init_' + chanel['idChanel'])])
  return InlineKeyboardMarkup(keyboard)

def get_categories(category_type, start_cut, finish_cut, page):
  categoriesBtns = []
  req = requests.get(
    'http://localhost:3001/chanel/categories' +
    '?category=' + category_type
    )
  categoriesArray =  req.json()
  if len(categoriesArray) != 0:
    categoriesBtns = parse_categories(categoriesArray[start_cut:finish_cut], category_type, page)
  return categoriesBtns

def set_catalog():
  keyboard = [
    [InlineKeyboardButton("Все тематики", callback_data='all_static_0')],
    [InlineKeyboardButton("Образование", callback_data='education_static_0')],
    [InlineKeyboardButton("Финансы", callback_data='finance_static_0')],
    [InlineKeyboardButton("Здоровье", callback_data='health_static_0')],
    [InlineKeyboardButton("Новости", callback_data='news_static_0')],
    [InlineKeyboardButton("IT", callback_data='tech_static_0')],
    [InlineKeyboardButton("Развлечения", callback_data='entertainment_static_0')],
    [InlineKeyboardButton("Психология", callback_data='psychology_static_0')],
    [InlineKeyboardButton("Видосики", callback_data='video_static_0')],
    [InlineKeyboardButton("Авторские", callback_data='author_static_0')],
    [InlineKeyboardButton("Другое", callback_data='other_static_0')],
  ]
  return InlineKeyboardMarkup(keyboard)

def query_parse(name, query):
  return name + '_' + query

def set_filters(query, mode_callback):
  print('query', query)
  keyboard = []
  if mode_callback:
    keyboard = [
      [InlineKeyboardButton("Фильтры", callback_data=query + '_static_0')],
      [InlineKeyboardButton("Рейтинг", callback_data=query_parse('rating', query))],
      [InlineKeyboardButton("Охват", callback_data=query_parse('coverage', query))],
      [InlineKeyboardButton("Кол-во подписчиков", callback_data=query_parse('numberSubscribers', query))],
      [InlineKeyboardButton("Прирост за месяц", callback_data=query_parse('growthMonth', query))],
      [InlineKeyboardButton("Прирост за неделю", callback_data=query_parse('growthWeek', query))],
      [InlineKeyboardButton("Прирост за день", callback_data=query_parse('growthDay', query))],
      [InlineKeyboardButton("Сначала новые", callback_data=query_parse('new', query))],
      [InlineKeyboardButton("Сначала старые", callback_data=query_parse('old', query))],
      [InlineKeyboardButton("Подтвержденные", callback_data=query_parse('confirm', query))],
      [InlineKeyboardButton("Применить", callback_data=query_parse('apply', query))]
    ]
  else:
    keyboard = [
      [InlineKeyboardButton("Фильтры", callback_data='static_0')],
      [InlineKeyboardButton("Рейтинг", callback_data='rating_' + query)],
      [InlineKeyboardButton("Охват", callback_data='coverage_' + query)],
      [InlineKeyboardButton("Кол-во подписчиков", callback_data='numberSubscribers_' + query)],
      [InlineKeyboardButton("Прирост за месяц", callback_data='growthMonth_' + query)],
      [InlineKeyboardButton("Прирост за неделю", callback_data='growthWeek_' + query)],
      [InlineKeyboardButton("Прирост за день", callback_data='growthDay_' + query)],
      [InlineKeyboardButton("Сначала новые", callback_data='new_' + query)],
      [InlineKeyboardButton("Сначала старые", callback_data='old_' + query)],
      [InlineKeyboardButton("Подтвержденные", callback_data='confirm_' + query)],
      [InlineKeyboardButton("Применить", callback_data='apply_' + query)]
    ]
  return InlineKeyboardMarkup(keyboard)


def go_into_opt():
  keyboard = [
    [InlineKeyboardButton("Все тематики", callback_data='opt_all')],
    [InlineKeyboardButton("Образование", callback_data='opt_education')],
    [InlineKeyboardButton("Финансы", callback_data='opt_finance')],
    [InlineKeyboardButton("Здоровье", callback_data='opt_health')],
    [InlineKeyboardButton("Новости", callback_data='opt_news')],
    [InlineKeyboardButton("IT", callback_data='opt_tech')],
    [InlineKeyboardButton("Развлечения", callback_data='opt_entertainment')],
    [InlineKeyboardButton("Психология", callback_data='opt_psychology')],
    [InlineKeyboardButton("Видосики", callback_data='opt_video')],
    [InlineKeyboardButton("Авторские", callback_data='opt_author')],
    [InlineKeyboardButton("Другое", callback_data='opt_other')],
  ]
  return InlineKeyboardMarkup(keyboard)

def go_chanel_opt(category_type, start_cut, finish_cut, page):
  categoriesBtns = []
  req = requests.get(
    'http://localhost:3001/chanel/categories' +
    '?category=' + category_type
    )
  categoriesArray =  req.json()
  if len(categoriesArray) != 0:
    categoriesBtns = parse_categories_opt(categoriesArray[start_cut:finish_cut], category_type, page)
  return categoriesBtns

def parse_categories_opt(categoriesArray, category_type, page):
  if len(categoriesArray) == 0:
    return 'каналов по запросу нет'
  arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='filters_' + category_type +'_'+ str(page))]]
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['username'] + ' ' + str(category['participants_count']), callback_data='opt_' + category['username'] + '_' + category_type)])
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=('opt_' + category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=('opt_' + category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

def parse_categories(categoriesArray, category_type, page):
  if len(categoriesArray) == 0:
    return 'каналов по запросу нет'
  arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='filters_' + category_type +'_'+ str(page))]]
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['username'] + ' ' + str(category['participants_count']), callback_data=category['username'] + '_' + category_type)])
    # output += category['username'] + ' количество подписчиков: ' + str(category['participants_count']) + ' суммарный дневной охват: ' + str(category['daily_reach']) + ' количнсвто репостов в другие каналы: ' + str(category['forwards_count']) + '\n'
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=(category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=(category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

def opt_reservation():
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='test'), InlineKeyboardButton("Утро", callback_data='test'), InlineKeyboardButton("День", callback_data='test'), InlineKeyboardButton("Вечер", callback_data='test')])
  for data in data_reservation:
    keyboard.append([InlineKeyboardButton(data, callback_data='test'), InlineKeyboardButton(" ", callback_data='opt_reservation_data_morning_' + data), InlineKeyboardButton(" ", callback_data='opt_reservation_day_' + data), InlineKeyboardButton(" ", callback_data='opt_reservation_evening_' + data)])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='test'), InlineKeyboardButton("Потдвердить", callback_data='opt_reservation_confirm')])
  return InlineKeyboardMarkup(keyboard)