from telegram import Update

from create_btns import (
    go_chanel_opt_into,
    set_filters,
)
from requests_data import (
    get_profile,
    parse_filter,
)

# filters_type = ['rating', 'coverage', 'numberSubscribers', 'growthMonth', 'growthWeek', 'new', 'old', 'confirm']
filters_type = ['repost', 'numberSubscribers', 'coveragePub', 'coverageDay', 'indexSay']


async def filters(update: Update, _):
    query = update.callback_query
    query_array = query.data.split('_')
    user_id = query.message.chat.id
    # !ФИЛЬТРЫ
    if query_array[0] == 'filters':
        user = get_profile(user_id)
        filter = parse_filter(user['filter'])
        reply_markup = set_filters(query_array[1], filter)
        await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] in filters_type:
        reply_markup = set_filters(query_array[1], query_array[0])
        await query.edit_message_text('Фильтры', reply_markup=reply_markup)
    elif query_array[0] == 'apply':
        profile = get_profile(user_id)
        categoriesArray = go_chanel_opt_into(query_array[1], 1, 10, 1, profile['filter_opt'], user_id)
        await query.edit_message_text('все каналы', reply_markup=categoriesArray)
