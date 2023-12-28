from typing import List, Any
import json

from telegram import InlineKeyboardButton


def init_time_slots_keyboard_data():
    """
    Keyboard for selecting booking time slots in section Slon Business✨
    """
    keyboard_data = []
    k = 0
    for i in range(8, 13):
        keyboard_row = []

        for j in range(0, 3):
            hour = i + j * 5
            button_value = f'{hour}.10'
            button_text = f'{hour}:10'
            button_item = {'id': k + 1, 'text': button_text, 'data': button_value, 'checked': False,
                           'is_available': True}
            keyboard_row.append(button_item)
            k += 1
        keyboard_data.append(keyboard_row)
    return keyboard_data

def day_time_choice_keyboard(keyboard_data: List, available_values=None, channel: Any = 'channel'):
    # print('day_time_choice_keyboard')
    print(len(available_values))
    keyboard = [
        [
            InlineKeyboardButton("Утро", callback_data='empty'),
            InlineKeyboardButton("День", callback_data='empty'),
            InlineKeyboardButton("Вечер", callback_data='empty'),
        ]
    ]

    for i in range(5):
        keyboard_row = []

        for j in range(3):
            button_item = keyboard_data[i][j]
            callback_data = {
                'id': button_item['id'],
                'text': button_item['text'],
                'data': button_item['data'],
                'checked': button_item['checked']
            }
            # print(button_item)
            if i == 0 and j == 0:
                with open('button_item.json', 'w') as fp:
                    json.dump(button_item, fp)
            # hour = i + j * 5
            # time_value = f'{hour}.10'
            time_value = button_item['data']
            is_available = True
            if available_values is not None:
                is_available = (time_value in available_values)
            print(is_available)
            # button_value = 'empty' if not is_available else time_value
            button_item['is_available'] = is_available
            button_text = '✅ ' if button_item['checked'] else ''
            button_text = '❌ ' if not is_available else button_text
            button_text += button_item['text'] # f'{hour}:10'
            # if i == 0 and j == 0:
            # button_item = {'id': i + 1, 'text': button_text, 'data': button_value, 'checked': False}
            keyboard_row.append(InlineKeyboardButton(button_text, callback_data=json.dumps(callback_data)))
            # json.dumps(button_item)
        keyboard.append(keyboard_row)
    keyboard.append([
        InlineKeyboardButton("Подтвердить", callback_data='opt-into_@'+ channel +'_time-confirm'),
    ])

    return keyboard


def selection_buttons_keyboard(data: List):
    keyboard = [[]]
    for button_item in data:
        button_text = '✅ ' if button_item['checked'] else ''
        button_text += button_item['text']
        keyboard[0].append(InlineKeyboardButton(button_text, callback_data=json.dumps(button_item)))
    return keyboard