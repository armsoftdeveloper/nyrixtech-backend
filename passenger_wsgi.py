"""
Entry point cPanel's "Setup Python App" (Phusion Passenger) expects.

When you create the app in cPanel, it generates a stub passenger_wsgi.py in the
app root — replace its contents with this file so it points at the real Django
WSGI application instead.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402
