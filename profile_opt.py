import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from requests_data import (
  opt_post_delete,
  user_recommendation_into,
  user_opt_into,
  parse_view_date
)
from create_btns import (
  get_user_chanels,
  go_into_opt_user
)


# в оптах в которых участвуешь
async def profile_opt(update: Update, context) -> None:
  query = update.callback_query
  query_array = query.data.split('_')
  user_id = query.message.chat.id

  if query_array[0] == 'my-opt-into':
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    opts_str = ''
    keyboard = []
    for opt in opts:
      keyboard.append([
        InlineKeyboardButton(opt['chanel'], callback_data='empty'),
        InlineKeyboardButton('Посты', callback_data='my-opt-into-post_' + opt['chanel']),
        InlineKeyboardButton('Чек', callback_data='my-opt-into-check_' + opt['chanel']),
        InlineKeyboardButton('Даты брони', callback_data='my-opt-into-date_' + opt['chanel'])
      ])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('В подборках в которых учавствуешь\n' + opts_str, reply_markup=reply_markup)

  elif query_array[0] == 'my-opt-into-date':
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    user_array = query_array[1:]
    chanel = ''
    if len(user_array) > 1:
      chanel = '_'.join(user_array)
    else:
      chanel = query_array[1]
    keyboard = [[InlineKeyboardButton("Назад", callback_data='my-profile')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    for opt in opts:
      if opt['chanel'] == chanel:
        booking_date =  parse_view_date(opt['booking_date'].split('_'))
        await query.edit_message_text(booking_date, reply_markup=reply_markup)
        return
    await query.edit_message_text('Упс :( что-то пошло не так')

  elif query_array[0] == 'my-opt-into-check':
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    user_array = query_array[1:]
    chanel = ''
    if len(user_array) > 1:
      chanel = '_'.join(user_array)
    else:
      chanel = query_array[1]
    keyboard = []
    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    for opt in opts:
      if opt['chanel'] == chanel:
        check =  opt['check']
        await query.answer()
        await context.bot.send_photo(caption="Ваш чек: ", chat_id=query.message.chat.id, photo=check, reply_markup=reply_markup)
        return
    await query.edit_message_text('Упс :( что-то пошло не так')

  elif query_array[0] == 'my-opt-into-post':
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    user_array = query_array[1:]
    chanel = ''
    if len(user_array) > 1:
      chanel = '_'.join(user_array)
    else:
      chanel = query_array[1]
    keyboard = []
    for opt in opts:
      if opt['chanel'] == chanel:
        creatives =  opt['creatives'].split('///')
        for i, v in enumerate(creatives):
          if i == 0:
            continue
          keyboard.append([InlineKeyboardButton("Пост № " + str(i), callback_data='my-opt-into-post-number_' + str(i) + '_' + chanel)])
        
    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Посты:', reply_markup=reply_markup)

  elif query_array[0] == 'my-opt-into-post-number':
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    user_array = query_array[2:]
    post_number = query_array[1]
    chanel = ''
    if len(user_array) > 1:
      chanel = '_'.join(user_array)
    else:
      chanel = query_array[2]
    for opt in opts:
      if opt['chanel'] == chanel:
        creatives =  opt['creatives'].split('///')
        for i, v in enumerate(creatives):
          if i == int(post_number):
            print(v)
            textArray = v.split('*')
            await query.answer()
            keyboard = [
              [InlineKeyboardButton("Удалить ❌", callback_data='my-opt-into-post-delete_' + str(i) + '_' + chanel + '_' + opt['type'])],
              # [InlineKeyboardButton("Редактировать ✍️", callback_data='my-opt-into-post-edit_' + str(i) + '_' + chanel + '_' + opt['type'])],
              [InlineKeyboardButton("Назад", callback_data='my-profile')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if len(textArray) == 1:
              print(v)
              await query.message.reply_text(v, reply_markup=reply_markup, parse_mode="HTML")
            else:
              text = textArray[0]
              file_id, file_type = textArray[1].split('%')
              if file_type == 'photo':
                await context.bot.send_photo(caption=text, chat_id=query.message.chat.id, photo=file_id, reply_markup=reply_markup, parse_mode="HTML")
              elif file_type == 'video':
                await context.bot.send_video(caption=text, chat_id=query.message.chat.id, video=file_id, reply_markup=reply_markup, parse_mode="HTML")
              elif file_type == 'animation':
                await context.bot.send_animation(caption=text, chat_id=query.message.chat.id, animation=file_id, reply_markup=reply_markup, parse_mode="HTML")
            return
        
    await query.edit_message_text('Упс какая-то ошибка :(', reply_markup=reply_markup)

  elif query_array[0] == 'my-opt-into-post-delete':
    user_array = query_array[2:-1]
    post_id = query_array[1]
    opt_type = query_array[-1]
    chanel = ''
    if len(user_array) > 1:
      chanel = '_'.join(user_array)
    else:
      chanel = query_array[2]
    keyboard = []
    opt_post_delete(user_id, chanel, opt_type, post_id)
    recommendations_into = user_recommendation_into(user_id)
    opts_into = user_opt_into(user_id)
    opts = [*recommendations_into, *opts_into]
    for opt in opts:
      if opt['chanel'] == chanel:
        creatives =  opt['creatives'].split('///')
        for i, v in enumerate(creatives):
          if i == 0:
            continue
          keyboard.append([InlineKeyboardButton("Пост № " + str(i), callback_data='my-opt-into-post-number_' + str(i) + '_' + chanel)])
        
    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.message.reply_text('Посты:', reply_markup=reply_markup)

  # elif query_array[0] == 'my-opt-into-post-edit':
  #   await query.message.reply_text('Введите:', reply_markup=reply_markup)