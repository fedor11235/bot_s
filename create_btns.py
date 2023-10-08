import requests
from datetime import datetime
from calendar import monthrange
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from requests_data import recommendations_get, set_tariff_temp_profile

data_reservation = ['01.07', '02.07', '03.07', '04.07', '05.07', '06.07', '07.07', '08.07', '09.07', '10.07']
data_reservation_time = [
  ['8:10', '13:10', '18:10'],
  ['9:10', '14:10', '19:10'],
  ['10:10', '15:10', '20:10'],
  ['11:10', '16:10', '21:10'],
  ['12:10', '17:10', '22:10'],
]

categories = ['Образование', 'Финансы', 'Здоровье', 'Новости', 'IT', 'Досуг', 'Психология', 'Видео', 'Авторские', 'Другое']

def get_btns_categories():
  keyboard=[]
  for category in categories:
    keyboard.append([InlineKeyboardButton(category, callback_data='set-category_' + category)])
  return InlineKeyboardMarkup(keyboard)

def get_opt_create(chanel):
  keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='opt_create'), InlineKeyboardButton("Изменить", callback_data='opt_init_' + chanel)]]
  return InlineKeyboardMarkup(keyboard)

def get_reservation_table():
  keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='opt_save'), InlineKeyboardButton("Изменить", callback_data='opt_change')]]
  return InlineKeyboardMarkup(keyboard)


def check_morning(data, bookeds):
  result = " "
  for booked in bookeds:
    if (data in booked) and ("morning" in booked):
      result = "✅"
      break
  return result

def check_day(data, bookeds):
  result = " "
  for booked in bookeds:
    if (data in booked) and ("day" in booked):
      result = "✅"
      break
  return result

def check_evening(data, bookeds):
  result = " "
  for booked in bookeds:
    if (data in booked) and ("evening" in booked):
      result = "✅"
      break
  return result

def generate_date(offset = 0):
  dates = []
  current_datetime = datetime.now()
  month_now = current_datetime.month
  month = current_datetime.month
  day_now = current_datetime.day

  days_in_month = monthrange(current_datetime.year, current_datetime.month)[1]

  for index in range(10):
    day = day_now + index  + int(offset)
    if day >= days_in_month:
      month = month_now + 1
      day -= days_in_month
      day += 1
    dates.append(str(day) + '.' + str(month))
  return dates

def get_reservation_more_table(bookeds=[], offset = 0):
  dates = generate_date(offset)
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='empty'), InlineKeyboardButton("Утро", callback_data='empty'), InlineKeyboardButton("День", callback_data='empty'), InlineKeyboardButton("Вечер", callback_data='empty')])

  for data in dates:
    keyboard.append([InlineKeyboardButton(data, callback_data='empty'), InlineKeyboardButton(check_morning(data, bookeds) , callback_data='reservation_morning/' + data + "_" +str(offset)), InlineKeyboardButton(check_day(data, bookeds), callback_data='reservation_day/' + data + "_" +str(offset)), InlineKeyboardButton(check_evening(data, bookeds), callback_data='reservation_evening/' + data + "_" +str(offset))])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='reservation_more_' + str(offset)), InlineKeyboardButton("Потдвердить", callback_data='opt_confirm')])
  return InlineKeyboardMarkup(keyboard)

def get_reservation_time_table(bookeds=[]):
  keyboard = []
  keyboard.append([InlineKeyboardButton("Утро", callback_data='empty'), InlineKeyboardButton("День", callback_data='empty'), InlineKeyboardButton("Вечер", callback_data='empty')])
  for data_row in data_reservation_time:
    row = []
    for data in data_row:
      if data in bookeds:
        row.append(InlineKeyboardButton("✅ " +data, callback_data='time_' + data))
      else:
        row.append(InlineKeyboardButton(data, callback_data='time_' + data))
    keyboard.append(row)
  keyboard.append([InlineKeyboardButton("Потдвердить", callback_data='opt_time')])
  return InlineKeyboardMarkup(keyboard)

