**Requirements**
    python 2.6 (probably works with other versions.)
    pip install django
    pip install django-celery
    pip install south
    pip install mysql-python
    pip install python-memcached
    pip install simplejson
    pip install -e git+http://github.com/pika/pika.git@v0.5.2#egg=pika-v0.5.2
    pip install gdata
    rabbitmq

    OPTIONAL:
    pip install django-debug-toolbar
    pip install django-extensions
    pip install werkzeug
    
**Usage**
Run memcached, run rabbitmq-server, run django.
Connect to the root url, submit your username in the form.
Give it 5-10 minutes to gather all the necessary data from lastfm.
Connect again to the root url, submit your username in the form.
Give it a few minutes (there's a lot of optimization to be done here,
the data processing takes an absurdly long amount of time for this step)


**Screenshots**
![Screenshot 1](https://img.skitch.com/20110725-mn6day4uxsdmjrqbdress6yjrg.jpg "Friends listening, visualized")
![Screenshot 2](https://img.skitch.com/20110725-gc3gg3awwtyrx89cfx1f2nm2yj.jpg "Youtube and Playlist")

