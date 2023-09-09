import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_categories(category_type, start_cut, finish_cut, page):
  categoriesBtns = []
  req = requests.get(
    'http://localhost:3001/category' +
    '?category=' + category_type
    )
  categoriesArray =  req.json()
  if len(categoriesArray) != 0:
    categoriesBtns = parseCategories(categoriesArray[start_cut:finish_cut], category_type, page)
  return categoriesBtns

def parseCategories(categoriesArray, category_type, page):
  if len(categoriesArray) == 0:
    return 'каналов по запросу нет'
  arrayBtns = [[InlineKeyboardButton('Фильтры', callback_data='filters_' + category_type +'_'+ str(page))]]
  for category in categoriesArray:
    arrayBtns.append([InlineKeyboardButton(category['username'], callback_data=category['username'])])
    # output += category['username'] + ' количество подписчиков: ' + str(category['participants_count']) + ' суммарный дневной охват: ' + str(category['daily_reach']) + ' количнсвто репостов в другие каналы: ' + str(category['forwards_count']) + '\n'
  arrayBtns.append([InlineKeyboardButton('<<Назад', callback_data=(category_type +'_back_' + str(page))), InlineKeyboardButton('Далее>>', callback_data=(category_type +'_next_' + str(page)))])
  return InlineKeyboardMarkup(arrayBtns)

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