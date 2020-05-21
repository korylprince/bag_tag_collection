#!/bin/bash

DB="Middle School.db" uwsgi --plugins python --http "0.0.0.0:9000" --module app:app &
DB="High School.db" uwsgi --plugins python --http "0.0.0.0:9001" --module app:app
