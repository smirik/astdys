import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import shutil

import astdys


@pytest.fixture(autouse=True)
def run_around_tests():
    Path("cache/tests").mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree("cache/tests")


def test_transform_astdys_catalog():
    data = astdys.astdys.search(1)
    assert data is not None


def test_transform_astdys_synthetic_catalog():
    astdys.set_type("synthetic")
    data = astdys.astdys.search(1)
    assert data is not None
    assert 2.7670962 == pytest.approx(data["a"], 0.01)
    assert 54.070272 == pytest.approx(data["g"], 0.1)
    assert -59.170034 == pytest.approx(data["s"], 0.1)
