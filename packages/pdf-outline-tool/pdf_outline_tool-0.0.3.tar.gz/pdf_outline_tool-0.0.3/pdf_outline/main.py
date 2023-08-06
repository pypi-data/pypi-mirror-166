import click

from .pdf import gen_toc_from_pdf, gen_pdf_with_toc


@click.command()
@click.option(
    "--offset",
    default=0,
    show_default=True,
    help="Add offset to the extracted page numbers",
)
@click.option(
    "--indentation",
    default=2,
    show_default=True,
    help="Indentation used for nested outlines",
)
@click.option(
    "--delimiter",
    default="::",
    show_default=True,
    help="Delimiter used to separate outline name and page",
)
@click.argument("pdf")
@click.argument("txt")
def ext(pdf, txt, offset, indentation, delimiter):
    """Extract pdf outline to a text file"""
    gen_toc_from_pdf(pdf, txt, offset, indentation, delimiter)


@click.command()
@click.option(
    "--indentation",
    default=2,
    show_default=True,
    help="Indentation used for nested outlines",
)
@click.option(
    "--delimiter",
    default="::",
    show_default=True,
    help="Delimiter used to separate outline name and page",
)
@click.argument("pdf")
@click.argument("new_pdf")
@click.argument("txt")
def add(pdf, new_pdf, txt, indentation, delimiter):
    """Add pdf outline based on a text file"""
    gen_pdf_with_toc(pdf, new_pdf, txt, indentation, delimiter)


@click.group()
def potl():
    """Extract or add pdf outline based on a text file"""
    pass


potl.add_command(ext)
potl.add_command(add)
