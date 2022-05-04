# harkare
Path to SiyaRam

## Install MinIO and run the binary if downloaded
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=password ./minio server /mnt/data --console-address ":9001"

## Install dependencies in vitual env to avoid breaking systems
pip install -r requirements.txt

## Heroku Commands
heroku destroy harkare --confirm harkare
heroku create harkare
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=6aj8il2xu2vqwvnitsg@\!+4-8t3%zwr@$agm7x%o%yb2t9idt%
heroku config:set DISABLE_COLLECTSTATIC=0
heroku config
git push heroku main

## Create Super User on Heroku
heroku run bash
python manage.py createsuperuser
