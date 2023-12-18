from telegram import InlineKeyboardButton


def day_time_choice_keyboard(disabled_values=None):
    print('day_time_choice_keyboard')
    print(disabled_values)
    keyboard = [
        [
            InlineKeyboardButton("Утро", callback_data='empty'),
            InlineKeyboardButton("День", callback_data='empty'),
            InlineKeyboardButton("Вечер", callback_data='empty'),
        ]
    ]
    for i in range(8, 13):
        keyboard_row = []
        for j in range(0, 3):
            hour = i + j * 5
            time_value = f'{hour}.10'
            callback_data = 'empty' if time_value in disabled_values else time_value
            button_text = '❌ ' if time_value in disabled_values else ''
            button_text += f'{hour}:10'
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    keyboard.append([
        InlineKeyboardButton("Подтвердить", callback_data='confirm'),
    ])

    return keyboard