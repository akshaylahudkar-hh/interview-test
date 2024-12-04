# Makefile with convenient shortcuts to build, clean, & run a
# Ruby-on-Rails development environment.
#
#	make build - builds the Docker image from Dockerfile
#	make clean - removes the Docker image
#	make bundle - bundle install into ./bundler in the host
#	cmd - runs a Bash shell with the proper RoR environment
#	console - runs a rails console directly
#	server - runs a rails server with forwarded port 3000
#

include config.mk

build:
	docker build . -t $(IMAGE)

clean:
	docker image rm $(IMAGE)

bundle:
	$(RUN_IN_APP) bundle install

cmd:
	$(RUN_IN_APP)

console:
	$(RUN_IN_APP) rails console

server:
	$(RUN_IN_APP_3000) rails server -b 0.0.0.0
