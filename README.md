**Description**
This project allows you to have a website that will let you visualize how your last.fm friends have spent their past week listening to music, in terms of sum duration of seconds listened to tracks/artists. Lets you listen to any track your friends have listened to during that timeframe, within an embedded youtube player on the page. Check out the screenshots for a better sense of how it works. This project was basically an excuse for me to learn javascript and css, as well as an excuse to play around with rabbitmq and celery. It's certainly not a polished product, and it's certainly not pretty, but it does what it needs to.


**Requirements**

    Google Chrome (Firefox also 'sort-of' works, but the experience sucks. Haven't tested it w ff v5, YMMV)
    python 2.6 (probably works with other versions.)
    MySQL (probably works w any other db django supports, but untested)
    RabbitMQ
    pip install django
    pip install django-celery
    pip install south
    pip install mysql-python
    pip install python-memcached
    pip install simplejson
    pip install -e git+http://github.com/pika/pika.git@v0.5.2#egg=pika-v0.5.2
    pip install gdata
    

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

At this point, you'll have a list of artists with proportionate bars labelled with usernames in the main viewing pane. The username-labelled bars are scaled proportionate to total sum seconds listened in the past week to that artist. The outer bar is scaled to the aggregate sum of seconds spent listening to that artist among all of your lastfm friends, proportionate to the aggregate sum for the artist currently at the top of the main viewing pane.

Click any artist name for a list of their tracks to fill the bottom area, sorted by sum number of seconds spent listening to each, with sum listening duration indicated with the green bars. Click a particular username instead of the artist name to get only listening data for a particular user for a particular artist. 

Inside the bottom area, click any track title to bring up a youtube player and add it to a playlist. Ex: there are 3 songs in the playlist in Screenshot 2, with the currently playing track inside the main viewing area. If you want to switch the artist/user you are viewing data for within the bottom area, you can hit the minimize button above the currently playing video. In chrome, you'll continue to hear the audio. In firefox, you won't (not tested w FF5). 

**Screenshots**
![Screenshot 1](https://img.skitch.com/20110725-mn6day4uxsdmjrqbdress6yjrg.jpg "Friends listening, visualized")
![Screenshot 2](https://img.skitch.com/20110725-gc3gg3awwtyrx89cfx1f2nm2yj.jpg "Youtube and Playlist")

