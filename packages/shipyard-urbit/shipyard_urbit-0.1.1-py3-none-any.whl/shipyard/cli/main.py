import typer

from shipyard.api.main import gunicorn_full, uvicorn_local
from shipyard.envoy.tunnel import open_tunnel
from shipyard.models import SshRemote


app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    Urbit hosting and automation platform
    """
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@app.command()
def api(
    host: str = typer.Option("127.0.0.1", help="Host the server will listen on"),
    port: int = typer.Option("8000", help="Port the server will listen on"),
    log_level: str = typer.Option("info", help="Logging level of the server"),
    full: bool = typer.Option(False, help="Run a full multi-worker Gunicorn server"),
):
    """
    Run a local API server
    """
    if full:
        gunicorn_full()
    else:
        uvicorn_local(host=host, port=port, log_level=log_level)


@app.command()
def tunnel(
    host: str = typer.Option(
        ..., "--host", "-h", help="Hostname of the remote SSH server"
    ),
    user: str = typer.Option(
        ..., "--user", "-u", help="Username to login to remote SSH server"
    ),
    port: int = typer.Option(
        22, "--port", "-p", help="Listening port of the remote SSH server"
    ),
    local_port: int = typer.Option(
        4000, "--local-port", "-L", help="Local port to forward application to"
    ),
    remote_port: int = typer.Option(
        4000, "--remote-port", "-R", help="Remote application port to forward"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Silence informational output"
    ),
):
    """
    Open an SSH tunnel to remote ship, allows you to connect on local port
    """

    ssh: SshRemote = SshRemote(url=f"ssh://{user}@{host}:{port}")  # pyright:ignore
    open_tunnel(ssh, local_port, remote_port, quiet)
