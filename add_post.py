from telegram import Update

from parse import get_text_for_post
from requests_data import (
  user_get_message_mod,
  add_new_post,
  user_change_message_mod
)


# ввод креативов опта
async def add_post(update: Update, context) -> None:
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)

    if mode == 'add-post':
        post = await get_text_for_post(update, context)
        add_new_post(user_id, {'creatives': post})
        user_change_message_mod(user_id, 'standart')
        await update.message.reply_text("Ваш пост добавлен!")
        return