def get_btns_pay(mode, discount, user_id):
  keyboard = []
  days_three = 10 + discount
  year = 20 + discount
  
  if mode == 'lite':
    set_tariff_temp_profile(user_id, 'lite')
    prise_m = int(290 * ((100 - discount) / 100))
    prise_three_m = int((290 * 3) * ((100 - days_three) / 100))
    prise_y = int((290 * 12) * ((100 - year) / 100))
    keyboard = [
      [InlineKeyboardButton("Ввести промокод", callback_data='promocode_enter')],
      [InlineKeyboardButton("30 дней за "+ str(prise_m) +"₽ (" + str(discount) + "% скидка)", callback_data='pay_check_lite_litle_'+ str(prise_m))],
      [InlineKeyboardButton("90 дней за "+ str(prise_three_m) +"₽ (" + str(days_three) + "% скидка)", callback_data='pay_check_lite_middle_'+ str(prise_three_m))],
      [InlineKeyboardButton("365 дней за "+ str(prise_y) +"₽ (" + str(year) + "% скидка)", callback_data='pay_check_lite_big_'+ str(prise_y))],
    ]
  elif mode == 'pro':
    set_tariff_temp_profile(user_id, 'pro')
    prise_m = int(890 * ((100 - discount) / 100))
    prise_three_m = int((890 * 3) * ((100 - days_three) / 100))
    prise_y = int((890 * 12) * ((100 - year) / 100))
    keyboard = [
      [InlineKeyboardButton("Ввести промокод", callback_data='promocode_enter')],
      [InlineKeyboardButton("30 дней за "+ str(prise_m) +"₽ (" + str(discount) + "% скидка)", callback_data='pay_check_pro_litle_'+ str(prise_m))],
      [InlineKeyboardButton("90 дней за "+ str(prise_three_m) +"₽ (" + str(days_three) + "% скидка)", callback_data='pay_check_pro_middle_'+ str(prise_three_m))],
      [InlineKeyboardButton("365 дней за "+ str(prise_y) +"₽ (" + str(year) + "% скидка)", callback_data='pay_check_pro_big_'+ str(prise_y))],
    ]
  elif mode == 'business':
    set_tariff_temp_profile(user_id, 'business')
    prise_m = int(3890 * ((100 - discount) / 100))
    prise_three_m = int((3890 * 3) * ((100 - days_three) / 100))
    prise_y = int((3890 * 12) * ((100 - year) / 100))
    keyboard = [
      [InlineKeyboardButton("Ввести промокод", callback_data='promocode_enter')],
      [InlineKeyboardButton("30 дней за "+ str(prise_m) +"₽ (" + str(discount) + "% скидка)", callback_data='_'+ str(prise_m))],
      [InlineKeyboardButton("90 дней за "+ str(prise_three_m) +"₽ (" + str(days_three) + "% скидка)", callback_data='pay_check_business_middle_'+ str(prise_three_m))],
      [InlineKeyboardButton("365 дней за "+ str(prise_y) +"₽ (" + str(year) + "% скидка)", callback_data='pay_check_business_big_'+ str(prise_y))],
    ]
  return InlineKeyboardMarkup(keyboard)

def get_user_chanels(chanels_array):
  keyboard = []
  for chanel in chanels_array:
    keyboard.append([InlineKeyboardButton(chanel['title'], callback_data='opt_init_' + chanel['idChanel'])])
  return InlineKeyboardMarkup(keyboard)

def get_categories(category_type, start_cut, finish_cut, page, idUser, filter=""):
  categoriesBtns = []
  req = requests.get(
    'http://localhost:3001/chanel/categories' +
    '?category=' + category_type +
    '&filter=' + filter +
    '&idUser=' + str(idUser)
    )
  categoriesArray =  req.json()
  if len(categoriesArray) != 0:
    categoriesBtns = parse_categories(categoriesArray[start_cut-1:finish_cut], category_type, page)
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
  # return name + '_' + query
  return name + '_' + query

def check_filter(name, query):
  if name in query:
    return " ✅"
  return ""

