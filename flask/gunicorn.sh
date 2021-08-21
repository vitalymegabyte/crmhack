#!/bin/sh
gunicorn --reload --chdir app app:app -b 0.0.0.0:80
