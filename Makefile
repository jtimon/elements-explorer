# Only use these programs directly or explain yourself:
#  awk cat cmp cp diff echo egrep expr false grep install-info ln ls
#  mkdir mv printf pwd rm rmdir sed sleep sort tar test touch tr true

.PHONY: dev dev-nod staging staging-nod production production-nod
all: dev-nod

dev:
	cd docker/dev && docker-compose up -d --build
dev-nod:
	cd docker/dev && docker-compose up --build
staging:
	cd docker/staging && docker-compose up -d --build
staging-nod:
	cd docker/staging && docker-compose up --build
production:
	cd docker/production && docker-compose up -d --build
production-nod:
	cd docker/production && docker-compose up --build

test-dummydb-nod:
	rm -rf /tmp/test-elements-explorer && cd docker/test-dummydb && export CURRENT_UID=$(id -u):$(id -g) && docker-compose up --build
test-postgres-nod:
	rm -rf /tmp/test-elements-explorer && cd docker/test-postgres && export CURRENT_UID=$(id -u):$(id -g) && docker-compose up --build

.PHONY: check check-dummydb check-postgres check-all
check-dummydb:
	python3 ./run_tests.py --dbs=dummydb
check-postgres:
	python3 ./run_tests.py --dbs=postgres
check-all:
	python3 ./run_tests.py --dbs=dummydb,postgres
check: check-postgres

.PHONY: stop stop-dev stop-staging stop-production
stop-dev:
	cd docker/dev ; docker-compose stop
stop-staging:
	cd docker/staging ; docker-compose stop
stop-production:
	cd docker/production ; docker-compose stop
stop: stop-dev stop-staging stop-production

.PHONY: clean docker-prune clean-db
# docker-compose rm -f
# cd docker && docker-compose down
docker-prune:
	docker system prune -a

clean-db:
	rm -f ../explorer-data/target/schema.json

clean: docker-prune clean-db
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -q)
