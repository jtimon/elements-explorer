#!/bin/sh

gunicorn py:app -b "0.0.0.0:5000" -w 8 -k gevent
