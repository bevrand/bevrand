# This repository and project is no longer maintained

# bevrand
The Beverage Randomizer Repo

For creation of docker-compose please use docker-compose-create.py

To get more information please run:

python3 docker-compose-create.py --help

Quick start:

python3 docker-compose-create.py
docker-compose -f docker-compose-created.yml build && docker-compose -f docker-compose-created.yml up -d 

## Automated checks
### Build Status
Travis CI

[![Build Status](https://img.shields.io/travis/bevrand/bevrand.svg?style=flat)](https://travis-ci.org/bevrand/bevrand)

CircleCI

[![CircleCI](https://img.shields.io/circleci/project/github/bevrand/bevrand.svg?style=flat)](https://circleci.com/gh/bevrand/bevrand)

### Licensing
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbevrand%2Fbevrand.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbevrand%2Fbevrand?ref=badge_shield)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

### Code Conventions
[![Code Factor](https://www.codefactor.io/repository/github/bevrand/bevrand/badge?style=plastic)](https://www.codefactor.io/repository/github/bevrand/bevrand/badge?style=plastic)
<!-- [![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com) -->

### Code Quality
[![Maintainability](https://api.codeclimate.com/v1/badges/adeebe7e99a8d049645c/maintainability)](https://codeclimate.com/github/bevrand/bevrand/maintainability)

[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=alert_status)](https://sonarcloud.io/dashboard?id=bevrand)

[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=bugs)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=code_smells)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=ncloc)](https://sonarcloud.io/dashboard?id=bevrand)

[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=security_rating)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=sqale_index)](https://sonarcloud.io/dashboard?id=bevrand)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=bevrand&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=bevrand)

## Services

### Dockernginx
Nginx container to route requests to either Frontend or Proxy API.

[![](https://img.shields.io/docker/pulls/bevrand/dockernginx.svg?style=flat)](https://hub.docker.com/r/bevrand/dockernginx "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/dockernginx:production.svg)](https://microbadger.com/images/bevrand/dockernginx:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/dockernginx:production.svg)](https://microbadger.com/images/bevrand/dockernginx:production "View version details on microbadger.com")

### Frontend
Nginx container to serve the Single Page Application.

[![](https://img.shields.io/docker/pulls/bevrand/frontend.svg?style=flat)](https://hub.docker.com/r/bevrand/frontend "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/frontend:production.svg)](https://microbadger.com/images/bevrand/frontend:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/frontend:production.svg)](https://microbadger.com/images/bevrand/frontend:production "View version details on microbadger.com")

### Proxy API
NodeJS service to handle authentication, verify request, and call the backend services.

[![Node 11.9](https://img.shields.io/badge/node-11.9-blue.svg)](https://nodejs.org/en/download/current/)

[![](https://img.shields.io/docker/pulls/bevrand/proxyapi.svg?style=flat)](https://hub.docker.com/r/bevrand/proxyapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/proxyapi:production.svg)](https://microbadger.com/images/bevrand/proxyapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/proxyapi:production.svg)](https://microbadger.com/images/bevrand/proxyapi:production "View version details on microbadger.com")

### Authentication API
C# dotnet core service to register and authenticate users, using a Postgres database as storage.

[![dotnet core 2.2](https://img.shields.io/badge/dotnet_core-2.2-blue.svg)](https://dotnet.microsoft.com/download/dotnet-core/2.2)

[![](https://img.shields.io/docker/pulls/bevrand/authenticationapi.svg?style=flat)](https://hub.docker.com/r/bevrand/authenticationapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/authenticationapi:production.svg)](https://microbadger.com/images/bevrand/authenticationapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/authenticationapi:production.svg)](https://microbadger.com/images/bevrand/authenticationapi:production "View version details on microbadger.com")

### Playlist API
Python service to get lists of beverage from a MongoDB.

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![](https://img.shields.io/docker/pulls/bevrand/playlistapi.svg?style=flat)](https://hub.docker.com/r/bevrand/playlistapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/playlistapi:production.svg)](https://microbadger.com/images/bevrand/playlistapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/playlistapi:production.svg)](https://microbadger.com/images/bevrand/playlistapi:production "View version details on microbadger.com")

### Randomizer API
Python service to randomize a beverage from a beverage list.

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![](https://img.shields.io/docker/pulls/bevrand/randomizerapi.svg?style=flat)](https://hub.docker.com/r/bevrand/highscoreapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/randomizerapi:production.svg)](https://microbadger.com/images/bevrand/randomizerapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/randomizerapi:production.svg)](https://microbadger.com/images/bevrand/randomizerapi:production "View version details on microbadger.com")

### Highscore API
Golang service to process randomized beverages and serve high-score information.

[![go 1.11.5](https://img.shields.io/badge/go-1.11.5-blue.svg)](https://golang.org/doc/go1.11)
[![Go Report Card](https://goreportcard.com/badge/github.com/bevrand/bevrand)](https://goreportcard.com/report/github.com/bevrand/bevrand)

[![](https://img.shields.io/docker/pulls/bevrand/highscoreapi.svg?style=flat)](https://hub.docker.com/r/bevrand/highscoreapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/highscoreapi:production.svg)](https://microbadger.com/images/bevrand/highscoreapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/highscoreapi:production.svg)](https://microbadger.com/images/bevrand/highscoreapi:production "View version details on microbadger.com")

### Recommendation API
Golang service to make recommendations for playlist creation. Uses Neo4j as a backend

[![go 1.11.5](https://img.shields.io/badge/go-1.11.5-blue.svg)](https://golang.org/doc/go1.11)
[![Go Report Card](https://goreportcard.com/badge/github.com/bevrand/bevrand)](https://goreportcard.com/report/github.com/bevrand/bevrand)

[![](https://img.shields.io/docker/pulls/bevrand/recommendationapi.svg?style=flat)](https://hub.docker.com/r/bevrand/recommendationapi "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/recommendationapi:production.svg)](https://microbadger.com/images/bevrand/recommendationapi:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/recommendationapi:production.svg)](https://microbadger.com/images/bevrand/recommendationapi:production "View version details on microbadger.com")

### Elastic Search
Elastic Search image with our configuration applied.

[![](https://img.shields.io/docker/pulls/bevrand/dockerels.svg?style=flat)](https://hub.docker.com/r/bevrand/dockerels "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/dockerels:production.svg)](https://microbadger.com/images/bevrand/dockerels:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/dockerels:production.svg)](https://microbadger.com/images/bevrand/dockerels:production "View version details on microbadger.com")

### Dockergres
Postgres image with our configuration and schema applied.

[![](https://img.shields.io/docker/pulls/bevrand/dockergres.svg?style=flat)](https://hub.docker.com/r/bevrand/dockergres "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/dockergres:production.svg)](https://microbadger.com/images/bevrand/dockergres:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/dockergres:production.svg)](https://microbadger.com/images/bevrand/dockergres:production "View version details on microbadger.com")

## Supporting containers

### Dataseeder
TODO

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![](https://img.shields.io/docker/pulls/bevrand/dataseeder.svg?style=flat)](https://hub.docker.com/r/bevrand/dataseeder "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/dataseeder:production.svg)](https://microbadger.com/images/bevrand/dataseeder:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/dataseeder:production.svg)](https://microbadger.com/images/bevrand/dataseeder:production "View version details on microbadger.com")

### Componenttest
TODO

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![](https://img.shields.io/docker/pulls/bevrand/componenttests.svg?style=flat)](https://hub.docker.com/r/bevrand/componenttests "View details on docker hub")
[![](https://images.microbadger.com/badges/version/bevrand/componenttests:production.svg)](https://microbadger.com/images/bevrand/componenttests:production "View version details on microbadger.com")
[![](https://images.microbadger.com/badges/image/bevrand/componenttests:production.svg)](https://microbadger.com/images/bevrand/componenttests:production "View version details on microbadger.com")

## Infrastructure

[![](https://www.cloudflare.com/media/images/web-badges/cf-web-badges-f-4.png)](https://cloudflare.com "Cloudflare.com")

[![](https://img.shields.io/uptimerobot/status/m780479359-09cc629e32902510a1c838ed.svg?style=flat)](https://status.beveragerandomizer.com/ "Uptime Robot")
[![](https://img.shields.io/uptimerobot/ratio/m780479359-09cc629e32902510a1c838ed.svg?style=flat)](https://status.beveragerandomizer.com/ "Uptime Robot")

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbevrand%2Fbevrand.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbevrand%2Fbevrand?ref=badge_large)
