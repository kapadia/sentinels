
import json
import click
from sentinel import api


raw_opt = click.option("--raw", is_flag=True, help="Return the raw form response.")


@click.group()
def sentinel():
    pass


@click.command('ping')
def ping():
    click.echo(api.ping())


@click.command('metadata-service')
def metadata_service():
    click.echo(api.metadata_service())


@click.command('collections')
@raw_opt
def collections(raw):
    """
    Describe the collections hosted by the Scientific Data Hub.
    """
    data = api.collections(raw=raw)
    click.echo(json.dumps(data))


@click.command('search')
@click.argument("aoi", default="-", required=False)
@click.option('--rows', default=50, help='The number of results to return')
@click.option('--start', default=0, help='The start offset')
def search(aoi, rows, start):
    """
    Describe the products hosted by the Scientific Data Hub.
    """

    geojson = None
    if aoi == "-":
        src = click.open_file('-')
        if not src.isatty():
            geojson = json.loads(src.read())
    else:
        geojson = json.loads(click.open_file(aoi).read())
    
    click.echo(json.dumps(api.search(aoi=geojson, rows=rows, start=start)))

sentinel.add_command(ping)
sentinel.add_command(metadata_service)
sentinel.add_command(collections)
sentinel.add_command(search)