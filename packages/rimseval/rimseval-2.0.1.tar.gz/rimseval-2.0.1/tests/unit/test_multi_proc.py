"""Multi processor unit tests."""

from pathlib import Path

import pytest
import numpy as np

from rimseval.multi_proc import MultiFileProcessor as mfp


@pytest.mark.parametrize("params", [[True, False], [False, True]])
def test_mfp_apply_to_all(params, crd_file):
    """Apply settings from one crd file to all.

    :param params: Parameters for: bg_corr, opt_mcal
    :param crd_file: CRD file to process.
    """
    _, _, _, fname = crd_file
    files = [Path(fname), Path(fname)]
    id = 0  # id of main crd file
    bg_corr = params[0]

    crds = mfp(files)
    crds.read_files()

    crd_main = crds.files[id]
    crd_main.def_mcal = np.array([[0.1, 10], [0.2, 22], [0.3, 33]])
    crd_main.mass_calibration()
    crd_main.def_integrals = ["Int1"], np.array([[6.0, 7.0]])
    crd_main.def_backgrounds = ["Int1"], np.array([[5.0, 6.0]])
    crd_main.packages(2)
    crd_main.filter_max_ions_per_pkg(5)
    crd_main.integrals_calc(bg_corr=bg_corr)

    # apply to all
    crds.apply_to_all(id=id, opt_mcal=params[1], bg_corr=bg_corr)

    for crd in crds.files:
        np.testing.assert_equal(crd.data, crd_main.data)
        np.testing.assert_equal(crd.mass, crd_main.mass)
        np.testing.assert_equal(crd.tof, crd_main.tof)
        np.testing.assert_equal(crd.data_pkg, crd_main.data_pkg)
        assert crd.nof_shots == crd_main.nof_shots
        np.testing.assert_equal(crd.nof_shots_pkg, crd_main.nof_shots_pkg)
        assert crd.fname.with_suffix(".json").is_file()


def test_mfp_apply_to_all_main_file_not_processed(crd_file):
    """Apply settings from one crd file to all, while one file is not yet processed."""
    _, _, _, fname = crd_file
    files = [Path(fname), Path(fname)]
    id = 0  # id of main crd file
    bg_corr = True

    crds = mfp(files)
    crds.open_files()

    crd_main = crds.files[id]
    crd_main.def_mcal = np.array([[0.1, 10], [0.2, 22], [0.3, 33]])
    crd_main.def_integrals = ["Int1"], np.array([[6.0, 7.0]])
    crd_main.def_backgrounds = ["Int1"], np.array([[5.0, 6.0]])

    # apply to all
    crds.apply_to_all(id=id, opt_mcal=False, bg_corr=bg_corr)

    # assert main file was processed right
    assert crd_main.tof is not None
    assert crd_main.data is not None
    assert crd_main.mass is not None
    assert crd_main.integrals is not None

    for crd in crds.files:
        np.testing.assert_equal(crd.data, crd_main.data)
        np.testing.assert_equal(crd.mass, crd_main.mass)
        np.testing.assert_equal(crd.tof, crd_main.tof)
        np.testing.assert_equal(crd.data_pkg, crd_main.data_pkg)
        assert crd.nof_shots == crd_main.nof_shots
        np.testing.assert_equal(crd.nof_shots_pkg, crd_main.nof_shots_pkg)
        assert crd.fname.with_suffix(".json").is_file()


def test_mfp_load_calibrations(crd_file, crd_data):
    """Load calibrations with primary and secondary file."""
    _, _, _, fname = crd_file
    files = [Path(fname), crd_data.joinpath("ti_standard_01.crd")]

    secondary_cal_file = crd_data.joinpath("ti_standard_01.json")

    crds = mfp(files)
    crds.load_calibrations(secondary_cal=secondary_cal_file)

    for crd in crds.files:
        assert crd.def_mcal is not None  # loading complete
