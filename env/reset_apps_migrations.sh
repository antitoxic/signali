rm -r src/contact/migrations
rm -r src/feedback/migrations
rm -r src/location/migrations
rm -r src/siteguide/migrations
rm -r src/taxonomy/migrations

python manage.py makemigrations contact
python manage.py makemigrations feedback
python manage.py makemigrations location
python manage.py makemigrations siteguide
python manage.py makemigrations taxonomy