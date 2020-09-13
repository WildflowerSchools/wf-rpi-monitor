import rpi_monitor.core
import click


@click.command()
@click.option('-i', '--interval', type=int, default=30, show_default=True, help='Number of seconds between data points')
@click.argument('path', type=click.Path(exists=False))
def log_rpi_status(
    path,
    interval
):
    rpi_monitor.core.log_rpi_status_csv(
        path,
        interval
    )
