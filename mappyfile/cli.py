import sys
import os
import glob
import logging
import mappyfile
import click


def configure_logging(verbosity):
    """
    Configure logging level

    Parameters
    ----------
    verbosity : int
        The number of `-v` options from the command line.
    Returns
    -------
    None
    """
    log_level = max(10, 30 - 10 * verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


logger = logging.getLogger(__name__)
# The CLI command group.
@click.group(help="Command line interface for the mappyfile package")
@click.option('--verbose', '-v', count=True, help="Increase verbosity")
@click.option('--quiet', '-q', count=True, help="Decrease verbosity")
@click.version_option(version=mappyfile.__version__, message='%(version)s')
@click.pass_context
def main(ctx, verbose, quiet):
    """
    Execute the main mappyfile command
    """
    verbosity = verbose - quiet
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj['verbosity'] = verbosity


@main.command(short_help="Validate a Mapfile against a schema")
@click.argument('mapfiles',  nargs=-1, type=click.Path()) # exists=True
@click.option('--no-expand', is_flag=True, default=False)
@click.pass_context
def validate(ctx, mapfiles, no_expand):
    """
    mappyfile validate C:\Temp\valid.map
    """
    all_mapfiles =  [mf for sublist in mapfiles for mf in glob.glob(sublist) if not os.path.isdir(mf)]

    if len(all_mapfiles) == 0:
        click.echo("No Mapfiles found in the following locations: {}!".format(",".join(mapfiles)))
        return

    validation_count = 0

    for fn in all_mapfiles:
        fn = click.format_filename(fn)
        if not os.path.isfile(fn):
            click.echo("{} does not exist!".format(fn))
        else:
            d = mappyfile.open(fn, expand_includes=not no_expand, include_position=True)
            validation_messages = mappyfile.validate(d)
            if validation_messages:
                for v in validation_messages:
                    v["fn"] = fn
                    msg = "{fn} (Line: {line} Column: {column}) {message} - {error}".format(**v)
                    click.echo(msg)
            else:
                click.echo("{} validated successfully".format(fn))
                validation_count += 1

    click.echo("{} file(s) validated".format(validation_count))