# Update(
#   message=Message(
#     channel_chat_created=False, 
#     chat=Chat(
#       first_name='АО', 
#       id=6358290821, 
#       last_name='ГК «Талент»', 
#       type=<ChatType.PRIVATE>, 
#       username='JSC_Talent_Group'),
#     date=datetime.datetime(2023, 8, 23, 12, 7, 37, tzinfo=datetime.timezone.utc),
#     delete_chat_photo=False,
#     entities=(
#       MessageEntity(
#           length=6, offset=0, type=<MessageEntityType.BOT_COMMAND>),),
#           from_user=User(
#           first_name='АО',
#           id=6358290821,
#           is_bot=False,
#           language_code='ru',
#           last_name='ГК «Талент»',
#           username='JSC_Talent_Group'
#           ),
#     group_chat_created=False,
#     message_id=5,
#     supergroup_chat_created=False,
#     text='/start'
#     ),
#   update_id=913966895
# )

# ChatMemberMember(
#   status=<ChatMemberStatus.MEMBER>,
#   user=User(first_name='Slon', id=6423584132, is_bot=True, username='SlonPostBot')
# )

# Message(channel_chat_created=False, chat=Chat(first_name='Fedor', id=372099197, last_name='Avdeev', type=<ChatType.PRIVATE>, username='fedor11235b'), date=datetime.datetime(2023, 9, 1, 10, 52, 33, tzinfo=<UTC>), delete_chat_photo=False, forward_date=datetime.datetime(2023, 9, 1, 
# 10, 48, 42, tzinfo=<UTC>), forward_from_chat=Chat(id=-1001713055963, title='test3', type=<ChatType.CHANNEL>, username='jbhjvyvy'), forward_from_message_id=2, from_user=User(first_name='Fedor', id=372099197, is_bot=False, language_code='ru', last_name='Avdeev', username='fedor11235b'), group_chat_created=False, message_id=470, supergroup_chat_created=False, text='ссс')

stroka = 'ef_fedor_pd'
check = "education"
# print(check in stroka)

array = ['all', 'education', 'finance', 'health', 'news', 'tech', 'entertainment', 'psychology', 'video', 'author', 'other']


print(check in array)
