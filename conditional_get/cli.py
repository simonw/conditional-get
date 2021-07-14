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
@click.option("--key", help="Key to lookup ETag in etags.json - defaults to the URL")
@click.option("-v", "--verbose", help="Verbose output", is_flag=True)
def cli(url, output, etags, key, verbose):
    """
    Fetch data using HTTP conditional get
    """
    headers = {}
    key = key or url
    try:
        existing_etags = json.load(open(etags))
    except IOError:
        existing_etags = {}
    if key in existing_etags:
        headers["If-None-Match"] = existing_etags[key]
        if verbose:
            click.echo("Existing ETag: {}".format(existing_etags[key]), err=True)
    with httpx.stream("GET", url, headers=headers) as response:
        if verbose:
            click.echo(
                "Response status code: {}".format(response.status_code), err=True
            )
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
                existing_etags[key] = etag
            bar = None
            if verbose and response.headers.get("content-length"):
                bar = click.progressbar(length=int(response.headers["content-length"]))
            with open(output, "wb") as fp:
                for b in response.iter_bytes():
                    fp.write(b)
                    if bar:
                        bar.update(len(b))
            open(etags, "w").write(json.dumps(existing_etags, indent=4))
