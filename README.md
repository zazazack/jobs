# jobs

Work smart not hard.

Scrapy spider for searching for jobs. ~~Currently only for Houston, TX.~~

## Installation

### Development version

    $ git clone https://github.com/zazazack/jobs.git

### Release version

    $ docker pull zwilson/jobs

## Usage

Crawls popular job posting sites (~~currently only indeed.com~~) to collect post data

To run locally w/ scrapy (via docker)

    $ docker run --rm -v items:/usr/src/items zwilson/jobs scrapy crawl $SPIDER

To deploy add a version to a [scrapyd](https://github.com/scrapy/scrapyd) server

    $ docker-compose up # NOTE: must be on the same network as scrapyd server
