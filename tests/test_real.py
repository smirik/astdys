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
