# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-29 07:33:02
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 16:27:57

from orb.web.app import serve as web_serve
from typing import Optional
import typer

app = typer.Typer()


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="The allowed host."),
    port: int = typer.Option(8080, help="The port to serve."),
    reload: bool = typer.Option(False, help="Live reloading (dev)."),
    debug: bool = typer.Option(False, help="Show debug info (dev)."),
    workers: int = typer.Option(1, help="Number of web workers."),
):
    """
    Serve the Orb web app.
    """
    web_serve(host=host, port=port, reload=reload, debug=debug, workers=workers)
