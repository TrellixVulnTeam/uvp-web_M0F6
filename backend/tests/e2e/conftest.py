import copy
import os
import tarfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def xserver(pg_container, xserver_factory, pytestconfig, settings):
    _environ = copy.copy(os.environ)
    _environ.update(
        dict(
            PYTHONPATH=os.path.abspath(pytestconfig.rootdir),
            PYTHONDONTWRITEBYTECODE="1",
            POSTGRES_HOST=pg_container.name,
            POSTGRES_USER=settings.DATABASE_URL.user,
            POSTGRES_DB=settings.DATABASE_URL.path.strip("/"),
        )
    )
    with xserver_factory(
        appstr="app.main:app",
        env=_environ,
        host="0.0.0.0",
        port=8001,
        raise_if_used_port=True,
    ) as _xserver:
        yield _xserver


@pytest.fixture
def retrieve_from_workdir(pytestconfig, tmp_path):
    def _retrieve_from_workdir(container, rel_path):
        archive_src = Path(container.attrs["Config"]["WorkingDir"]) / rel_path
        archive_dest = tmp_path / rel_path
        extract_dest = Path(pytestconfig.rootdir) / rel_path
        stream, _ = container.get_archive(archive_src)
        with open(archive_dest, "wb") as f:
            for chunk in stream:
                f.write(chunk)
        with tarfile.open(archive_dest, "r") as f:
            f.extractall(pytestconfig.rootdir)
        return extract_dest

    yield _retrieve_from_workdir
