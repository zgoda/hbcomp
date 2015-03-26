#! /bin/bash

pybabel extract -F ./babel.cfg -k lazy_gettext -o ./hbapp/translations/messages.pot ./

pybabel init -i ./hbapp/translations/messages.pot -d ./hbapp/translations -l pl
