#!/bin/bash
ps -aux | grep -E 'runserver|omni' | awk '{print $2}' | xargs kill -HUP
python manage.py omnibusd & python manage.py runserver