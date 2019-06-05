FROM ruby:2.6.1-alpine3.9

ENV BUILD_PACKAGES build-base

# Update and install all of the required packages.
# At the end, remove the apk cache
RUN apk update && \
    apk add $BUILD_PACKAGES && \
    rm -rf /var/cache/apk/*

RUN mkdir /usr/app
WORKDIR /usr/app

ADD Gemfile Gemfile.lock ./
RUN gem install bundler -v 2.0.1
RUN bundle install -j 8

ADD . .

ENV RUBY_ENV Docker