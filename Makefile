# Only use these programs directly or explain yourself:
#  awk cat cmp cp diff echo egrep expr false grep install-info ln ls
#  mkdir mv printf pwd rm rmdir sed sleep sort tar test touch tr true

SHELL = /bin/sh
ROOT=$(shell pwd)
BUILD_DIR=${ROOT}/.build
PYENV=${BUILD_DIR}/.virtualenv
DOCKERPROJECT=rpcexplorer

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


app/node_modules: app/package.json
	cd app && npm i
requirements : app/node_modules
clean-app-js:
	rm -rf app/node_modules
clean: clean-app-js

.PHONY: docker-build docker-up
docker-up:
	cd docker && docker-compose --project-name $(DOCKERPROJECT) up -d
docker-build:
	cd docker && docker-compose --project-name $(DOCKERPROJECT) up -d --build

.PHONY: docker-clean docker-down docker-prune
docker-down:
	cd docker && docker-compose --project-name $(DOCKERPROJECT) down
docker-prune:
	docker system prune -a
docker-clean: docker-prune
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -q)
clean: docker-clean

$(BUILD_DIR):
	mkdir -p $@

run: all
	bash -c "source $(PYENV)/bin/activate && $(PYTHON) ./py/__init__.py"
