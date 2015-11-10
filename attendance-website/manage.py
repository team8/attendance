#!/usr/bin/env python
import os
import sys
import threading

AUTOLOGOUTENABLED = True

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance.settings")

    from django.core.management import execute_from_command_line

    if AUTOLOGOUTENABLED:
        import autoLogout
        threading.Thread(target=autoLogout.main).start()

    execute_from_command_line(sys.argv)
