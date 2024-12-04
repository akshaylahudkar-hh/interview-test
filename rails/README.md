# Hinge Health Rails #


## Devs with Ruby Version Manager ##

For devs who are using a Ruby version manager such as _rvm_ or _rbenv_, `cd` into "hinge_health_challenge" and run `bundle install`. Then proceed with the usual test-edit-debug cycle in the "hinge_health_challenge" folder.


## Devs without Ruby Version Manager ##

For devs who have not installed a Ruby version manager, use _Makefile_ (which invokes `docker` via _Dockerfile_) to build, provision, test, and run the "hinge_health_challenge" app. Devs who already use a Ruby version manager can also use these files to avoid polluting their existing environments & configurations.

`Makefile` uses `Dockerfile` to build a Docker image named "hh_rails" with a recent version of Ruby (3.1.4) and Rails (6.1.7.6). This image allows devs to:

* `make build` - build the image.
* `make bundle` - provision the image with _bundle install_.
* `make cmd` - start a Bash shell to run tests, execute `rails` commands, etc.
* `make console` - start a `rails console`.
* `make server` - start a `rails server` that forward to port 3000.
* `make clean` - delete the Docker image and free up corresponding resources.

### Typical Development Life Cycle ###

You will run the `make` commands in the "rails" folder, while pointing your editor to files in the "hinge_health_challenge" folder.

The interactive & server `make` commands (_cmd_, _console_, _server_) map the "hinge_health_challenge" folder on your host machine to _/app_ in your image. Once you have an interactive terminal, you are automatically `cd` inside /app in the image.

#### `make build`
Run this once initially to create the Docker image. All subsequent commands depend on this image to function.

#### `make bundle`
Run this once to _bundle install_ the gems into the correct location on your host machine (_./bundle_ - which is git ignored). Run `make bundle` again as necessary when changes are made to _Gemfile_.

#### `make cmd`
Start a correctly bundled Bash shell. Devs can run tests, rubocop, etc in this shell. Multiple terminals can run `make cmd` simultaneously. Exit with Ctrl-d.

#### `make console`
Start a rails console for testing code, querying the DB, etc. This command can also be run simultaneously in multiple terminal windows. Exit with Ctrl-d.

#### `make server`
Start a rails server running the "hinge_health_challenge" app. Only one instance can be run at a time as port 3000 from the image is forwarded to your local host. Exit with Ctrl-c.

#### `make clean`
When you're done with development and no longer need the Docker image, `make clean` is a shortcut to delete it.


## Maintainers ##

Maintainers of this repository will use both `Makefile` and `maintainer.mk` to rebuild the "hinge_health_challenge" folder as needed in order to upgrade Ruby & Rails, etc.

_**CAUTION**_: The following steps will rebuild the "hinge_health_challenge" folder from scratch. As such, devs who are editing & working in "hinge_health_challenge" should _**NOT**_ follow any of these steps as they run a real risk of irrevocably losing their work.

### Rebuilding Steps ###

Follow these steps in order to rebuild the "hinge_health_challenge" folder. When you're `cd` in the same directory where this README resides:
1. `make build` - builds the "hh_rails" image
2. `make -f maintainer.mk rebuild` - rebuilds the "hinge_health_challenge" folder in a reproducible manner
3. `make -f maintainer.mk stage` - _git stage_ the changes
4. Inspect the staged changes for correctness.
5. `git commit` - if the inspection passes muster.
6. `make -f maintainer.mk restore` - if the inspection fails, restores the "hinge_health_challenge" folder to its most recent commit.

### Updating Ruby & Rails ###

When it is time to update Ruby and/or Rails, perform the following edits in `Dockerfile`:

1. Update the base ruby Docker image version from 3.1.4.
2. Update `bundler` as necessary (currently 2.4.13).
3. Update `rails` from 6.1.7.6.
4. Rerun the _Rebuilding Steps_ from the previous section.
