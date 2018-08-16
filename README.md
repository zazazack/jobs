# jobs

Work smart not hard.

Scrapy spider for searching for jobs. ~~Currently only for Houston, TX.~~

## Prerequisites

-   `git`
-   Docker CE

## Installation

    $ git clone https://github.com/zazazack/jobs.git
    $ cd jobs/
    $ docker swarm init
    $ docker stack up -c stack.yml jobs

To confirm the stack is reachable from the host

    $ curl localhost:5602  # 5602 == nginx reverse proxy

To schedule a daily cron job to run the spiders

    $ cp ./configs/cron/crontab /etc/cron/daily/jobs.crontab

## Testing

To test the spiders

    $ docker exec jobs_app.1 scrapy crawl rigzone

## Usage

Visit localhost:5602 to view and analyze the data.
