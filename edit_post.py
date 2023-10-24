from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from parse import get_text_for_post
from requests_data import (
  edit_check_req,
  get_profile,
  edit_post_req,
  set_opt_recommendation_into,
  user_change_message_mod,
  user_get_message_mod,
)


async def edit_post(update: Update, context) -> None:
  user_id = update.message.chat.id
  mode = user_get_message_mod(user_id)
  
  #принять редактор пост
  if mode == 'edit-post':
    post = await get_text_for_post(update, context)
    edit_post_req(user_id, {'post': post})
    user_change_message_mod(user_id, 'standart')
    await update.message.reply_text("Ваш пост упешно отредактирован!")
    return
  
  #принять редактор пост
  if mode == 'edit-chek':
    check = update.message.photo[-1].file_id
    edit_check_req(user_id, check)
    user_change_message_mod(user_id, 'standart')
    await update.message.reply_text("Ваш чек упешно сохранён!")
    return