def set_filters(query, check=""):
  keyboard = []
  keyboard = [
    # [InlineKeyboardButton("Фильтры", callback_data=query + '_static_0')],
    [InlineKeyboardButton("Количество подписчиков"+ check_filter('numberSubscribers', check), callback_data=query_parse('numberSubscribers', query))],
    [InlineKeyboardButton("Индекс цитирования"+ check_filter('indexSay', check), callback_data=query_parse('indexSay', query))],
    [InlineKeyboardButton("Сумарный дневной охват"+ check_filter('coverageDay', check), callback_data=query_parse('coverageDay', query))],
    [InlineKeyboardButton("Средний охват публикаций"+ check_filter('coveragePub', check), callback_data=query_parse('coveragePub', query))],
    [InlineKeyboardButton("Количнсвто репостов в другие каналы"+ check_filter('repost', check), callback_data=query_parse('repost', query))],
    # [InlineKeyboardButton("Рейтинг"+ check_filter('rating', check), callback_data=query_parse('rating', query))],
    # [InlineKeyboardButton("Охват"+ check_filter('coverage', check), callback_data=query_parse('coverage', query))],
    # [InlineKeyboardButton("Кол-во подписчиков"+ check_filter('numberSubscribers', check), callback_data=query_parse('numberSubscribers', query))],
    # [InlineKeyboardButton("Прирост за месяц"+ check_filter('growthMonth', check), callback_data=query_parse('growthMonth', query))],
    # [InlineKeyboardButton("Прирост за неделю"+ check_filter('growthWeek', check), callback_data=query_parse('growthWeek', query))],
    # [InlineKeyboardButton("Прирост за день"+ check_filter('growthDay', check), callback_data=query_parse('growthDay', query))],
    # [InlineKeyboardButton("Сначала новые"+ check_filter('new', check), callback_data=query_parse('new', query))],
    # [InlineKeyboardButton("Сначала старые"+ check_filter('old', check), callback_data=query_parse('old', query))],
    # [InlineKeyboardButton("Подтвержденные"+ check_filter('confirm', check), callback_data=query_parse('confirm', query))],
    [InlineKeyboardButton("Применить", callback_data='apply' + "_" + query + "_"+ check)]
  ]
  return InlineKeyboardMarkup(keyboard)

def set_filters_opt(query, check=""):
  keyboard = []
  keyboard = [
    # [InlineKeyboardButton("Фильтры", callback_data=query + '_static_0')],
    [InlineKeyboardButton("Количество подписчиков"+ check_filter('numberSubscribers', check), callback_data=query_parse('numberSubscribers', query))],
    [InlineKeyboardButton("Индекс цитирования"+ check_filter('indexSay', check), callback_data=query_parse('indexSay', query))],
    [InlineKeyboardButton("Сумарный дневной охват"+ check_filter('coverageDay', check), callback_data=query_parse('coverageDay', query))],
    [InlineKeyboardButton("Средний охват публикаций"+ check_filter('coveragePub', check), callback_data=query_parse('coveragePub', query))],
    [InlineKeyboardButton("Количнсвто репостов в другие каналы"+ check_filter('repost', check), callback_data=query_parse('repost', query))],
    # [InlineKeyboardButton("Рейтинг"+ check_filter('rating', check), callback_data=query_parse('rating', query))],
    # [InlineKeyboardButton("Охват"+ check_filter('coverage', check), callback_data=query_parse('coverage', query))],
    # [InlineKeyboardButton("Кол-во подписчиков"+ check_filter('numberSubscribers', check), callback_data=query_parse('numberSubscribers', query))],
    # [InlineKeyboardButton("Прирост за месяц"+ check_filter('growthMonth', check), callback_data=query_parse('growthMonth', query))],
    # [InlineKeyboardButton("Прирост за неделю"+ check_filter('growthWeek', check), callback_data=query_parse('growthWeek', query))],
    # [InlineKeyboardButton("Прирост за день"+ check_filter('growthDay', check), callback_data=query_parse('growthDay', query))],
    # [InlineKeyboardButton("Сначала новые"+ check_filter('new', check), callback_data=query_parse('new', query))],
    # [InlineKeyboardButton("Сначала старые"+ check_filter('old', check), callback_data=query_parse('old', query))],
    # [InlineKeyboardButton("Подтвержденные"+ check_filter('confirm', check), callback_data=query_parse('confirm', query))],
    [InlineKeyboardButton("Применить", callback_data='apply' + "_" + query + "_"+ check)]
  ]
  return InlineKeyboardMarkup(keyboard)


