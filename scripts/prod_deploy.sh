#!/bin/bash

# A quick deploy skips bootstrap, buildout, syncdb and migrate
quick=0

# Help
function usage {
    echo "Usage: prod_deply [-q]"
    echo "Arguments:"
    echo "  -q: Quick deploy, skips bootstrap, buildout, syncdb and migration"
}

# Add more commands here at your/our leisure :)
while [ "$1" != "" ]; do
    case $1 in
        -q | --quick )          quick=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

# SSH in and prod that shit
if [ $quick == 1 ]; then
    echo "Quick deploy"

    ssh ubuntu@srv2.fncit.no -p 7500 '
        cd /home/ubuntu/www/prod_focustime/focus
        git pull origin prod
        sudo /etc/init.d/apache2 restart
    '

else
    ssh ubuntu@srv2.fncit.no -p 7500 '
        cd /home/ubuntu/www/prod_focustime/focus
        git pull origin prod
        bin/django syncdb
        bin/django migrate
        bin/django collectstatic --noinput
        sudo /etc/init.d/apache2 restart
        '
fi