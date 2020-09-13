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

@click.command()
@click.option('-n', type=int, default=10000, show_default=True, help='Fibonacci number to repeatedly calculate')
@click.option('--num_processes', type=int, help='Number of parallel processes to launch [default: number of cores]')
def fibonacci_test(
    n,
    num_processes
):
    rpi_monitor.tests.fibonacci_test(
        n=n,
        num_processes=num_processes
    )
