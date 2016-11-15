#!/usr/bin/env python
import os
import sys
import threading

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance.settings")

    from django.core.management import execute_from_command_line

    # if AUTOLOGOUTENABLED:
        # import autoLogout
        # t = threading.Thread(target=autoLogout.main)
        # t.daemon = True
        # t.start()
    execute_from_command_line(sys.argv)
