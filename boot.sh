#!/bin/sh
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        flask populatedb artists
        flask populatedb hits
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - task:app