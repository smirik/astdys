import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import shutil

import astdys


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
    astdys.astdys.catalogs_configs = {'osculating': catalog1}
    Path("cache/tests").mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree("cache/tests")


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


def test_search():
    obj = astdys.astdys.search(6)
    assert 2.42456 == pytest.approx(obj["a"], 0.01)
    assert 0.20328 == pytest.approx(obj["e"], 0.01)
    assert 14.73973 == pytest.approx(obj["inc"] / np.pi * 180, 0.01)
    assert 138.64293 == pytest.approx(obj["Omega"] / np.pi * 180, 0.01)
    assert 239.70765 == pytest.approx(obj["omega"] / np.pi * 180, 0.01)
    assert 242.94481 == pytest.approx(obj["M"] / np.pi * 180, 0.01)

    obj = astdys.astdys.search(10)
    assert obj is not None
    obj = astdys.astdys.search(11)
    assert obj is None
    obj = astdys.astdys.search(123456789)
    assert obj is None


def test_search_list():
    objects = astdys.astdys.search([6])
    obj = objects['6']
    assert 2.42456 == pytest.approx(obj["a"], 0.01)
    assert 0.20328 == pytest.approx(obj["e"], 0.01)
    assert 14.73973 == pytest.approx(obj["inc"] / np.pi * 180, 0.01)
    assert 138.64293 == pytest.approx(obj["Omega"] / np.pi * 180, 0.01)
    assert 239.70765 == pytest.approx(obj["omega"] / np.pi * 180, 0.01)
    assert 242.94481 == pytest.approx(obj["M"] / np.pi * 180, 0.01)

    objects = astdys.astdys.search([5, 6, 7, 100])
    assert '5' in objects
    assert '6' in objects
    assert '7' in objects
    assert 2.57362 == pytest.approx(objects['5']["a"], 0.01)
    assert 2.42456 == pytest.approx(objects['6']["a"], 0.01)
    assert 2.38713 == pytest.approx(objects['7']["a"], 0.01)
    assert '100' not in objects
