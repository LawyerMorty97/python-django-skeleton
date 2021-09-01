python -c "import django_extensions"

if [ $? -eq 0 ]; then
	python manage.py runserver_plus $@
else
	python manage.py runserver $@
fi