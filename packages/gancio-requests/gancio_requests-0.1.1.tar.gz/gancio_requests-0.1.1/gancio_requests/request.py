import aiohttp
import aiohttp_client_cache
from bs4 import BeautifulSoup


__all_ = [
	"get_event_description",
	"get_event_image",
	"get_events"
]


async def get_event_description(
	instance_url: str,
	event_slug: str,
	cache: "CacheBackend" = None
) -> dict:
	"""
	Fetches the html description of an event using the event slug

	:param instance_url: URL of the Gancio instance where the event is saved
	:type instance_url: str
	:param event_slug: the slug of the event to fetch
	:type event_slug: str
	:param cache: optional, the cache to use to save/fetch the http requests
	:type cache: CacheBackend
	:return: the response status code (key: "status") and the event html descritpion (key:"html_content")
	:rtype: dict

	:Example:

	>>> import asyncio
	>>> from gancio_requests.request import get_event_description
	>>> from aiohttp_client_cache import SQLiteBackend
	>>>
	>>> url = "https://gancio.cisti.org"
	>>> event_slug = "jazz-in-jardino-2"
	>>> cache = SQLiteBackend(
	...     cache_name = "aio-requests.db"
	... )
	>>>
	>>> result = asyncio.run(get_event_description(url, event_slug, cache))
	"""
	url = f"{instance_url}/event/{event_slug}"

	if cache is None:
		session = aiohttp.ClientSession()
	else:
		session = aiohttp_client_cache.CachedSession(cache=cache)

	try:
		async with session.get(url) as response:
			if response.status != 200:
				description_string = ""
			else:
				html_full_content = await response.text()

				html_soup = BeautifulSoup(html_full_content, "html.parser")
				description_html_div = html_soup.find("div", {"class": "p-description text-body-1 pa-3 rounded"})
				if description_html_div is None:
					description_string = ""
				else:
					description_string = str(description_html_div)

			return {
				"status": response.status,
				"html_content": description_string
			}
	finally:
		await session.close()


async def get_event_image(
		instance_url: str,
		image_name: str,
		cache: "CacheBackend" = None
) -> dict:
	"""
	Fetches the image of specified event.

	:param instance_url: the URL of the Gancio instance where the event is saved
	:type instance_url: str
	:param image_name: the name and file extension suffix of the image to fetch
	:type image_name: str
	:param cache: optional, the cache to use to save/fetch the http requests
	:type cache: CacheBackend
	:return: the response status code (key: "status") and the image bytes (key:"content")
	:rtype: dict

	:Example:

	>>> import asyncio
	>>> from gancio_requests.request import get_event_image
	>>> from aiohttp_client_cache import SQLiteBackend
	>>>
	>>> url = "https://gancio.cisti.org"
	>>> image_name = "072e0caedb51e352c43813376b59b26d.jpg"
	>>> cache = SQLiteBackend(
	...     cache_name = "aio-requests.db"
	... )
	>>>
	>>> res = asyncio.run(get_event_image(url, image_name, cache))
	"""
	url = f"{instance_url}/media/thumb/{image_name}"

	if cache is None:
		session = aiohttp.ClientSession()
	else:
		session = aiohttp_client_cache.CachedSession(cache=cache)

	try:
		async with session.get(url) as response:
			return {
				"status": response.status,
				"content": await response.read()
			}
	finally:
		await session.close()


async def get_events(
		instance_url: str,
		params: dict = None,
		cache: "CacheBackend" = None
) -> dict:
	"""
	Fetches the events saved on the specified Gancio instance using the specified url parameters.
	Information about the available URL parameters can be found at https://gancio.org/dev/api

	:param instance_url: URL of the Gancio instance where the event is saved
	:type instance_url: str
	:param params: optional, dictionary specifying for each URL parameter (key) its value (value)
	:type params: dict
	:param cache: optional, the cache to use to save/fetch the http requests
	:type cache: CacheBackend
	:return: the response status code (key: "status") and the list of events information (key:"json_content")
	:rtype: dict

	:Example:

	>>> import asyncio
	>>> from gancio_requests.request import get_events
	>>> from aiohttp_client_cache import SQLiteBackend
	>>>
	>>> url = "https://gancio.cisti.org"
	>>> # for this example we want to fetch all the events
	>>> # starting from 1-1-1970 00:00:00
	>>> params = {"start": 0}
	>>> cache = SQLiteBackend(
	...     cache_name = "aio-requests.db"
	... )
	>>> result = asyncio.run(get_events(url, params, cache))
	"""
	url = f"{instance_url}/api/events"

	if cache is None:
		session = aiohttp.ClientSession()
	else:
		session = aiohttp_client_cache.CachedSession(cache=cache)

	try:
		async with session.get(url, params=params) as response:
			return {
				"status": response.status,
				"json_content": await response.json()
			}
	finally:
		await session.close()