def user_get_btns_into(category_type, chanel):
  keyboard = [
    [InlineKeyboardButton("<<назад", callback_data='opt_into_'+ category_type +'_init')],
    [InlineKeyboardButton("Выбрать даты", callback_data='opt_into_'+ category_type +'_data_' + chanel)],
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

def go_into_opt_user():
  keyboard = [
    [InlineKeyboardButton("Все тематики", callback_data='opt_into_all_init')],
    [InlineKeyboardButton("Образование", callback_data='opt_into_Образование_init')],
    [InlineKeyboardButton("Финансы", callback_data='opt_into_Финансы_init')],
    [InlineKeyboardButton("Здоровье", callback_data='opt_into_Здоровье_init')],
    [InlineKeyboardButton("Новости", callback_data='opt_into_Новости_init')],
    [InlineKeyboardButton("IT", callback_data='opt_into_IT_init')],
    [InlineKeyboardButton("Досуг", callback_data='opt_into_Досуг_init')],
    [InlineKeyboardButton("Психология", callback_data='opt_into_Психология_init')],
    [InlineKeyboardButton("Видосики", callback_data='opt_into_Видосики_init')],
    [InlineKeyboardButton("Авторские", callback_data='opt_into_Авторские_init')],
    [InlineKeyboardButton("Другое", callback_data='opt_into_Другое_init')],
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
    categoriesBtns = parse_categories_opt(categoriesArray[start_cut-1:finish_cut], category_type, page)
  return categoriesBtns

def go_chanel_opt_into(category_type, start_cut, finish_cut, page, filter, idUser):
  categoriesBtns = []
  req = requests.get(
    'http://localhost:3001/opt/categories' +
    '?category=' + category_type +
    '&filter=' + filter +
    '&idUser=' + str(idUser)
    )
  categoriesArray =  req.json()
  categoriesBtns = parse_categories_opt_into(categoriesArray[start_cut-1:finish_cut], category_type, page)
  return categoriesBtns

def parse_categories_opt_into(categoriesArray, category_type, page):
  # arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='opt_into_'+ category_type +'_filters_' + category_type +'_'+ str(page))]]
  arrayBtns = []
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['chanel'], callback_data='opt_into_'+ category_type +'_old_' + category['chanel'] + '_' + category_type)])
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=('opt_into_' + category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=('opt_into_' + category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

def parse_categories_opt(categoriesArray, category_type, page):
  if len(categoriesArray) == 0:
    return False
  # arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='filters_' + category_type +'_'+ str(page))]]
  arrayBtns = []
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['chanel'], callback_data='opt_old_' + category['chanel'] + '_' + category_type)])
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=('opt_' + category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=('opt_' + category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

def parse_categories(categoriesArray, category_type, page):
  if len(categoriesArray) == 0:
    return False
  # arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='filters_' + category_type +'_'+ str(page))]]
  arrayBtns= []
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['username'] + ' ' + str(category['participants_count']), callback_data=category['username'] + '_' + category_type)])
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=(category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=(category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

def opt_reservation():
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='test'), InlineKeyboardButton("Утро", callback_data='test'), InlineKeyboardButton("День", callback_data='test'), InlineKeyboardButton("Вечер", callback_data='test')])
  for data in data_reservation:
    keyboard.append([InlineKeyboardButton(data, callback_data='test'), InlineKeyboardButton(" ", callback_data='opt_reservation_data_morning_' + data), InlineKeyboardButton(" ", callback_data='opt_reservation_day_' + data), InlineKeyboardButton(" ", callback_data='opt_reservation_evening_' + data)])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='test'), InlineKeyboardButton("Потдвердить", callback_data='opt_reservation_confirm')])
  return InlineKeyboardMarkup(keyboard)

def btns_recommendations_get(offset = 0):
  keyboard = []
  recommendations = recommendations_get()
  recommendations_filter = recommendations[offset: offset+10]
  for data in recommendations_filter:
    keyboard.append([InlineKeyboardButton(data['username'] +" "+ str(data['price_now']) + "тыс.₽", callback_data='watch_chanel_' + str(data['id']))])
  keyboard.append([InlineKeyboardButton("Назад", callback_data='watch_back_' + str(offset)), InlineKeyboardButton("Вперед", callback_data='watch_next_' + str(offset))])
  return InlineKeyboardMarkup(keyboard)



