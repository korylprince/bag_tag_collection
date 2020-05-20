#!/bin/bash

DB="Middle School.db" gunicorn -b "0.0.0.0:9000" app:app &
DB="High School.db" gunicorn -b "0.0.0.0:9001" app:app
