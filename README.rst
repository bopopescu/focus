For å bruke GIT
=============

for å hente nyeste versjon:

	git pull origin master

for å registere nye endringer

	git add <filnavn>

	git commit -a
	
for å sende nye endringer til server

	git push origin master


Generelt
=============

Når du har gjort endringer på modeller

	bin/django schemamigration <appnavn> --auto

Hvis du har opprettet ny app

	bin/django schemamigration <appnavn> --initial

Hvis du har registrert endringer, og vil skrive endringer til database

	bin/django migrate

For å fyre opp prosjektet i nettleser

	bin/django runserver


Første installasjon
=============

For å sette opp prosjektet for første gang

	git clone git@github.com:frecarlsen/focus.git

	cd focus

	python bootstrap.py

	bin/buildout

	bin/django syncdb

	bin/django migrate

	bin/django runserver
