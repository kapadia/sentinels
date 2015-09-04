
import json
import click
from sentinels import api


raw_opt = click.option("--raw", is_flag=True, help="Return the raw form response.")


@click.group()
def sentinels():
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
@click.option('--offset', default=0, help='The number of rows to offset the results')
@click.option('--satellite', help='The satellite platform name (e.g. Sentinel-1)')
@click.option('--begin-position', nargs=2, help='A time interval search based on the sensing start time')
@click.option('--end-position', nargs=2, help='A time interval search based on the sensing end time')
@click.option('--start-date', nargs=1, help='The start time of publication of the product on the Data Hub')
@click.option('--end-date', nargs=1, help='The end time of publication of the product on the Data Hub')
@click.option('--filename', nargs=1, help='The product filename')
@click.option('--orbit-number', nargs=1, help='Absolute orbit number of the oldest line within the image data')
@click.option('--last-orbit-number', nargs=1, help='Absolute orbit number of the most recent line within the image data')
@click.option('--orbit-direction', nargs=1, type=click.Choice(['ascending', 'descending']), help='Direction of the orbit')
@click.option('--polarisation-mode', '--polarization-mode', type=click.Choice(['HH', 'VV', 'HV', 'VH', 'HH HV', 'VV VH']), help='Polarizations for the S1 SAR instrument')
@click.option('--product-type', type=click.Choice(['SLC', 'GRD', 'OCN', 'S2MSI1C']))
@click.option('--relative-orbit-number', help='Relative orbit number of the oldest line within the image data')
@click.option('--last-relative-orbit-number', help='Relative orbit number of the most recent line within the image data')
@click.option('--sensor-operational-mode', type=click.Choice(['SM', 'IW', 'EW']), help='The SAR instrument imaging modes')
@click.option('--swath-identifier', type=click.Choice(['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'IW', 'IW1', 'IW2', 'IW3', 'EW', 'EW1', 'EW2', 'EW3', 'EW4', 'EW5']), help='Search all valid swath identifiers for the Sentinel-1 SAR instrument. The S1-S6 swaths apply to SM products, the IW and IW1-3 swaths apply to IW products (IW is used for detected IW products where the 3 swaths are merged into one image), the EW and EW1-5 swaths apply to EW products (EW is used for detected EW products where the 5 swaths are merged into one image).')
def search(aoi, rows, offset, satellite, begin_position, end_position, start_date, end_date, filename, orbit_number, last_orbit_number, orbit_direction, polarization_mode, product_type, relative_orbit_number, last_relative_orbit_number, sensor_operational_mode, swath_identifier):
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
    
    click.echo(json.dumps(api.search(
        aoi=geojson, rows=rows, offset=offset, platformname=satellite, begin_position=begin_position,
        end_position=end_position, start_date=start_date, end_date=end_date, filename=filename,
        orbit_number=orbit_number, last_orbit_number=last_orbit_number, orbit_direction=orbit_direction,
        polarization_mode=polarization_mode, product_type=product_type, relative_orbit_number=relative_orbit_number,
        last_relative_orbit_number=last_relative_orbit_number, sensor_operational_mode=sensor_operational_mode,
        swath_identifier=swath_identifier
    )))


sentinels.add_command(ping)
sentinels.add_command(metadata_service)
sentinels.add_command(collections)
sentinels.add_command(search)