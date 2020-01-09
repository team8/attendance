#!/bin/bash
cd "$(dirname "$0")"
python manage.py logout
python manage.py synchours