def check_morning_into(data, bookeds, allowed_dates):
  result = ["❌", False]
  for allowed in allowed_dates:
    if (data in allowed) and ("morning" in allowed):
      result[0] = " "
      result[1] = True
      for booked in bookeds:
        if (data in booked) and ("morning" in booked):
          result[0] = "✅"
          break

  return result

def check_day_into(data, bookeds, allowed_dates):
  result = ["❌", False]
  for allowed in allowed_dates:
    if (data in allowed) and ("day" in allowed):
      result[0] = " "
      result[1] = True
      for booked in bookeds:
        if (data in booked) and ("day" in booked):
          result[0] = "✅"
          break


  return result

def check_evening_into(data, bookeds, allowed_dates):
  result = ["❌", False]
  for allowed in allowed_dates:
    if (data in allowed) and ("evening" in allowed):
      result[0] = " "
      result[1] = True
      for booked in bookeds:
        if (data in booked) and ("evening" in booked):
          result[0] = "✅"
          break

  return result


# таблица для выбор дат вход в опт
def get_reservation_into_table(bookeds=[], offset = 0, channel="", allowed_dates=[]):
  # print(allowed_dates)
  dates = generate_date(offset)
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='empty'), InlineKeyboardButton("Утро", callback_data='empty'), InlineKeyboardButton("День", callback_data='empty'), InlineKeyboardButton("Вечер", callback_data='empty')])

  for data in dates:
    keyboard.append([InlineKeyboardButton(data, callback_data='empty'), InlineKeyboardButton(check_morning_into(data, bookeds, allowed_dates)[0] , callback_data='opt-into_' + channel + '_morning/' + data + "_" +str(offset) if check_morning_into(data, bookeds, allowed_dates)[1] else 'empty'), InlineKeyboardButton(check_day_into(data, bookeds, allowed_dates)[0], callback_data='opt-into_' + channel + '_day/' + data + "_" +str(offset) if check_day_into(data, bookeds, allowed_dates)[1] else 'empty'), InlineKeyboardButton(check_evening_into(data, bookeds, allowed_dates)[0], callback_data='opt-into_' + channel + '_evening/' + data + "_" +str(offset) if check_evening_into(data, bookeds, allowed_dates)[1] else 'empty')])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='opt-into_' + channel + '_more_' + str(offset)), InlineKeyboardButton("Потдвердить", callback_data='opt-into_' + channel + '_confirm')])
  keyboard.append([InlineKeyboardButton("Назад", callback_data='opt_into_all_init')])
  return InlineKeyboardMarkup(keyboard)


# таблица для выбор дат подборок
def get_reservation_req_table(bookeds=[], offset = 0, channel="", allowed_dates=[]):
  # print(allowed_dates)
  dates = generate_date(offset)
  keyboard = []
  keyboard.append([InlineKeyboardButton("Дата", callback_data='empty'), InlineKeyboardButton("Утро", callback_data='empty'), InlineKeyboardButton("День", callback_data='empty'), InlineKeyboardButton("Вечер", callback_data='empty')])

  for data in dates:
    keyboard.append([InlineKeyboardButton(data, callback_data='empty'), InlineKeyboardButton(check_morning_into(data, bookeds, allowed_dates)[0] , callback_data='watch_opt-into_' + channel + '_morning/' + data + "_" +str(offset) if check_morning_into(data, bookeds, allowed_dates)[1] else 'empty'), InlineKeyboardButton(check_day_into(data, bookeds, allowed_dates)[0], callback_data='watch_opt-into_' + channel + '_day/' + data + "_" +str(offset) if check_day_into(data, bookeds, allowed_dates)[1] else 'empty'), InlineKeyboardButton(check_evening_into(data, bookeds, allowed_dates)[0], callback_data='watch_opt-into_' + channel + '_evening/' + data + "_" +str(offset) if check_evening_into(data, bookeds, allowed_dates)[1] else 'empty')])
  keyboard.append([InlineKeyboardButton("Больше дат", callback_data='watch_opt-into_' + channel + '_more_' + str(offset)), InlineKeyboardButton("Потдвердить", callback_data='watch_opt-into_' + channel + '_confirm')])
  keyboard.append([InlineKeyboardButton("Назад", callback_data='watch_see')])
  return InlineKeyboardMarkup(keyboard)