import sys
import os
import codecs
import glob
import logging
import mappyfile
import click


def get_mapfiles(mapfiles):

    all_mapfiles = [mf for sublist in mapfiles for mf in glob.glob(sublist) if not os.path.isdir(mf)]
    return all_mapfiles


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


@main.command(short_help="Format a Mapfile")
@click.argument('input-mapfile', nargs=1, type=click.Path(exists=True))
@click.argument('output-mapfile',  nargs=1, type=click.Path())
@click.option('--indent', default=4, show_default=True, help="The number of spacer characters to indent structures in the Mapfile") # noqa
@click.option('--spacer', default=" ", help="The character to use for indenting structures in the Mapfile")
@click.option('--quote', default='"', help="The quote character to use in the Mapfile (double or single quotes). Ensure these are escaped e.g. \\\" or \\' [default: \\\"]") # noqa
@click.option('--newlinechar', default='\n', help="The character used to insert newlines in the Mapfile [default: \\n]")
@click.option('--expand/--no-expand', default=True, show_default=True, help="Expand any INCLUDE directives found in the Mapfile") # noqa
@click.option('--comments/--no-comments', default=False, show_default=True, help="Keep Mapfile comments in the output (experimental)") # noqa
@click.pass_context
def format(ctx, input_mapfile, output_mapfile, indent, spacer, quote, newlinechar, expand, comments):
    """
    Format a the input-mapfile and save as output-mapfile. Note output-mapfile will be
    overwritten if it already exists.

    Example of formatting a single Mapfile:

        mappyfile format C:/Temp/valid.map C:/Temp/valid_formatted.map

    Example of formatting a single Mapfile with single quotes and tabs for indentation:

        mappyfile format C:/Temp/valid.map C:/Temp/valid_formatted.map --quote=\\' --indent=1 --spacer=\t

    Example of formatting a single Mapfile without expanding includes, but including comments:

        mappyfile format C:/Temp/valid.map C:/Temp/valid_formatted.map --no-expand --comments
    """

    quote = codecs.decode(quote, 'unicode_escape')  # ensure \t is handled as a tab
    spacer = codecs.decode(spacer, 'unicode_escape')  # ensure \t is handled as a tab
    newlinechar = codecs.decode(newlinechar, 'unicode_escape')  # ensure \n is handled as a newline

    d = mappyfile.open(input_mapfile, expand_includes=expand, include_comments=comments, include_position=True)
    mappyfile.save(d, output_mapfile, indent=indent, spacer=spacer, quote=quote, newlinechar=newlinechar)
    sys.exit(0)


@main.command(short_help="Validate Mapfile(s) against a schema")
@click.argument('mapfiles', nargs=-1, type=click.Path())
@click.option('--expand/--no-expand', default=True, show_default=True, help="Expand any INCLUDE directives found in the Mapfile") # noqa
@click.pass_context
def validate(ctx, mapfiles, expand):
    """
    Validate Mapfile(s) against the Mapfile schema

    The MAPFILES argument is a list of paths, either to individual Mapfiles, or a folders containing Mapfiles.
    Wildcards are supported (natively on Linux, and up to one level deep on Windows).
    Validation errors are reported to the console. The program returns the error count - this will be 0 if no
    validation errors are encountered.

    Example of validating a single Mapfile:

        mappyfile validate C:/Temp/valid.map

    Example of validating two folders containing Mapfiles, without expanding INCLUDES:

        mappyfile validate C:/Temp/*.map D:/GitHub/mappyfile/tests/mapfiles/*.map --no-expand
    """

    all_mapfiles = get_mapfiles(mapfiles)

    if len(all_mapfiles) == 0:
        click.echo("No Mapfiles found at the following paths: {}".format(",".join(mapfiles)))
        return

    validation_count = 0
    errors = 0

    for fn in all_mapfiles:
        fn = click.format_filename(fn)
        d = mappyfile.open(fn, expand_includes=expand, include_position=True)

        validation_messages = mappyfile.validate(d)
        if validation_messages:
            for v in validation_messages:
                v["fn"] = fn
                msg = "{fn} (Line: {line} Column: {column}) {message} - {error}".format(**v)
                click.echo(msg)
                errors += 1
        else:
            click.echo("{} validated successfully".format(fn))
            validation_count += 1

    click.echo("{} file(s) validated ({} successfully)".format(len(all_mapfiles), validation_count))
    sys.exit(errors)
