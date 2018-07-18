# Only use these programs directly or explain yourself:
#  awk cat cmp cp diff echo egrep expr false grep install-info ln ls
#  mkdir mv printf pwd rm rmdir sed sleep sort tar test touch tr true

# TODO FIX s/sudo //

.PHONY: dev dev-nod staging staging-nod production production-nod
all: dev-nod

.PHONY: dev-conf stating-conf production-conf

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
	sudo rm -f ../explorer-data/target/schema.json

clean: docker-prune clean-db
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -q)
