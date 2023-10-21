from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from parse import get_text_for_post
from requests_data import (
  get_profile,
  set_opt_recommendation_into,
  user_get_message_mod,
)

# ввод креативов подборок
async def recommendation_creative(update: Update, context) -> None:
  user_id = update.message.chat.id
  mode = user_get_message_mod(user_id)

  if mode == 'recommendation-creative-one':
    post = await get_text_for_post(update, context)
    profile = get_profile(user_id)
    opt_old = set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {}, 'none')
    creatives = opt_old['creatives'] + '///' + post
    set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {'creatives': creatives}, 'none')
    keyboard = [[InlineKeyboardButton("Добавить", callback_data='recommendation-creative-two'), InlineKeyboardButton("Потдвердить", callback_data='recommendation-creative-accept')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
    return
  
  elif mode == 'recommendation-creative-two':
    post = await get_text_for_post(update, context)
    profile = get_profile(user_id)
    opt_old = set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {}, 'none')
    creatives = opt_old['creatives'] + '///' + post
    set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {'creatives': creatives}, 'none')
    keyboard = [[InlineKeyboardButton("Добавить", callback_data='recommendation-creative-three'), InlineKeyboardButton("Потдвердить", callback_data='recommendation-creative-accept')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
    return
  
  elif mode == 'recommendation-creative-three':
    post = await get_text_for_post(update, context)
    profile = get_profile(user_id)
    opt_old = set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {}, 'none')
    creatives = opt_old['creatives'] + '///' + post
    set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {'creatives': creatives}, 'none')
    keyboard = [[InlineKeyboardButton("Добавить", callback_data='recommendation-creative-four'), InlineKeyboardButton("Потдвердить", callback_data='recommendation-creative-accept')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
    return
  
  elif mode == 'recommendation-creative-four':
    post = await get_text_for_post(update, context)
    profile = get_profile(user_id)
    opt_old = set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {}, 'none')
    creatives = opt_old['creatives'] + '///' + post
    set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {'creatives': creatives}, 'none')
    keyboard = [[InlineKeyboardButton("Добавить", callback_data='recommendation-creative-five'), InlineKeyboardButton("Потдвердить", callback_data='recommendation-creative-accept')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
    return
  
  elif mode == 'recommendation-creative-five':
    post = await get_text_for_post(update, context)
    profile = get_profile(user_id)
    opt_old = set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {}, 'none')
    creatives = opt_old['creatives'] + '///' + post
    set_opt_recommendation_into(user_id, profile['rec_into_temp'],  {'creatives': creatives}, 'none')
    keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='recommendation-creative-accept')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
    return