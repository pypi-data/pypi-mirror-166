"""Function test for processor class methods, focusing on each function."""

import datetime
from pathlib import Path

import pytest
import numpy as np

from rimseval.processor import CRDFileProcessor
import rimseval.processor_utils as pu

# TEST PROPERTIES #


def test_integrals_overlap(crd_file):
    """Check if integrals overlap and return bools."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))

    assert not crd.integrals_overlap

    crd.def_integrals = ["p1", "p2"], np.array([[1, 2], [3, 4]])
    assert not crd.integrals_overlap


def test_timestamp(crd_file):
    """Get the time stamp of the CRD file as a python datetime."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    timestamp = crd.timestamp
    assert isinstance(timestamp, datetime.datetime)


# TEST METHODS #


@pytest.mark.parametrize("ind", [0, 1])
def test_adjust_overlap_background_peaks(ind, crd_file, mocker):
    """Ensure the correct return is chosen and set, plus warning raised if required."""
    corrs_exp = (["p1"], np.array([[2, 3]])), (["p1"], np.array([[5, 6]]))
    mocker.patch(
        "rimseval.processor_utils.peak_background_overlap",
        return_value=(corrs_exp[0], corrs_exp[1]),
    )

    warn_msg = "Your backgrounds have overlaps with peaks other than themselves."

    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))

    crd.def_backgrounds = (["p1"], np.array([[1, 9]]))
    crd.def_integrals = (["p1"], np.array([[2.9, 3.2]]))

    if ind == 0:  # expect a warning
        with pytest.warns(UserWarning, match=warn_msg):
            crd.adjust_overlap_background_peaks(other_peaks=bool(ind))
    else:
        crd.adjust_overlap_background_peaks(other_peaks=bool(ind))

    assert crd.def_backgrounds[0] == corrs_exp[ind][0]
    np.testing.assert_almost_equal(crd.def_backgrounds[1], corrs_exp[ind][1])


def test_adjust_overlap_background_peaks_do_nothing(crd_file):
    """Do nothing if backgrounds or integrals are not defined."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.adjust_overlap_background_peaks()


def test_data_dimension_after_dead_time_correction(crd_file):
    """Ensure ToF and data have the same dimensions - BF 2021-07-23."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.dead_time_correction(3)

    assert crd.tof.ndim == crd.data.ndim


def test_filter_max_ions_per_pkg(crd_file):
    """Filter the packages by maximum ion."""
    _, ions_per_shot, _, fname = crd_file
    max_ions = ions_per_shot.max() - 1  # filter one or so packages out
    sum_ions = 0
    for ion in ions_per_shot:
        if ion <= max_ions:
            sum_ions += ion

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.packages(1)
    crd.filter_max_ions_per_pkg(max_ions)
    assert crd.data_pkg.sum() == sum_ions


def test_filter_max_ions_per_shot(crd_file):
    """Filter the shots by maximum ions per shot."""
    _, ions_per_shot, _, fname = crd_file
    max_ions = ions_per_shot.min() + 1  # filter most out
    filtered_data = ions_per_shot[np.where(ions_per_shot <= max_ions)]
    sum_ions_exp = np.sum(filtered_data)
    nof_shots_exp = len(filtered_data)

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_shot(max_ions)

    assert crd.nof_shots == nof_shots_exp
    assert crd.data.sum() == sum_ions_exp
    np.testing.assert_equal(crd.ions_per_shot, filtered_data)


def test_filter_max_ions_per_shot_double(crd_file):
    """Test filterting max ions per shot twice (no pkgs)."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions1 = max(ions_per_shot) - 1  # filter the highest one out
    max_ions2 = min(ions_per_shot) + 1

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_shot(max_ions1)
    crd.filter_max_ions_per_shot(max_ions2)

    ions_per_shot_filtered = ions_per_shot[np.where(ions_per_shot <= max_ions2)]
    nof_shots = len(ions_per_shot_filtered)
    nof_ions = np.sum(ions_per_shot_filtered)

    assert crd.nof_shots == nof_shots
    assert np.sum(crd.data) == nof_ions


def test_filter_max_ions_per_shot_pkg(crd_file):
    """Test maximum ions per shot filtering with packages."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions = max(ions_per_shot) - 1  # filter the highest one out
    shots_per_pkg = 2

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.packages(shots_per_pkg)
    crd.filter_max_ions_per_shot(max_ions)

    # assert that package data are the same as the rest
    assert crd.nof_shots == crd.nof_shots_pkg.sum()
    assert crd.data.sum() == crd.data_pkg.sum()


