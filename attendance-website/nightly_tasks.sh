#!/bin/bash
cd "$(dirname "$0")"
python manage.py logout
python manage.py synchours
python manage.py recalculate
python manage.py sendchangesupdate
