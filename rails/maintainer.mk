# Makefile for use by repository maintainers only. All others, please avoid.

include config.mk

caution:
	echo CAUTION: Using this Makefile will erase all your work.

rebuild:
	# start from scratch
	rm -rf ./$(APP_NAME)

	# --api AND --minimal has smaller footprint than just --api
	$(RUN_IN_PARENT) rails new $(APP_NAME) --api --minimal

	# no need for app folder git
	rm -rf ./$(APP_NAME)/.git

	# no need for credentials
	rm -rf ./$(APP_NAME)/config/credentials.yml.enc

	# custom Hello & rubocop config
	cp -a ./source/. ./$(APP_NAME)/

	# give devs access to rspec in addition to default minitest
	$(RUN_IN_APP) bundle add rspec-rails --group "development, test"

	# give devs access to rubocop so they can lint
	$(RUN_IN_APP) bundle add rubocop --group development

	# create initial rspec files
	$(RUN_IN_APP) bundle exec rails generate rspec:install

	# lint & correct default new rails app
	$(RUN_IN_APP) bundle exec rubocop -A

	# convenient gemset for devs who use rvm
	echo "$(IMAGE)" > ./$(APP_NAME)/.ruby-gemset

# Once the app has been rebuilt, stage it for final inspection before committing
stage:
	git status --short | grep "$(APP_NAME)/" | perl -pe 's/.+ //' | xargs git add

# If the updated app does not pass inspection, unwind the changes
restore:
	git restore --staged ./$(APP_NAME)/
	rm -rf ./$(APP_NAME)/
	git co ./$(APP_NAME)/
