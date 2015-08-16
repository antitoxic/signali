rm -r src/signali_contact/migrations
rm -r src/signali_location/migrations
rm -r src/signali_accessibility/migrations
rm -r src/signali_taxonomy/migrations
rm -r src/signali/migrations

python manage.py makemigrations signali_contact
python manage.py makemigrations signali_location
python manage.py makemigrations signali_accessibility
python manage.py makemigrations signali_taxonomy
python manage.py makemigrations signali
