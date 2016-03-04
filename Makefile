PYLINT_TEMPLATE = --msg-template='{msg_id}: {line}, {column}: {msg} ({symbol}) {obj}'
TMPFILE = '/tmp/${USER}_pyluac_piptmp'

help:
	@echo  "usage: make <target>"
	@echo  "    deps        Ensure development dependancies are installed"
	@echo  "    test        Runs unit tests"
	@echo  "    lint        Runs PyLint"

deps:
	@cat requirements.txt | grep -v '^#' | grep -v '^$$' | sort > ${TMPFILE}
	@if [ "X`pip freeze | sort | join -v1 ${TMPFILE} - 2>/dev/null`" != "X" ]; then pip install -r requirements.txt; fi

test:
	coverage run --branch --source=pyluac --omit=pyluac/parsetab.py setup.py -q test
	coverage report -m

lint:
	pylint --ignore=parsetab.py -f colorized $(PYLINT_TEMPLATE) pyluac/
