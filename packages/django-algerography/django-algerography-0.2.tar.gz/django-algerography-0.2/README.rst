============
Algerography
============

Algerography is a Django app that allow you to use 
Wilaya and Daira information of Algeria into you django project.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "algerography" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'algerography',
    ]

2. Run ``python manage.py migrate`` to create the algerography models.

3. Run ``python manage.py load_algerography`` to load wilaya and daira fixtures
into your database.