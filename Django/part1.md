# Writing your first Django app, part1 (modes)

MTV

    """
        request --> view.function   -->response
                --> model
                --> templates
    """

## First Django App

show django version

	python -c "import django; print(django.get_version())"	

create a new project 

	django-admin.py startproject opweb 

runing server 
	
	python manage.py runserver 0.0.0.0:8000

## Create models

create a app

	python manage.py startapp op

edit op/models.py

edit opweb/settings.py

	add line 'op',  in INSTALLED_APPS 

Activating models 

	python manage.py validate
	python manage.py makemigrations op 
	python manage.py sqlmigrate op 0001
	python manage.py migratge

Playing with the API

	python manage.py shell
	from polls.models import Question, Choice
	from django.utils import timezone
	q = Question.objects.get(pk=1)
	q.was_published_recently()
	q.choice_set.all()
	q.choice_set.create(choice_text='Not much', votes=0)
	q.choice_set.create(choice_text='The sky', votes=0)
	c = q.choice_set.create(choice_text='Just hacking again', votes=0)
	q.choice_set.all()
	q.choice_set.count()
	c = q.choice_set.filter(choice_text__startswith='Just hacking')
	c.delete()
	q.choice_set.count()
	q.choice_set.all()

Add templates

    mkdir templates

    vim setting
    TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

Return

    Httpresponse()          # 返回数据
    render_to_response()    # 返回页面
