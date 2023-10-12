from telegram import Update

async def get_text_for_post(update: Update, context):
  post = ''
  if update.message.animation:
    file_id = update.message.animation.file_id
    # file_info = await context.bot.get_file(file_id)
    # file_path = file_info.file_path
    text = update.message.caption_html
    if text:
      post = text + '*' + file_id + '%' + 'animation'
    else:
      post = file_id+ '%' + 'animation'
  elif  update.message.video:
    file_id = update.message.video.file_id
    # file_info = await context.bot.get_file(file_id)
    # file_path = file_info.file_path
    text = update.message.caption_html
    if text:
      post = text + '*' + file_id + '%' + 'video'
    else:
      post = file_id+ '%' + 'video'
  elif update.message.photo:
    file_id = update.message.photo[-1].file_id
    # file_info = await context.bot.get_file(file_id)
    # file_path = file_info.file_path
    text = update.message.caption_html
    if text:
      post = text + '*' + file_id + '%' + 'photo'
    else:
      post = file_id + '%' + 'photo'
  else:
    post = update.message.text_html
  return post