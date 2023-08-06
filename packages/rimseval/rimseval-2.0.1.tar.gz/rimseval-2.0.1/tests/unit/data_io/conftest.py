"""PyTest fixtures for unit tests in data_io."""

import os

from pathlib import Path
import pytest


@pytest.fixture
def crd_data(request) -> Path:
    """Provides the path to the `crd_data` folder.

    This folder contains simple, small CRD files with real data for testing.

    :return: Path to the folder
    """
    curr = Path(request.fspath).parents[0]
    return Path(curr).joinpath("../crd_data").absolute()


@pytest.fixture
def lst_crd_path(request):
    """Provides the path to the `lst_crd_files` folder.

    :return: Path to the folder
    :rtype: Path
    """
    curr = Path(request.fspath).parents[0]
    return Path(curr).joinpath("lst_crd_files").absolute()
