from io import BufferedReader

import aiofiles
from aiofiles import base, threadpool
from unittest import mock
from pyfakefs import fake_filesystem
import anyio

import pytest


@pytest.mark.asyncio
async def test_plugin_dispatcher(fs):
    with open('test', 'w') as f:
        wrapped = threadpool.wrap(f)

    assert isinstance(f, fake_filesystem.FakeFileWrapper)
    assert isinstance(wrapped, base.AsyncBase)


@pytest.mark.asyncio
@mock.patch.object(fake_filesystem.FakeFileWrapper, 'seek')
async def test_plugin_fixture(mock_write, afs):
    filename = 'test'
    value = 0

    async with aiofiles.open(filename, 'w') as f:
        await f.seek(value)

    assert afs.exists(filename)

    mock_write.assert_called_with(value)

@pytest.mark.asyncio
async def test_plugin_urandom(afs):
    async with aiofiles.open('/dev/urandom', 'rb') as f:
        assert isinstance(f, aiofiles.threadpool.binary.AsyncBufferedIOBase )
    
    with open('blah', 'wb') as f:
        assert isinstance(f, fake_filesystem.FakeFileWrapper)
        f.write(b'hello')
    
    async with aiofiles.open('blah', 'rb') as f:
        assert isinstance(f, aiofiles.threadpool.binary.AsyncBufferedIOBase)
        b = await f.read()
        assert b == b'hello'

    with open('/dev/urandom', 'rb') as f:
        assert isinstance(f, BufferedReader)

    with open('blah', 'rb') as f:
        assert isinstance(f, fake_filesystem.FakeFileWrapper)

    assert await anyio.Path('blah').exists()
    b = await anyio.Path('blah').read_bytes()
    assert b == b'hello'
