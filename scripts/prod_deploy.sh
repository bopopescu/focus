#!/bin/bash
ssh ubuntu@srv2.fncit.no -p 7500 '
    cd /home/ubuntu/www/prod_focustime/focus
    git pull origin prod
    bin/django syncdb
    bin/django migrate
    bin/django collectstatic --noinput
    sudo /etc/init.d/apache2 restart
'