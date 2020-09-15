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
@click.option('-i', '--iterations', type=int, default=1000, show_default=True, help='Number of times the program calculates this number in each batch')
@click.option('--parallel/--no-parallel', default=True, help='Turn parallel processing on/off [default:  off]')
@click.option('--num_processes', type=int, help='Number of parallel processes to launch [default: number of cores]')
@click.option('--log-level', help='Log level (e.g., warning, info, debug, etc.)')
def fibonacci_test(
    n,
    iterations,
    parallel,
    num_processes,
    log_level
):
    rpi_monitor.tests.fibonacci_test(
        n=n,
        iterations=iterations,
        parallel=parallel,
        num_processes=num_processes,
        log_level=log_level
    )


@click.command()
@click.option('-d', '--delay', type=int, default=5, show_default=True, help='Number of seconds to wait before returning')
@click.option('--num_processes', type=int, help='Number of parallel processes to launch [default: number of cores]')
@click.option('--log-level', help='Log level (e.g., warning, info, debug, etc.)')
def sleep_test(
    delay,
    num_processes,
    log_level=None
):
    rpi_monitor.tests.sleep_test(
        delay=delay,
        num_processes=num_processes,
        log_level=log_level
    )