def test_filter_max_ions_per_shot_pkg_filtered(crd_file):
    """Test maximum ions per shot filtering with packages and pkg filter applied."""
    header, ions_per_shot, all_tofs, fname = crd_file
    shots_per_pkg = 2
    max_ions = 1
    max_ions_per_pkg = 4

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.packages(shots_per_pkg)
    crd.filter_max_ions_per_pkg(max_ions_per_pkg)
    crd.filter_max_ions_per_shot(max_ions)

    # assert that package data are the same as the rest
    assert crd.nof_shots == crd.nof_shots_pkg.sum()
    assert crd.data.sum() == crd.data_pkg.sum()


def test_filter_max_ions_per_time(crd_file):
    """Test maximum ions per shot in given time window."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions = 1  # filter the highest one out
    time_window_us = 39 * 100 / 1e6  # 40 channels, filters third but not fifth

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_time(max_ions, time_window_us)

    assert crd.nof_shots == len(ions_per_shot) - 1
    assert np.sum(crd.data) == np.sum(ions_per_shot) - 4


def test_filter_max_ions_per_time_nothing(crd_file):
    """Do nothing if filter shows no entries for removal."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions = ions_per_shot.max()  # no ions will be filtered
    time_window_us = 80e-6  # channel width for MCS8a

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_time(max_ions, time_window_us)

    assert crd.nof_shots == len(ions_per_shot)
    assert np.sum(crd.data) == np.sum(ions_per_shot)


def test_filter_max_ions_per_tof_window(crd_file):
    """Test maximum ions per shot in given time window."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions = 1  # filter the highest one out
    tof_window_us = (
        np.array([221, 281]) * 100 / 1e6
    )  # filter out the last one, but none of the others

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_tof_window(max_ions, tof_window_us)

    assert crd.nof_shots == len(ions_per_shot) - 1
    assert np.sum(crd.data) == np.sum(ions_per_shot) - 2


def test_filter_max_ions_per_tof_window_conv_tof_window_no_shots(crd_file):
    """Convert ToF window to np.ndarry, no filtering since no ions in criterion."""
    header, ions_per_shot, all_tofs, fname = crd_file
    max_ions = ions_per_shot.sum()  # filter the highest one out
    tof_window_us = (221, 400)
    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.filter_max_ions_per_tof_window(max_ions, tof_window_us)

    assert crd.nof_shots == len(ions_per_shot)
    assert np.sum(crd.data) == np.sum(ions_per_shot)


def test_mass_calibration_2pts(crd_file):
    """Perform mass calibration with two points."""
    _, _, _, fname = crd_file
    params = (13, 42)
    tms = (42.0, 95.0)

    mass_cal = np.zeros((len(tms), 2))
    for it, tm in enumerate(tms):
        mass_cal[it][0] = tm
        mass_cal[it][1] = pu.tof_to_mass(tm, params[0], params[1])

    # set variables
    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()

    crd.def_mcal = mass_cal
    mass_exp = pu.tof_to_mass(crd.tof, params[0], params[1])

    crd.mass_calibration()
    mass_rec = crd.mass
    print(tms)
    np.testing.assert_almost_equal(mass_rec, mass_exp)
    assert crd.mass.ndim == crd.tof.ndim


@pytest.mark.parametrize("new_integral", [None, (["Int2"], np.array([[3.0, 4.0]]))])
def test_integrals_definition_delete_undefined_background_to_none(
    crd_file, new_integral
):
    """Delete backgrounds and set to none if peak goes to undefined."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))

    crd.def_integrals = ["Integral"], np.array([[1.0, 2.0]])
    crd.def_backgrounds = ["Integral"], np.array([[2.0, 3.0]])
    crd.def_integrals = new_integral
    assert crd.def_backgrounds is None


