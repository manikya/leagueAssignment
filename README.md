Install Django 3.1.7

Install Python 3.8.6


run command to int database

```bash
python manage.py migrate
```

run command to initialize data dump into database

```bash
python manage.py loaddata data_dump.json
```

| username   | password | type   |
|------------|----------|--------|
| superuser  | 123      | admin  |
| coach1     | 123      | coach  |
| player_1_1 | 123      | player |