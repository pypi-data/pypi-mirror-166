import asyncio
import logging
import shlex
import subprocess
import uuid
from asyncio.subprocess import Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextlib import contextmanager
from typing import Callable, Generator, Optional

import rosys

process_pool = ProcessPoolExecutor()
thread_pool = ThreadPoolExecutor(thread_name_prefix='run.py thread_pool')
running_cpu_bound_processes: list[int] = []  # NOTE is used in tests to advance time slower until computation is done
running_sh_processes: list[Process] = []
log = logging.getLogger('rosys.run')


async def io_bound(callback: Callable, *args: any):
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(thread_pool, callback, *args)
    except RuntimeError as e:
        if 'cannot schedule new futures after shutdown' not in str(e):
            raise
    except asyncio.exceptions.CancelledError:
        pass


async def cpu_bound(callback: Callable, *args: any):
    with cpu():
        try:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(process_pool, callback, *args)
        except RuntimeError as e:
            if 'cannot schedule new futures after shutdown' not in str(e):
                raise
        except asyncio.exceptions.CancelledError:
            pass


@contextmanager
def cpu() -> Generator[None, None, None]:
    id = str(uuid.uuid4())
    running_cpu_bound_processes.append(id)
    try:
        yield
    finally:
        running_cpu_bound_processes.remove(id)


async def sh(command: list[str] | str, timeout: Optional[float] = 1, shell: bool = False) -> str:
    '''executes a shell command

    Args:
        command: a sequence of program arguments as subprocess.Popen requires or full string
        shell: whether a subshell should be launched (default is `False`, for speed, use `True` if you need file globbing or other features)

    Returns:
        stdout
    '''
    def popen() -> str:
        if shell:  # convert to string
            cmd = ' '.join(command) if isinstance(command, list) else command
        else:  # convert to list
            cmd = shlex.split(command) if isinstance(command, str) else command
        if timeout is not None:
            if shell:
                cmd = f'timeout {timeout} {cmd}'
            else:
                cmd = ['timeout', str(timeout)] + cmd
        #log.info(f'running sh: "{cmd}"')
        proc = subprocess.Popen(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            shell=shell,
        )
        running_sh_processes.append(proc)
        stdout, *_ = proc.communicate()
        proc.kill()
        running_sh_processes.remove(proc)
        return stdout.decode('utf-8')
    return await io_bound(popen)


def tear_down() -> None:
    # stopping process as described in https://www.cloudcity.io/blog/2019/02/27/things-i-wish-they-told-me-about-multiprocessing-in-python/
    log.info('teardown thread_pool')
    thread_pool.shutdown(wait=False, cancel_futures=True)
    [p.join(2) for p in running_sh_processes]
    [p.terminate() for p in running_sh_processes if p.is_alive()]
    running_sh_processes.clear()
    if not rosys.is_test:
        log.info('teardown process_pool')
        [p.kill() for p in process_pool._processes.values()]
        process_pool.shutdown(wait=True, cancel_futures=True)
    log.info('teardown complete')
