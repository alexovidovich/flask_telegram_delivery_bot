# flask_telegram_delivery_bot
bot for delivery service

This is 2 years old test project with a lot of SUPER BAD CODE, but is example of my work then/
I've checked it today and wanna tell u how to run it./
it's not dockerized, sry./
- install requirements called libs.txt (updated)
- create your database (in this case it's mysql) and enter uri to config.py
- create bot with botfather
- put your telegram bot token into app.py
- set a webhook with url https://api.telegram.org/bot{token}/setWebhook?url={your https url to this app}
- run python3 manage.py db upgrade (alembic)
- run python3 main.py(running app, port 5000 default, u can use ngrok to make a step with a webhook)
- manualy, or using sqlalchemy (or admin panel) create first Text object for saying 'hi' when /start 
- manualy, or using sqlalchemy (or admin panel) create Menu objects 
- use bot

