# job

Work smart not hard. Scrapy spider for searching for jobs. Currently only for Houston, TX.

## Installation

### Development version

    $ git clone https://github.com/zazazack/jobs.git

### Release version

    $ docker pull zwilson/jobs

## Usage

Crawls popular job posting sites (currently only indeed.com) to collect

To run locally w/ scrapy (via docker)

    $ docker run --rm -v ./items:/usr/src/items zwilson/jobs scrapy crawl indeed # TODO: test

To deploy add a version to a [scrapyd](https://github.com/scrapy/scrapyd) server

    $ docker-compose up

To deploy to a local instance of [spiderkeeper](https://github.com/DormyMo/SpiderKeeper) (via docker), first execute

    $ docker-compose run scrapyd-deploy --build-egg output.egg

`output.egg` will be saved to deploy/output.egg in the root of the workding directory.
