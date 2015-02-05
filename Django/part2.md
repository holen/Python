# Django app, part 2 
automatically-generated admin site.  

create an admin user

	python manage.py createsuperuser

start the development server 

	python manage.py runserver

enter the admin site

	http://127.0.0.1:8000/admin/

make the poll app modifiable in the admin

	vim polls/admin.py
	from django.contrib import admin
	from polls.models import Question
	admin.site.register(Question)

make admin template

	mkdir -p templates/admin
	python -c "
	import sys
	sys.path = sys.path[1:]
	import django
	print(django.__path__)"
	cp /usr/local/lib/python2.7/dist-packages/django/contrib/admin/templates/admin/base_site.html templates/admin/


