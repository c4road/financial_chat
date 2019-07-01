# Financial Chat

This is a Django Channels chat implementation with a Celery task queue. You can create rooms, chat and retrieve stock's closing data with this command /stock=AAPL.US where AAPL.US is the ticker of the security. You can see more tickers and financial information in stooq.com

## Installing

First you need to activate the environment.

On Linux:
```bash
virtualenv -p python3 financialchat
cd ca_challenge
git clone https://github.com/Ballanxe/financial_chat.git
mv financial_chat src 
source bin/activate
cd src 
pip install -r requirements.txt
```

## Setting Up

The environment is using SQLite by default, to make easier to run and test the project. 

Minimalistic implementation of custom user model. It could be more minimalistic.

Mr. Bot algorithm could be optimized without using dictionary object, just using a list. But I thing it is more elegant! 

Do not forget start redis server in a separate terminal

```bash
redis-server
```

And run the celery worker, also in a separate terminal

```bash
celery -A financialchat worker -l info
```

Then, you know the drill!


```bash
python manage.py makemigrations profiles chat
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Testing

Currently 75%, nothing fancy!

```bash
coverage run --source='profiles','chat' manage.py test
coverage report
```

Check PEP8 compliance!

```bash
flake8 profiles chat
```






