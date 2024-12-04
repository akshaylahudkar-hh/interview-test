# Build a Docker image suitable for Ruby-on-Rails development using
# Ruby 3.1.4 and Rails 6.1.7.6.

FROM ruby:3.1.4

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  zsh
RUN gem install -v 2.4.13 bundler
RUN gem install -v 6.1.7.6 rails
RUN gem install rake
RUN gem install rspec-rails
RUN gem install rubocop

WORKDIR /app
RUN git config --global init.defaultBranch main

# use CMD instead of ENTRYPOINT to allow `docker run` override -
# https://stackoverflow.com/a/34245657
CMD ["/bin/bash"]
