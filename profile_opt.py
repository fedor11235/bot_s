from functools import reduce
from requests_data import (
    # get_release_schedule,
    get_profile,
    save_eddit_temp_check,
    save_eddit_temp_post,
    user_change_message_mod,
    opt_post_delete,
    user_recommendation_into,
    user_opt_into,
    parse_view_date
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from requests_data import (
    # get_release_schedule,
    get_profile,
    save_eddit_temp_check,
    save_eddit_temp_post,
    user_change_message_mod,
    opt_post_delete,
    user_recommendation_into,
    user_opt_into,
    parse_view_date
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
            print(opt)

            keyboard.append([
                InlineKeyboardButton(str(opt['title']), callback_data='empty'),
                InlineKeyboardButton('Посты', callback_data='my-opt-into-post_' + opt['chanel']),
                InlineKeyboardButton('Чек', callback_data='my-opt-into-check_' + opt['chanel']),
                InlineKeyboardButton('Даты брони', callback_data='my-opt-into-date_' + opt['chanel'])
            ])
        keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('Актуальные опты с вашим участием:\n' + opts_str, reply_markup=reply_markup)

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
        keyboard = [[InlineKeyboardButton("Назад", callback_data='my-opt-into')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        for opt in opts:
            if opt['chanel'] == chanel:
                booking_date = parse_view_date(opt['booking_date'].split('_'))
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
        for opt in opts:
            if opt['chanel'] == chanel:
                check = opt['check']
                if check:
                    keyboard.append([InlineKeyboardButton("Редактировать ✍️",
                                                          callback_data='my-opt-into-chek-edit_' + chanel + '_' + opt[
                                                              'type'])])
                    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-into')])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await query.answer()
                    await context.bot.send_photo(caption="Ваш чек ", chat_id=query.message.chat.id, photo=check,
                                                 reply_markup=reply_markup)
                else:
                    keyboard.append([InlineKeyboardButton("Добавить ✍️",
                                                          callback_data='my-opt-into-chek-edit_' + chanel + '_' + opt[
                                                              'type'])])
                    keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-into')])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await query.edit_message_text('У вас нет чеков, хотите добавить?', reply_markup=reply_markup)
                return
        await query.edit_message_text('Упс, что-то пошло не так :(')

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
        opt_type = ''
        for opt in opts:
            if opt['chanel'] == chanel:
                opt_type = opt['type']
                creatives = opt['creatives'].split('///')
                for i, v in enumerate(creatives):
                    if i == 0:
                        continue
                    keyboard.append([InlineKeyboardButton("Пост № " + str(i),
                                                          callback_data='my-opt-into-post-number_' + str(
                                                              i) + '_' + chanel)])
        keyboard.append(
            [InlineKeyboardButton("Добавить пост ➕", callback_data='my-opt-into-post-add_' + chanel + '_' + opt_type)])
        keyboard.append([InlineKeyboardButton("Назад", callback_data='my-opt-into')])
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
                creatives = opt['creatives'].split('///')
                for i, v in enumerate(creatives):
                    if i == int(post_number):
                        textArray = v.split('*')
                        await query.answer()
                        keyboard = [
                            [InlineKeyboardButton("Удалить ❌", callback_data='my-opt-into-post-delete_' + str(
                                i) + '_' + chanel + '_' + opt['type'])],
                            [InlineKeyboardButton("Редактировать ✍️",
                                                  callback_data='my-opt-into-post-edit_' + str(i) + '_' + chanel + '_' +
                                                                opt['type'])],
                            [InlineKeyboardButton("Назад", callback_data='my-profile')]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        if len(textArray) == 1:
                            await query.message.reply_text(v, reply_markup=reply_markup, parse_mode="HTML")
                        else:
                            text = textArray[0]
                            file_id, file_type = textArray[1].split('%')
                            if file_type == 'photo':
                                await context.bot.send_photo(caption=text, chat_id=query.message.chat.id, photo=file_id,
                                                             reply_markup=reply_markup, parse_mode="HTML")
                            elif file_type == 'video':
                                await context.bot.send_video(caption=text, chat_id=query.message.chat.id, video=file_id,
                                                             reply_markup=reply_markup, parse_mode="HTML")
                            elif file_type == 'animation':
                                await context.bot.send_animation(caption=text, chat_id=query.message.chat.id,
                                                                 animation=file_id, reply_markup=reply_markup,
                                                                 parse_mode="HTML")
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
        opt_type = ''
        for opt in opts:
            if opt['chanel'] == chanel:
                opt_type = opt['type']
                creatives = opt['creatives'].split('///')
                for i, v in enumerate(creatives):
                    if i == 0:
                        continue
                    keyboard.append([InlineKeyboardButton("Пост № " + str(i),
                                                          callback_data='my-opt-into-post-number_' + str(
                                                              i) + '_' + chanel)])
        keyboard.append(
            [InlineKeyboardButton("Добавить пост ➕", callback_data='my-opt-into-post-add_' + chanel + '_' + opt_type)])
        keyboard.append([InlineKeyboardButton("Назад", callback_data='my-profile')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.message.reply_text('Посты:', reply_markup=reply_markup)

    elif query_array[0] == 'my-opt-into-post-edit':
        user_array = query_array[2:-1]
        post_number = query_array[1]
        opt_type = query_array[-1]
        chanel = ''
        if len(user_array) > 1:
            chanel = '_'.join(user_array)
        else:
            chanel = query_array[2]
        user_change_message_mod(user_id, 'edit-post')
        save_eddit_temp_post(user_id, chanel, opt_type, post_number)
        await query.message.reply_text('Введите новый пост:')

    elif query_array[0] == 'my-opt-into-chek-edit':
        user_array = query_array[1:-1]
        opt_type = query_array[-1]
        chanel = ''
        if len(user_array) > 1:
            chanel = '_'.join(user_array)
        else:
            chanel = query_array[1]
        user_change_message_mod(user_id, 'edit-chek')
        save_eddit_temp_check(user_id, chanel, opt_type)
        await query.answer()
        await query.message.reply_text('Отправьте чек')

    elif query_array[0] == 'my-opt-into-post-add':
        user_array = query_array[1:-1]
        opt_type = query_array[-1]
        chanel = ''
        if len(user_array) > 1:
            chanel = '_'.join(user_array)
        else:
            chanel = query_array[1]
        save_eddit_temp_check(user_id, chanel, opt_type)
        user_change_message_mod(user_id, 'add-post')
        await query.answer()
        await query.message.reply_text('Введите новый пост:')

    elif query_array[0] == 'my-chanel':
        keyboard = [[InlineKeyboardButton("Добавить канал", callback_data='add-channel')],
                    [InlineKeyboardButton("Назад", callback_data='my-profile')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        profile = get_profile(user_id)
        channels = profile['channels']
        text = ''
        for channel in channels:
            text += channel['title'] + '  ' + channel['idChanel'] + '\n'

        await query.answer()
        await query.message.edit_text(text, reply_markup=reply_markup)

    elif query_array[0] == 'add-channel':
        user_change_message_mod(user_id, 'chanel')
        await query.answer()
        await query.message.reply_text(
            '''Чтобы добавить канал, сделайте @SlonRobot администратором в канале, а затем пришлите сюда ссылку на канал или просто перешлите из него любое сообщение.\n\nБоту можно не выдавать никаких прав. Данная процедура нужна чтобы подтвердить, что вы являетесь владельцем канала.\n''')

    elif query_array[0] == 'release-schedule':
        text = ''
        await query.answer()
        recommendations_into = user_recommendation_into(user_id)
        opts_into = user_opt_into(user_id)
        opts = [*recommendations_into, *opts_into]
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='my-profile')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # opts = user_opt(user_id)
        for opt in opts:
            date_str = ''
            date_array = opt['booking_date'].split('_')
            time_array = opt['booking_time'].split('_')
            print(opt['booking_date'])
            print(date_array)
            for date in date_array:
                if date != '':
                  date_str += ' ' + date.split('/')[1]

            text += date_str + ' ' + opt['chanel'] + ' ' +' '.join(time_array) + '\n'
            # text += ' '.join(opt['booking_date'].split('_')) + ' ' + opt['chanel'] + ' ' + ' '.join(opt['placement_time'].split('_')) + '\n'
        if not text:
            text = 'Нету вхождений в опты'
        await query.message.edit_text(text, reply_markup=reply_markup)
