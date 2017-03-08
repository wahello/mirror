#!/usr/bin/env bash

while true; do

    # check db is ready
    while ! ((>/dev/tcp/db/5432) &>/dev/null)
    do
        echo "$(date) - waiting for db"
        sleep 1
    done
    echo "$(date) - db is ready, starting server"

    printf "\n# Deploying D-BAS...\n"
    python setup.py --quiet develop

    printf "\n# Compiling JS files...\n"
    google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,discussion,review}/*.js > dbas/static/js/dbas.min.js

    printf "\n# Compiling SASS files...\n"
    sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
    rm -r .sass-cache

    #printf "\n# Seeding discussion database...\n"
    #init_discussion_sql docker.ini > /dev/null 2>&1

    printf "\n# Drop old database...\n"
    psql -U postgres bash -c "dropdb -U postgres discussion --if-exists" > /dev/null 2>&1
    psql -U postgres bash -c "dropdb -U postgres news --if-exists" > /dev/null 2>&1

    #printf "\n# Restoring previous discussion database...\n"
    psql -U postgres bash -c "psql discussion < db/recent_db.sql" > /dev/null 2>&1

    printf "\n# Seeding news database...\n"
    init_news_sql docker.ini > /dev/null 2>&1

    printf "\n# Starting integrated web server -- for development use only!\n"
    uwsgi --ini-paste docker.ini

    echo ""
    echo "      ---------------------------------------"
    echo "     < A disturbance in the Force, I sense... >"
    echo "      ---------------------------------------"
    echo "        /"
    echo "       /"
    echo "      /"
    echo "__.-._"
    echo "'-._\"7'"
    echo " /'.-c"
    echo " |  /T"
    echo "_)_/LI"
    echo ""

    sleep 3

done