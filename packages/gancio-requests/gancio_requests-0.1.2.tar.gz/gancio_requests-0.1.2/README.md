# gancio_requests
`gancio_requests` is a tool for making asynchronous HTTP 
requests to the API of a specified Gancio instance. [Gancio](https://gancio.org/) is a shared 
agenda for local communities, a project which wants to provide 
a self-hosted solution to host and organize events.  

This repo aims to supply a convenient set of functions to fetch
data from a gancio instance (e.g. scheduled events, the image or
description of an event).

## Installation
To install the latest version of the library just download 
(or clone) the current project, open a terminal and run the 
following commands:

```
pip install -r requirements.txt
pip install .
```

Alternatively use pip

```python
pip install gancio_requests
```

### Dependencies
At the moment I have tested the library only on _python == 3.10.4_  

The library requires the dependencies specified in _requirements.txt_
and I haven't still tested other versions.

## Usage

### Command line interface

```
python3 -m gancio_requests [-h] gancio_instance
```
_gancio_instance_ is the URL of the instance from which we want
to fetch the data.  

The output displays the list of events starting of 00:00:00 of
the current day. The information about an event is shown this 
way:
```
EVENT_NAME
[STARTING_TIME | END_TIME]
PLACE_NAME - ADDRESS
LIST_OF_TAGS (optional)
EVENT_URL
```
#### Example

##### Input
```
python3 -m gancio_requests https://gancio.cisti.org
```

##### Output
```
Crazy toga party
[2022-08-11 22:30:00 | 2022-08-12 00:00:00]
Colosseo - Piazza del Colosseo, Roma
Tags: ["colosseum", "ancient rome", "toga party"]
https://gancio.cisti.org/crazy-toga-party

Gioco del ponte
[2022-09-10 22:00:00 | 2022-09-10 23:00:00]
Ponte di mezzo - Ponte di Mezzo, 1, 56125 Pisa
https://gancio.cisti.org/gioco-del-ponte
```

### Python library
After the installation, it is possible to use the package
directly from the python interpreter by using 
`import gancio_requests`.

### Caching

It is possible to cache HTTP requests thanks to 
[aiohttp-client-cache](https://aiohttp-client-cache.readthedocs.io/en/latest/).
All the functions shown above have an optional parameter 
called _cache_ which accepts a [_aiohttp_client_cache.backends_](https://aiohttp-client-cache.readthedocs.io/en/latest/backends.html)
object.
```
import asyncio
from aiohttp_client_cache import SQLiteBackend
from gancio_requests.request import get_events

url = 'https://gancio.cisti.org'
params = {"start": 0}
cache = SQLiteBackend(
    cache_name = "Test.db"
)
result = asyncio.run(get_events(url, params, cache=cache)) 
```
