from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from parse import get_text_for_post
from requests_data import (
    get_profile,
    set_opt_into,
    user_get_message_mod,
)


# ввод креативов опта
async def opt_creative(update: Update, context) -> None:
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)

    if mode == 'opt-creative-one':
        post = await get_text_for_post(update, context)
        profile = get_profile(user_id)
        opt_old = set_opt_into(user_id, profile['opt_into_temp'], {}, 'none')
        creatives = opt_old['creatives'] + '///' + post
        set_opt_into(user_id, profile['opt_into_temp'], {'creatives': creatives}, 'none')
        keyboard = [[InlineKeyboardButton("Добавить", callback_data='opt-creative-two'),
                     InlineKeyboardButton("Потдвердить", callback_data='opt-creative-accept')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
        return

    elif mode == 'opt-creative-two':
        post = await get_text_for_post(update, context)
        profile = get_profile(user_id)
        opt_old = set_opt_into(user_id, profile['opt_into_temp'], {}, 'none')
        creatives = opt_old['creatives'] + '///' + post
        set_opt_into(user_id, profile['opt_into_temp'], {'creatives': creatives}, 'none')
        keyboard = [[InlineKeyboardButton("Добавить", callback_data='opt-creative-three'),
                     InlineKeyboardButton("Потдвердить", callback_data='opt-creative-accept')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
        return

    elif mode == 'opt-creative-three':
        post = await get_text_for_post(update, context)
        profile = get_profile(user_id)
        opt_old = set_opt_into(user_id, profile['opt_into_temp'], {}, 'none')
        creatives = opt_old['creatives'] + '///' + post
        set_opt_into(user_id, profile['opt_into_temp'], {'creatives': creatives}, 'none')
        keyboard = [[InlineKeyboardButton("Добавить", callback_data='opt-creative-four'),
                     InlineKeyboardButton("Потдвердить", callback_data='opt-creative-accept')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
        return

    elif mode == 'opt-creative-four':
        post = await get_text_for_post(update, context)
        profile = get_profile(user_id)
        opt_old = set_opt_into(user_id, profile['opt_into_temp'], {}, 'none')
        creatives = opt_old['creatives'] + '///' + post
        set_opt_into(user_id, profile['opt_into_temp'], {'creatives': creatives}, 'none')
        keyboard = [[InlineKeyboardButton("Добавить", callback_data='opt-creative-five'),
                     InlineKeyboardButton("Потдвердить", callback_data='opt-creative-accept')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
        return

    elif mode == 'opt-creative-five':
        post = await get_text_for_post(update, context)
        profile = get_profile(user_id)
        opt_old = set_opt_into(user_id, profile['opt_into_temp'], {}, 'none')
        creatives = opt_old['creatives'] + '///' + post
        set_opt_into(user_id, profile['opt_into_temp'], {'creatives': creatives}, 'none')
        keyboard = [[InlineKeyboardButton("Потдвердить", callback_data='opt-creative-accept')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Хотите отправить креатив?:", reply_markup=reply_markup)
        return
