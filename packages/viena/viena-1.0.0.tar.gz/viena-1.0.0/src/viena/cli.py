"""This module provides the CLI."""
# cli-module/cli.py

from pathlib import Path
from typing import List, Optional
import typer
import time
from viena import __app_name__, __version__,rest_connect
# import dataset
# import container

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()

def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def add(configfile:str = typer.Option("None","--configfile","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: configure  """
        f"""pass apikey and jsonfile to configure""",
        fg=typer.colors.GREEN,
    )
    if(configfile!=None):
      status=rest_connect.configuredetails(configfile)
      print(status)
    else:
        print("Please pass configfile path")

@app.command()
def update(configfile:str = typer.Option("None","--configfile","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: update  """
        f"""pass  configfile to update""",
        fg=typer.colors.GREEN,
    )
    if(configfile!=None):
      status=rest_connect.updatedetails(configfile)
      print(status)
    else:
        print("Please pass apikey and jsonfile path")

@app.command()
def logs():
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: logs  """ ,
        fg=typer.colors.GREEN,
    )
    while True:
        status = rest_connect.getlogs()
        print(status)
        time.sleep(5)

@app.command()
def summarydetails(videoid:str = typer.Option("None","--videoid","--n"),
        videopath:str = typer.Option("None","--videopath","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: summarydetails  """
        f"""pass videoid or videopath to get the summary""",
        fg=typer.colors.GREEN,
    )
    if (videoid != "None" or videopath != "None"):
        status = rest_connect.getsummarydetails(videoid, videopath)
        print(status)


@app.command()
def framedetails(path:str = typer.Option("None","--path","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: summarydetails  """
        f"""pass videoid or videopath to get the summary""",
        fg=typer.colors.GREEN,
    )
    if (path != "None"):
        status = rest_connect.getframedetails(path)
        print(status)



@app.command()
def frameimage(path:str = typer.Option("None","--path","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: frameimage  """ ,
        fg=typer.colors.GREEN,
    )
    if (path != "None"):
        status = rest_connect.getframeimage(path)
        print(status)



@app.command()
def getvideoid():
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: getvideoid  """ ,
        fg=typer.colors.GREEN,
    )
    status=rest_connect.getvideoid()
    print(status)


@app.command()
def getframespath(videoid:str = typer.Option("None","--videoid","--n"),
        videopath:str = typer.Option("None","--videopath","--n"),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""viena: getframespath  """
        f"""pass videoid or videopath to get the summary""",
        fg=typer.colors.GREEN,
    )
    if (videoid != "None" or videopath != "None"):
        status = rest_connect.getframespathfromDB(videoid, videopath)
        print(status)