def test_integrals_definition_delete_undefined_background(crd_file):
    """Delete backgrounds and set to none if peak goes to undefined."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))

    crd.def_integrals = ["Int1", "Int2"], np.array([[1.0, 2.0], [2.0, 3.0]])
    crd.def_backgrounds = ["Int1", "Int2"], np.array([[2.0, 3.0], [4.0, 5.0]])
    crd.def_integrals = ["Int1"], np.array([[1.0, 2.0]])

    assert "Int2" not in crd.def_backgrounds[0]


def test_integrals_delta_calc(crd_int_delta):
    """Assure that the delta calculation on the integral returns correct values."""
    crd_int_delta.integrals_calc_delta()
    deltas_exp = np.array([0, 0, 0, 0, np.nan, np.nan, np.nan])
    deltas_rec = crd_int_delta.integrals_delta.transpose()[0]  # test only deltas
    np.testing.assert_almost_equal(deltas_exp, deltas_rec)
    for line in crd_int_delta.integrals_pkg:
        np.testing.assert_almost_equal(crd_int_delta.integrals, line)


def test_packages(crd_file):
    """Simple test to ensure packages are made in two ways correctly."""
    _, ions_per_shot, _, fname = crd_file
    nof_shots = len(ions_per_shot)
    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.packages(nof_shots // 2)

    assert crd.data_pkg.sum() == crd.data.sum()
    np.testing.assert_equal(crd.data_pkg.sum(axis=0), crd.data)
    assert crd.nof_shots_pkg.sum() == crd.nof_shots
    # now redo w/ a lower number of shots per pkg
    crd.packages(nof_shots // 4)
    assert crd.data_pkg.sum() == crd.data.sum()
    np.testing.assert_equal(crd.data_pkg.sum(axis=0), crd.data)
    assert crd.nof_shots_pkg.sum() == crd.nof_shots


def test_sort_backgrounds(crd_file):
    """Sort backgrounds by number of protons, mass, and starting mass of interval."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.sort_backgrounds()  # does nothing, since None
    crd.def_backgrounds = ["Fe-56", "Ti-46", "Fe-56"], np.array(
        [[58.8, 59.2], [45.8, 46.2], [55.8, 56.2]]
    )

    crd.backgrounds = np.array([[2, 2], [1, 1]])
    crd.backgrounds_pkg = np.array([crd.backgrounds, crd.backgrounds - 1])

    names_exp = ["Ti-46", "Fe-56", "Fe-56"]
    values_exp = np.array([[45.8, 46.2], [55.8, 56.2], [58.8, 59.2]])

    crd.sort_backgrounds()
    crd.sort_backgrounds()  # already sorted, does nothing
    names_rec, values_rec = crd.def_backgrounds
    assert names_rec == names_exp
    np.testing.assert_equal(values_rec, values_exp)


