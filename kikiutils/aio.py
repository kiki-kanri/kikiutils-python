import signal

from asyncio import AbstractEventLoop, all_tasks, Future, get_event_loop, sleep

from .log import logger


def run_loop_forever_and_wait_signals(loop: AbstractEventLoop = None, clean_up: bool = True):
    """
    Run an event loop indefinitely until receiving a SIGINT or SIGTERM signal.

    If clean_up is True, cancels all tasks and stops then closes the loop.

    Args:
    loop (AbstractEventLoop, optional): The event loop to run. If not provided, it gets the current event loop.
    clean_up (bool, optional): A flag to determine if the loop should be cleaned up (tasks cancelled, loop stopped and closed) after termination. Defaults to True.
    """

    if loop is None:
        loop = get_event_loop()

    future = Future(loop=loop)
    signal_handler = lambda: future.done() or future.set_result(None)
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)
    loop.run_until_complete(future)

    if clean_up:
        while tasks := [t for t in all_tasks(loop) if not t.cancelled()]:
            logger.info(f'Waiting for {len(tasks)} tasks stop...')
            [task.cancel() for task in tasks]
            loop.run_until_complete(sleep(1))

        loop.stop()
        loop.close()
