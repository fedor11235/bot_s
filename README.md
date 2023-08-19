# telegram game bot
## Project setup
creating a virtual environment
```
python -m venv venv
```
launch virtual environment in cmd (windows)
```
venv\Scripts\activate
```
install all the necessary dependencies from requirements
```
pip install -r requirements.txt
```
bot launch
```
python newbot.py
```
server start
open another terminal and in it we write the command
```
python server.py
```
## for development
information about the bot is in the file "info_information.txt"

exit the virtual environment (windows)
```
venv\Scripts\deactivate.bat
```
save all project dependencies to a file
```
pip freeze > requirements.txt
```
примерное апи для работы с ботом, тут осуществляется отправка в общий чат ботом сообщение
```
'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHATID + '&parse_mode=html&text=' + TEXT
```
## how to set up a bot
to create and edit your bots in telegram use @BotFather bot
