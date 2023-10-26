    # отправка чеков владельцу опта и подборок
    # if mode == 'recommendation-check':
    #   user_id = update.message.chat.id
    #   mode = user_get_message_mod(user_id)
    #   file_id = update.message.photo[-1].file_id
    #   profile = get_profile(user_id)

    #   file_info = await context.bot.get_file(file_id)
    #   file_path = file_info.file_path
    #   recommendation_set_check(user_id, profile['rec_into_temp'], file_id, file_path)
    #   await update.message.reply_text('Чек придет владельцу опта')
    #   user_change_message_mod(user_id, 'standart')
#     if mode == 'opt-check':
#       user_id = update.message.chat.id
#       mode = user_get_message_mod(user_id)
#       # file_id = update.message.photo[-1].file_id
#       profile = get_profile(user_id)

#       # file_info = await context.bot.get_file(file_id)
#       # file_path = file_info.file_path
#       # opt_set_check(user_id, profile['rec_into_temp'], file_id, file_path)
  
#       # await update.message.reply_text('Чек придет владельцу опта')
#       user_change_message_mod(user_id, 'standart')


#       try:
#         requisites = update.message.text
#         data = {'requisites': requisites}
#         opt = opt_set(user_id, data)
#         reply_markup = get_opt_create(opt['chanel'])
#         booking_date = opt['booking_date'].split('_')
#         booking_date_parse = parse_view_date(booking_date)
#         current_datetime = datetime.now()
#         month_now = current_datetime.month
#         day_now = current_datetime.day
#         date = str(day_now) + '.' + str(month_now)
#         first_name = update.message.chat.first_name
#         username = update.message.chat.username
#         await update.message.reply_text('''
# Опт от '''+ date +''' в канале ['''+opt['title']+'''](https://t.me/'''+opt['chanel'][1:]+''')\n
# *Розничная цена:* '''+ str(opt['retail_price']) + ''' \n
# *Оптовая цена:* '''+ str(opt['wholesale_cost']) + '''\n
# *Минимум постов:* '''+ str(opt['min_places']) + '''\n
# *Максимум постов:* '''+ str(opt['max_places']) + '''\n
# *Список дат:* \n'''+ booking_date_parse + '''\n
# *Дедлайн:* '''+ opt['deadline_date'] + '''\n
# *Реквизиты:* '''+ opt['requisites'] + '''\n
# *Владелец:* ['''+first_name+'''](https://t.me/'''+username+''')'''
#         ,
#         reply_markup=reply_markup,
#         parse_mode="Markdown",
#         disable_web_page_preview=None
#       )
#       except:
#         await update.message.reply_text("Упс произошла ошибка")
#       return



  # async def handler_catalog(self, update: Update, _) -> None:
  #   user_stat = user_check(update.message.chat.id)
  #   if user_stat == 'empty':
  #     await update.message.reply_text('''*Сначала создайте профиль*\n\nЧтобы начать использовать бота, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n\nДругие полезные команды:\n/partners — сгенерировать уникальный промокод, чтобы вы могли приглашать других пользователей и получать бонусы\n/help — связь со службой поддержки и ответы на часто задаваемые вопросы''', parse_mode="Markdown")
  #   else:
  #     reply_markup = set_catalog()
  #     await update.message.reply_text('Выберите тематику:',reply_markup=reply_markup)