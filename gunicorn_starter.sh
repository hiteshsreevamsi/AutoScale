#!/bin/sh
gunicorn --chdir app wsgi:application -w 2 --threads 2 0.0.0.0:5000
