import click
import httpx
import json
import time
from urllib.parse import urlparse

CONTENT_TYPE_TO_EXT = {
    "text/html": "html",
    "text/plain": "txt",
}


@click.command()
@click.version_option()
@click.argument("url", type=str, required=True)
@click.option("-o", "--output", help="Filename to save to")
@click.option(
    "--etags", help="File to store ETags, defaults to etags.json", default="etags.json"
)
@click.option("-v", "--verbose", help="Verbose output", is_flag=True)
def cli(url, output, etags, verbose):
    """
    Fetch data using HTTP conditional get
    """
    headers = {}
    try:
        existing_etags = json.load(open(etags))
    except IOError:
        existing_etags = {}
    if url in existing_etags:
        headers["If-None-Match"] = existing_etags[url]
        if verbose:
            click.echo("Existing ETag: {}".format(existing_etags[url]), err=True)
    response = httpx.get(url, headers=headers)
    if verbose:
        click.echo("Response status code: {}".format(response.status_code), err=True)
    if not output:
        # Detect output from URL and content_type
        bits = urlparse(url)
        output = bits.path.split("/")[-1]
        if not output:
            # Use index.filetype
            content_type = response.headers["content-type"].split()[0]
            ext = CONTENT_TYPE_TO_EXT.get(content_type, content_type.split("/")[-1])
            output = "index.{}".format(ext)

    if 304 == response.status_code:
        return
    elif 200 == response.status_code:
        etag = response.headers.get("etag")
        if etag:
            existing_etags[url] = etag
        open(etags, "w").write(json.dumps(existing_etags, indent=4))
        open(output, "wb").write(response.content)
