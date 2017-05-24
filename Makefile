# Only use these programs directly or explain yourself:
#  awk cat cmp cp diff echo egrep expr false grep install-info ln ls
#  mkdir mv printf pwd rm rmdir sed sleep sort tar test touch tr true

SHELL = /bin/sh
ROOT=$(shell pwd)
BUILD_DIR=${ROOT}/.build
PYENV=${BUILD_DIR}/.virtualenv
JSENV=${BUILD_DIR}/js
BOWERENV=${ROOT}/app/bower_components

# easier move to python3
PYTHON=python2
PIP=pip

.PHONY: all clean requirements run
all: requirements

.PHONY: requirements-base clean-base freeze-base
requirements: requirements-base
requirements-base: $(BUILD_DIR)
clean-base:
	find . -name "*.pyc" -type f -delete
clean: clean-base
clean-full: clean-base clean
	rm -rf $(BUILD_DIR)

.PHONY: requirements-py clean-py clean-pip freeze-pip
requirements : requirements-py
requirements-py: requirements-base $(PYENV)/.stamp-h $(PYENV)/.stamp-pip-install-h
clean-pip: clean-base
clean-py: clean-base
	rm -rf $(PYENV)
clean: clean-pip clean-py

$(PYENV)/.stamp-pip-install-h: requirements.txt $(PYENV)/.stamp-h
	bash -c "source '$(PYENV)'/bin/activate && $(PIP) install -r requirements.txt"
	touch "$@"

$(PYENV)/.stamp-h:
	rm -rf $(PYENV)
	mkdir -p $(PYENV)
	virtualenv $(PYENV)
	touch "$@"


.PHONY: requirements-bower clean-bower
requirements : requirements-bower
requirements-bower: requirements-js $(BOWERENV)/.stamp-h $(BOWERENV)/.stamp-bower-install-h
clean-bower: clean-base
	rm -rf $(BOWERENV)
clean: clean-bower

$(BOWERENV)/.stamp-bower-install-h: bower.json $(BOWERENV)/.stamp-h
	bower install
	touch "$@"

$(BOWERENV)/.stamp-h:
	rm -rf $(BOWERENV)
	mkdir -p $(BOWERENV)
	touch "$@"

.PHONY: requirements-js clean-js clean-npm freeze-npm
requirements : requirements-js
requirements-js: requirements-base $(JSENV)/.stamp-h $(JSENV)/.stamp-npm-install-h
clean-npm: clean-base
clean-js: clean-npm clean-bower
	rm -rf $(JSENV)
clean: clean-npm clean-js

$(JSENV)/.stamp-npm-install-h: package.json $(JSENV)/.stamp-h
	cp package.json $(JSENV)/package.json
	npm i --prefix $(JSENV)
	touch "$@"

$(JSENV)/.stamp-h:
	rm -rf $(JSENV)
	mkdir -p $(JSENV)
	touch "$@"


$(BUILD_DIR):
	mkdir -p $@

run: all
	bash -c "source $(PYENV)/bin/activate && $(PYTHON) ./py/__init__.py"
