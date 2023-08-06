"""PyTest fixtures for unit tests."""

from pathlib import Path
import pytest


@pytest.fixture
def crd_data(request) -> Path:
    """Provides the path to the `crd_data` folder.

    This folder contains simple, small CRD files with real data for testing.

    :return: Path to the folder
    """
    curr = Path(request.fspath).parents[0]
    return Path(curr).joinpath("crd_data").absolute()


@pytest.fixture
def legacy_files_path(request) -> Path:
    """Provides the path to the `legacy_files` folder.

    :return: Path to the folder
    """
    curr = Path(request.fspath).parents[0]
    return Path(curr).joinpath("legacy_files").absolute()


@pytest.fixture
def macro_path(request) -> Path:
    """Provides the path to this folder where the macros are.

    :return: Path to the folder
    """
    return Path(request.fspath).parents[0].absolute().joinpath("macro/")
