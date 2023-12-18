from telegram import InlineKeyboardButton


def day_time_choice_keyboard():
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
            button_text = f'{hour}:10'
            callback_data = f'{hour}.10'
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    keyboard.append([
        InlineKeyboardButton("Подтвердить", callback_data='confirm'),
    ])
    return keyboard