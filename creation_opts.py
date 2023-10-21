from datetime import datetime
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from requests_data import (
  opt_set,
  opt_get,
  get_profile,
  user_get_message_mod,
  user_change_message_mod,
  parse_view_date
)
from create_btns import (
  get_reservation_more_table,
  get_reservation_time_table,
  get_opt_create
)

# создание оптов
async def creation_opts(update: Update, _) -> None:
  user_id = update.message.chat.id
  mode = user_get_message_mod(user_id)

  if mode == 'opt-retail-price':
    try:
      retail_price = int(update.message.text)
      data = {'retail_price': retail_price}
      opt_set(user_id, data)
      user_change_message_mod(user_id, 'opt-wholesale-cost')
      await update.message.reply_text("Напишите текущую(оптовую) стоимость размещения. Разница с розничной должна быть не менее 10%:")
    except:
      await update.message.reply_text("вы ввели неверные данные, повторите ввод")
    return
  elif mode == 'opt-wholesale-cost':
    try:
      profile = get_profile(user_id)
      opt = opt_get(user_id)
      wholesale_cost = int(update.message.text)

      if int(opt['retail_price']) * 0.9 < wholesale_cost:
        await update.message.reply_text("Неверная оптовая стоимость. Разница с розничной должна быть не менее 10%:")
        return
      data = {'wholesale_cost': wholesale_cost}
      opt_set(user_id, data)
      user_change_message_mod(user_id, 'opt-minimum-permissible-value')
      await update.message.reply_text("Введите минимальное количество мест, необходимое для оформления опта(от 3 до 10):")
    except:
      await update.message.reply_text("вы ввели неверные данные, повторите ввод")
    return
  elif mode == 'opt-minimum-permissible-value':
    try:
      opt_minimum = int(update.message.text)
      if opt_minimum >= 3 and opt_minimum <= 10:
        data = {'min_places': str(opt_minimum)}
        opt_set(user_id, data)
        user_change_message_mod(user_id, 'opt-maximum-permissible-value')
        profile = get_profile(user_id)
        tariff_plan = profile['tariffPlan']
        maximum = ''
        if tariff_plan == 'lite':
          maximum = '10'
        elif tariff_plan == 'pro':
          maximum = '20'
        elif tariff_plan == 'business':
          maximum = '30'
        await update.message.reply_text("Введите максимальное допустимое количество мест в опте(до "+maximum+"):")
      else:
        await update.message.reply_text("вы ввели неверные данные, повторите ввод")
    except:
      await update.message.reply_text("вы ввели неверные данные, повторите ввод")
    return
  elif mode == 'opt-maximum-permissible-value':
    try:
      profile = get_profile(user_id)
      tariff_plan = profile['tariffPlan']
      maximum = 0
      if tariff_plan == 'lite':
        maximum = 10
      elif tariff_plan == 'pro':
        maximum = 20
      elif tariff_plan == 'business':
        maximum = 30
      opt_maximum = int(update.message.text)
      opt_old = opt_set(user_id, {})
      mini = opt_old['min_places']
      if opt_maximum > maximum:
        await update.message.reply_text("Выв ввели число мест больше вашего лимита: "+str(maximum)+" введите повторно")
        return
      elif opt_maximum < int(mini):
        await update.message.reply_text("Выв ввели число мест меньше вашего лимита: "+str(mini)+" введите повторно")
        return
      data = {'max_places': str(opt_maximum)}
      opt_set(user_id, data)
      user_change_message_mod(user_id, 'opt-available-reservation')
      reply_markup = get_reservation_more_table()
      await update.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
    except:
      await update.message.reply_text("вы ввели неверные данные, повторите ввод")
    return
  elif mode == 'opt-available-reservation':
    opt = opt_set(user_id, {})

    bookeds = []
    if opt != None:
      if isinstance(opt['booking_date'], str):
        bookeds = opt['booking_date'].split('_')
      
    reply_markup = get_reservation_more_table(bookeds)
    await update.message.reply_text('Выберите доступные для брони слоты:', reply_markup=reply_markup)
    return
  elif mode == 'deadline-wholesale-formation':
    opt = opt_get(user_id)
    booking_date = opt['booking_date']
    booking_date = booking_date.split('_')
    booking_date = list(map(lambda x: time.strptime(x.split('/')[1], '%d.%m'), booking_date))
    date_max = max(booking_date)
    date_min = min(booking_date)

    deadline_date = update.message.text
    try:
      valid_date = time.strptime(deadline_date, '%d.%m')
    except:
      await update.message.reply_text('Вы ввели некоректные данные, повторите ввод:')
      return

    if valid_date > date_max:
      await update.message.reply_text('Вы ввели дату больше крайней даты брони, повторите ввод:')
      return
    elif valid_date < date_min:
      await update.message.reply_text('Вы ввели дату меньшей крайней даты брони, повторите ввод:')
      return
    data = {'deadline_date': deadline_date}
    opt_set(user_id, data)
    reply_markup = get_reservation_time_table()
    await update.message.reply_text('Выберите допустимое время размещений:', reply_markup=reply_markup)
    return
  elif mode == 'opt-send-details':
    try:
      requisites = update.message.text
      data = {'requisites': requisites}
      opt = opt_set(user_id, data)
      reply_markup = get_opt_create(opt['chanel'])
      booking_date = opt['booking_date'].split('_')
      booking_date_parse = parse_view_date(booking_date)
      current_datetime = datetime.now()
      month_now = current_datetime.month
      day_now = current_datetime.day
      date = str(day_now) + '.' + str(month_now)
      first_name = update.message.chat.first_name
      username = update.message.chat.username
      await update.message.reply_text('''
Опт от '''+ date +''' в канале ['''+opt['title']+'''](https://t.me/'''+opt['chanel'][1:]+''')\n
*Розничная цена:* '''+ str(opt['retail_price']) + ''' \n
*Оптовая цена:* '''+ str(opt['wholesale_cost']) + '''\n
*Минимум постов:* '''+ str(opt['min_places']) + '''\n
*Максимум постов:* '''+ str(opt['max_places']) + '''\n
*Список дат:* \n'''+ booking_date_parse + '''\n
*Дедлайн:* '''+ opt['deadline_date'] + '''\n
*Реквизиты:* '''+ opt['requisites'] + '''\n
*Владелец:* ['''+first_name+'''](https://t.me/'''+username+''')'''
      ,
      reply_markup=reply_markup,
      parse_mode="Markdown",
      disable_web_page_preview=None
    )
    except:
      await update.message.reply_text("Упс произошла ошибка")
    return