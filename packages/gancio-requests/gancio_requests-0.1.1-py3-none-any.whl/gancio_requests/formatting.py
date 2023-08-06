from datetime import datetime
from bs4 import BeautifulSoup


__all__ = [
	"format_event_info",
	"html2text"
]


def html2text(html_content: str) -> str:
	"""
	Transforms a string containing html code and tags in plain text

	:param html_content: the html code
	:type html_content: str
	
	:return: the text inside the html code
	:rtype: str
	"""
	return BeautifulSoup(html_content, "html.parser").get_text("\n")


def format_event_info(event: dict, instance_url: str = None) -> str:
	"""
	Given the information about an event fetched from the API, formats  it in a more readable way.

	:param event: event information fetched from the API.
	:type: dict

	:param instance_url: optional, the instance url from which the data was fetched. \
	If this param is specified, then the event url is added to the infos
	:type instance_url: str

	:return: the event information.
	:rtype: str
	"""
	def format_timestamp(timestamp: float): return str(datetime.fromtimestamp(timestamp))
	title = event["title"]
	slug = event["slug"]
	start_datetime = format_timestamp(event["start_datetime"])
	end_datetime = format_timestamp(event["end_datetime"])
	tags = event["tags"]
	place = event["place"]["name"]
	address = event["place"]["address"]

	formatted_string = ""
	formatted_string += f"{title}\n"
	formatted_string += f"[{start_datetime} | {end_datetime}]\n"
	formatted_string += f"{place} - {address}\n"
	if tags != []:
		formatted_string += f"Tags: {tags}\n"
	if instance_url is not None:
		formatted_string += f"{instance_url}/{slug}\n"
	return formatted_string
