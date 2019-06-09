# Financial Chat

This is a Django Channels chat implementation with a Celery task queue. You can create rooms, chat and retrieve stock's closing data with this command /stock=AAPL.US where AAPL.US is the ticker of the security. You can see more tickers and financial information in stooq.com

## Installing

First you need to activate the environment.

On Linux:
```bash
virtualenv -p python3 financialchat
cd ca_challenge
git clone https://github.com/Ballanxe/financial_chat.git
mv ca_challenge src 
source bin/activate
cd src 
pip install -r requirements.txt
```

## Setting Up

The environment is using SQLite by default, to make easier to run and test the project. 

After setup the DB, you need to run the following commands to have the data scheme right.

Remember to start a redis server first

```bash
$ redis-server
```

```bash
python manage.py makemigrations profiles chat
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

There you will be prompted to enter the superuser credentials: username, email
and password.