def test_sort_backgrounds_non_element(crd_file) -> None:
    """Sort recognizable elements and other names together, all others last."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.sort_backgrounds()  # does nothing, since None
    crd.def_backgrounds = ["ZrO-94", "MoO-96", "Mo-94", "Zr-96"], np.array(
        [[93.9, 94.2], [95.4, 95.7], [93.4, 93.7], [95.9, 96.2]]
    )
    crd.backgrounds = np.array([[0, 0], [3, 3], [2, 2], [1, 1]])

    names_exp = ["Zr-96", "Mo-94", "ZrO-94", "MoO-96"]
    crd.sort_backgrounds()
    assert crd.def_backgrounds[0] == names_exp


def test_sort_integrals(crd_file):
    """Sort integrals by first mass."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.sort_integrals()  # does nothing, since None
    crd.def_integrals = ["Fe-56", "Ti-46"], np.array([[55.8, 56.2], [45.8, 46.2]])

    crd.integrals = np.array([[2, 2], [1, 1]])
    crd.integrals_pkg = np.array([crd.integrals, crd.integrals - 1])

    names_exp = ["Ti-46", "Fe-56"]
    values_exp = np.array([[45.8, 46.2], [55.8, 56.2]])
    integrals_exp = np.array([[1, 1], [2, 2]])
    integrals_pkg_exp = np.array([[[1, 1], [2, 2]], [[0, 0], [1, 1]]])

    crd.sort_integrals()
    crd.sort_integrals()  # second time, this should do nothing!
    names_rec, values_rec = crd.def_integrals
    assert names_rec == names_exp
    np.testing.assert_equal(values_rec, values_exp)
    np.testing.assert_equal(crd.integrals, integrals_exp)
    np.testing.assert_equal(crd.integrals_pkg, integrals_pkg_exp)


def test_sort_integrals_primary_and_secondary(crd_file) -> None:
    """Sort integrals first by element (if available), then by mass.

    This is especially important when we have two elements that are shifted by half
    masses.

    :param crd_file: CRD test file.
    """
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.sort_integrals()  # does nothing, since None
    crd.def_integrals = ["Zr-94", "Mo-96", "Mo-94", "Zr-96"], np.array(
        [[93.9, 94.2], [95.4, 95.7], [93.4, 93.7], [95.9, 96.2]]
    )
    crd.integrals = np.array([[0, 0], [3, 3], [2, 2], [1, 1]])

    names_exp = ["Zr-94", "Zr-96", "Mo-94", "Mo-96"]
    masses_exp = np.array([[93.9, 94.2], [95.9, 96.2], [93.4, 93.7], [95.4, 95.7]])
    integrals_exp = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])

    crd.sort_integrals()
    names_rec, masses_rec = crd.def_integrals
    assert names_rec == names_exp
    assert masses_rec == pytest.approx(masses_exp)
    np.testing.assert_equal(crd.integrals, integrals_exp)


def test_sort_integrals_non_element(crd_file) -> None:
    """Sort recognizable elements and other names together, all others last."""
    _, _, _, fname = crd_file
    crd = CRDFileProcessor(Path(fname))
    crd.sort_integrals()  # does nothing, since None
    crd.def_integrals = ["ZrO-94", "MoO-96", "Mo-94", "Zr-96"], np.array(
        [[93.9, 94.2], [95.4, 95.7], [93.4, 93.7], [95.9, 96.2]]
    )
    crd.integrals = np.array([[0, 0], [3, 3], [2, 2], [1, 1]])

    names_exp = ["Zr-96", "Mo-94", "ZrO-94", "MoO-96"]
    crd.sort_integrals()
    assert crd.def_integrals[0] == names_exp


def test_spectrum_part(crd_file):
    """Cut spectrum by two shots."""
    _, ions_per_shot, _, fname = crd_file

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.spectrum_part([1, len(ions_per_shot) - 2])

    assert crd.nof_shots == len(ions_per_shot) - 2


def test_spectrum_part_no_tof_indexes(crd_file):
    """Cut spectrum by two shots."""
    _, ions_per_shot, _, fname = crd_file

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.spectrum_part([2, 2])

    assert crd.nof_shots == 1
    assert crd.data.sum() == 0


def test_spectrum_part_data_length(crd_file):
    """Ensure that the data length is not cut."""
    _, _, _, fname = crd_file

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.spectrum_part([1, 2])

    assert len(crd.data) == len(crd.tof)


def test_spectrum_part_undo(crd_file):
    """Cut spectrum by two shots."""
    _, ions_per_shot, _, fname = crd_file

    crd = CRDFileProcessor(Path(fname))
    crd.spectrum_full()
    crd.spectrum_part([1, len(ions_per_shot) - 2])
    # undo the spectrum_part
    crd.spectrum_full()

    assert crd.nof_shots == len(ions_per_shot)
