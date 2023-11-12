#!/bin/bash

python /ticketApp/karma/manage.py makemigrations
python /ticketApp/karma/manage.py migrate
python /ticketApp/karma/manage.py loaddata /ticketApp/karma/kits/fixtures/kits_data.json
python /ticketApp/revives_import.py
python /ticketApp/warnings_import.py