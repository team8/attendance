#!/bin/bash
echo "we did the thing"
cd /home/bdavies/.virtualenvs/attendance
source bin/activate
cd ../../../../
cd home/bdavies/attendance/attendance-website
python manage.py logout
