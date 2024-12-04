# Common variables for both dev and maintainer Makefiles.

# XXX_DIR is path inside image
# XXX_FOLDER is path on your host machine
#
APP_NAME=hinge_health_challenge
BUNDLE_DIR=/bundle
BUNDLE_FOLDER=./bundle
IMAGE=hh_rails
WORK_DIR=/app

# `docker run` in parent directory
define RUN_IN_PARENT
    docker run --rm -it \
        -v ./:$(WORK_DIR) \
        -v $(BUNDLE_FOLDER):$(BUNDLE_DIR) \
        -e BUNDLE_PATH=$(BUNDLE_DIR) \
        $(IMAGE)
endef

# `docker run` in app directory
define RUN_IN_APP
    docker run --rm -it \
        -v ./$(APP_NAME):$(WORK_DIR) \
        -v $(BUNDLE_FOLDER):$(BUNDLE_DIR) \
        -e BUNDLE_PATH=$(BUNDLE_DIR) \
        $(IMAGE)
endef

# `docker run` in app directory + forward port 3000
define RUN_IN_APP_3000
    docker run --rm -it \
        -v ./$(APP_NAME):$(WORK_DIR) \
        -v $(BUNDLE_FOLDER):$(BUNDLE_DIR) \
        -e BUNDLE_PATH=$(BUNDLE_DIR) \
		-p 3000:3000 \
        $(IMAGE)
endef
