#! /bin/bash

pybabel extract -F ./babel.cfg -k lazy_gettext -o ./hbapp/translations/messages.pot ./
pybabel update -l pl -d ./hbapp/translations/ -i ./hbapp/translations/messages.pot
