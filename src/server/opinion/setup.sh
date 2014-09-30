rm os.sqlite
python manage.py syncdb --noinput
#python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
python scripts/create_db_quake.py 8
python scripts/populate_db_random.py
python scripts/add_ud_cache_for_ratings.py
python scripts/recalculate_median_grades.py
