from aiofiles import threadpool
from aiofiles.threadpool.binary import AsyncBufferedIOBase
from pyfakefs.fake_filesystem import FakeFileWrapper
from pyfakefs.fake_filesystem_unittest import Patcher
import pytest
import anyio
import os

def find_sync_open_attr():
    # fixme: depend on 0.3.2
    try:
        getattr(threadpool, 'sync_open')
        return 'sync_open'  # pragma: no cover
    except AttributeError as e:  # pragma: no cover
        try:
            getattr(threadpool, '_sync_open')
            return '_sync_open'
        except AttributeError:
            raise e


@pytest.fixture(scope="session")
def afs(request):
    """ Fake filesystem. """
    patcher = Patcher()
    patcher.setUp()

    threadpool._sync_open = open

    request.addfinalizer(patcher.tearDown)

    return patcher.fs


@threadpool.wrap.register(FakeFileWrapper)
def _(file, *, loop=None, executor=None):
    return AsyncBufferedIOBase(file, loop=loop, executor=executor)
