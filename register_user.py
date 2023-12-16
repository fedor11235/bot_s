from telegram import Update

from create_btns import (
    get_btns_categories,
    get_btns_pay
)
from requests_data import (
    get_profile,
    upload_promocode,
    user_check,
    user_change_message_mod,
    create_chanel,
    user_get_message_mod
)


async def add_chanel(update: Update, context):
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)
    if mode == 'chanel':
        status = ''
        try:
            if update.message.forward_from_chat:
                idChanel = update.message.forward_from_chat.id
                await context.bot.get_chat_member(user_id=6569483795, chat_id=str(idChanel))
                chat_info = await context.bot.get_chat(chat_id=idChanel)

                status = create_chanel(user_id, idChanel, chat_info.title)

                if status == 'exist':
                    await update.message.reply_text('Такой канал уже добавлен')
                    return
                elif status == 'created':
                    reply_markup = get_btns_categories()
                    await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
                    # user_change_message_mod(update.message.chat.id, 'type-chanel')
                    return
            else:
                text = update.message.text
                if 'https' in text:
                    username = '@' + text.split('/')[-1]
                    try:
                        await context.bot.get_chat_member(user_id=6569483795, chat_id=username)
                        chat_info = await context.bot.get_chat(chat_id=username)

                        status = create_chanel(user_id, username, chat_info.title)

                    except:
                        await update.message.reply_text(
                            'Бот не принимает ссылки на частные каналы и чаты. Отправьте @username или ID канала, или просто перешлите любое сообщение из него прямо сюда.')
                        user_change_message_mod(update.message.chat.id, 'standart')
                        return
                else:
                    await context.bot.get_chat_member(user_id=6569483795, chat_id=text)
                    chat_info = await context.bot.get_chat(chat_id=text)
                    status = create_chanel(user_id, text, chat_info.title)

            if status == 'exist':
                await update.message.reply_text('Такой канал уже добавлен')
                user_change_message_mod(update.message.chat.id, 'standart')
                return
            elif status == 'created':
                reply_markup = get_btns_categories()
                await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
                # user_change_message_mod(update.message.chat.id, 'type-chanel')
                return
            user_change_message_mod(update.message.chat.id, 'standart')

        except:
            user_change_message_mod(update.message.chat.id, 'standart')
            await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
            return


async def register_user(update: Update, context):
    user_id = update.message.chat.id
    user_stat = user_check(user_id)
    if user_stat == 'empty':
        status = ''
        try:
            if update.message.forward_from_chat:
                idChanel = update.message.forward_from_chat.id
                await context.bot.get_chat_member(user_id=6569483795, chat_id=str(idChanel))

                chat_info = await context.bot.get_chat(chat_id=idChanel)
                status = create_chanel(user_id, idChanel, chat_info.title, update.message.from_user.username)
            else:
                if 'https' in update.message.text:
                    username = '@' + update.message.text.split('/')[-1]

                    try:
                        await context.bot.get_chat_member(user_id=6569483795, chat_id=username)
                        chat_info = await context.bot.get_chat(chat_id=username)
                        status = create_chanel(user_id, username, chat_info.title, update.message.from_user.username)

                    except:
                        await update.message.reply_text(
                            'Бот не принимает ссылки на частные каналы и чаты. Отправьте @username или ID канала, или просто перешлите любое сообщение из него прямо сюда.')
                        user_change_message_mod(update.message.chat.id, 'standart')
                        return
                else:
                    await context.bot.get_chat_member(user_id=6569483795, chat_id=update.message.text)
                    chat_info = await context.bot.get_chat(chat_id=update.message.text)
                    status = create_chanel(user_id, update.message.text, chat_info.title,
                                           update.message.from_user.username)
            if status == "created":
                reply_markup = get_btns_categories()
                await update.message.reply_text('Введите категорию канала: ', reply_markup=reply_markup)
            else:
                await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
        except:
            await update.message.reply_text('Не верные введенные данные, либо вы не добавили бота в канал')
    return


async def user_promocode(update: Update, context):
    user_id = update.message.chat.id
    mode = user_get_message_mod(user_id)
    if mode == 'promocode':
        promocode = update.message.text
        user_change_message_mod(update.message.chat.id, 'standart')
        res = upload_promocode(user_id, promocode)
        profile = get_profile(user_id)
        reply_markup = get_btns_pay(profile['tariffPlan_temp'], profile['discount'], user_id)
        if res == 'not-exist':
            await update.message.reply_text(text='Такого промокода не существует')
        elif res == 'expired':
            await update.message.reply_text(text='Просроченный промокод')
        elif res == 'owner':
            await update.message.reply_text(text='Вы являетесь владельцем промокода')
        await update.message.reply_text(
            text='Выберите срок на который хотите продлить подписку *' + profile['tariffPlan_temp'].title() + '*:\n',
            reply_markup=reply_markup, parse_mode="Markdown")
        return
