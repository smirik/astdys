import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import shutil

import astdys
import astdys.util


@pytest.fixture(autouse=True)
def run_around_tests():
    catalog1 = astdys.Catalog(
        original_filename='tests/small.cat',
        filename='tests/small.csv',
        url="",
        catalog_type='osculating',
        skip_rows=6,
        columns=['num', 'epoch', 'a', 'e', 'inc', 'Omega', 'omega', 'M', 'del_1', 'del_2', 'del_3'],
        degree_columns=["inc", "Omega", "omega", "M"],
    )
    catalog2 = astdys.Catalog(
        original_filename='tests/proper.cat',
        filename='tests/proper.csv',
        url="",
        catalog_type='synthetic',
        skip_rows=2,
        columns=['num', 'mag', 'a', 'e', 'sinI', 'n', 'del_1', 'del_2', 'lce', 'del_3'],
        degree_columns=["sinI", "n"],
    )
    astdys.astdys.catalogs_configs = {'osculating': catalog1, 'synthetic': catalog2}
    Path("cache/tests").mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree("cache/tests")


def test_convert_mjd_to_date():
    assert "1858-11-17 00:00:00" == astdys.util.convert_mjd_to_date(0)
    assert "2021-01-01 00:00:00" == astdys.util.convert_mjd_to_date(59215)
    astdys.astdys.catalogs = {}


def test_convert_mjd_to_datetime():
    assert "1858-11-17 00:00:00" == astdys.util.convert_mjd_to_datetime(0).strftime("%Y-%m-%d %H:%M:%S")
    assert "2021-01-01 00:00:00" == astdys.util.convert_mjd_to_datetime(59215).strftime("%Y-%m-%d %H:%M:%S")
    astdys.astdys.catalogs = {}


def test_catalog_dates():
    assert "2020-12-17 00:00:00" == astdys.catalog_time()
    assert "2020-12-17 00:00:00" == astdys.datetime().strftime("%Y-%m-%d %H:%M:%S")
    astdys.astdys.catalogs = {}


def test_transform_astdys_catalog():
    cat = astdys.astdys.transform_astdys_catalog()
    assert "a" in cat
    assert "e" in cat
    assert "inc" in cat
    assert "omega" in cat
    assert "Omega" in cat
    assert "M" in cat
    assert 10 == len(cat)

    assert 2.766 == pytest.approx(cat["a"].iloc[0], 0.01)
    assert 0.07816 == pytest.approx(cat["e"].iloc[0], 0.01)

    assert "6" == cat["num"].iloc[5]
    assert 2.42456 == pytest.approx(cat["a"].iloc[5], 0.01)
    assert 0.20328 == pytest.approx(cat["e"].iloc[5], 0.01)
    assert 14.73973 == pytest.approx(cat["inc"].iloc[5] / np.pi * 180, 0.01)
    assert 138.64293 == pytest.approx(cat["Omega"].iloc[5] / np.pi * 180, 0.01)
    assert 239.70765 == pytest.approx(cat["omega"].iloc[5] / np.pi * 180, 0.01)
    assert 242.94481 == pytest.approx(cat["M"].iloc[5] / np.pi * 180, 0.01)


def test_build():
    astdys.astdys.build()

    cat = pd.read_csv("tests/small.csv")
    assert 10 == len(cat)
    assert 2.766 == pytest.approx(cat["a"].iloc[0], 0.01)
    assert 0.07816 == pytest.approx(cat["e"].iloc[0], 0.01)
    assert 6 == cat["num"].iloc[5]
    assert 2.42456 == pytest.approx(cat["a"].iloc[5], 0.01)


def test_load():
    assert astdys.astdys.catalog() is None
    astdys.astdys.load()
    assert astdys.astdys.catalog() is not None


def test_multiple_catalogs():
    obj = astdys.search(1)
    assert 2.76608 == pytest.approx(obj["a"], 0.01)
    astdys.set_type("synthetic")
    obj = astdys.search(1)
    assert 22.7670962 == pytest.approx(obj["a"], 0.01)
    astdys.set_type("osculating")
    obj = astdys.search(1)
    assert 2.76608 == pytest.approx(obj["a"], 0.01)


def test_search():
    obj = astdys.search(6)
    assert 2.42456 == pytest.approx(obj["a"], 0.01)
    assert 0.20328 == pytest.approx(obj["e"], 0.01)
    assert 14.73973 == pytest.approx(obj["inc"] / np.pi * 180, 0.01)
    assert 138.64293 == pytest.approx(obj["Omega"] / np.pi * 180, 0.01)
    assert 239.70765 == pytest.approx(obj["omega"] / np.pi * 180, 0.01)
    assert 242.94481 == pytest.approx(obj["M"] / np.pi * 180, 0.01)

    obj = astdys.search(10)
    assert obj is not None
    obj = astdys.search(11)
    assert obj is None
    obj = astdys.search(123456789)
    assert obj is None


def test_search_list():
    objects = astdys.search([6])
    obj = objects['6']
    assert 2.42456 == pytest.approx(obj["a"], 0.01)
    assert 0.20328 == pytest.approx(obj["e"], 0.01)
    assert 14.73973 == pytest.approx(obj["inc"] / np.pi * 180, 0.01)
    assert 138.64293 == pytest.approx(obj["Omega"] / np.pi * 180, 0.01)
    assert 239.70765 == pytest.approx(obj["omega"] / np.pi * 180, 0.01)
    assert 242.94481 == pytest.approx(obj["M"] / np.pi * 180, 0.01)

    objects = astdys.search([5, 6, 7, 100])
    assert '5' in objects
    assert '6' in objects
    assert '7' in objects
    assert 2.57362 == pytest.approx(objects['5']["a"], 0.01)
    assert 2.42456 == pytest.approx(objects['6']["a"], 0.01)
    assert 2.38713 == pytest.approx(objects['7']["a"], 0.01)
    assert '100' not in objects


def test_search_by_axis():
    obj = astdys.search_by_axis(2.70)
    assert 3 == len(obj)
    assert isinstance(obj, pd.DataFrame)

    obj = astdys.search_by_axis(2.70, sigma=0.05)
    assert 1 == len(obj)

    obj = astdys.search_by_axis(1.0)
    assert 0 == len(obj)
