# Content Proxy

A proxy server to allow navigation and interactions with foreign web assets, supports content insertion into proxied response.

# Usage

For local devlopment, clone this repo then:

```bash
pipenv run python3 ./proxy/main.py
```

Then navigate to (for example) a proxied version of gov.uk via http://127.0.0.1:5000/?url=https://www.gov.uk/.

You can see a complete list the sites and urls we can currently proxy in `./proxy/handlers/all.py`.

# How it works

Interventions are required to proxy web resources (for example, you need to rewrite relative to absolute links). We are implementing this via site level handlers. Whereas for content injection you extend that handler.

Example:
* (a) site handler: `./proxy/handlers/govuk.GovUKHandler`
* (b) page handler: `./proxy/handlers/govuk.GovUKStatisticsHandler`


So _all_ gov.uk pages matching the url `https://www.gov.uk` apply (a) but **only** urls matching `https://www.gov.uk/government/statistics` _then_ also apply (b).


# CI

TODO: it'll be cloudrun and actions, trigger on merge to master