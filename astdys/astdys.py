import pandas as pd
import numpy as np
from pathlib import Path
import urllib.request
import datetime
from typing import Union, Optional, Dict, List

from astdys.util import convert_mjd_to_date, convert_mjd_to_datetime
from astdys.catalog import Catalog

# Catalog configurations
OSCULATING_CATALOG = Catalog(
    original_filename='cache/allnum.cat',
    filename='cache/allnum.csv',
    url="https://newton.spacedys.com/~astdys2/catalogs/allnum.cat",
    catalog_type='osculating',
    skip_rows=6,
    columns=['name', 'epoch', 'a', 'e', 'inc', 'Omega', 'omega', 'M', 'del_1', 'del_2', 'del_3'],
    degree_columns=["inc", "Omega", "omega", "M"],
)

SYNTHETIC_CATALOG = Catalog(
    original_filename='cache/all.syn',
    filename='cache/allsyn.csv',
    url="https://newton.spacedys.com/~astdys2/propsynth/all.syn",
    catalog_type='synthetic',
    skip_rows=2,
    columns=['name', 'mag', 'a', 'e', 'sinI', 'n', 'g', 's', 'lce', 'my'],
    degree_columns=["sinI", "n"],
)


class AstDys:
    """Main class for accessing AstDyS asteroid catalogs.

    This class provides access to both osculating orbital elements and
    synthetic proper elements from the AstDyS database.
    """

    logger = None

    catalogs: Dict[str, pd.DataFrame] = {}

    catalogs_configs = {'osculating': OSCULATING_CATALOG, 'synthetic': SYNTHETIC_CATALOG}
    catalog_type = 'osculating'

    @classmethod
    def search(cls, identifier: Union[int, str, List[Union[int, str]]]) -> Optional[Union[Dict[str, float], Dict[str, Dict[str, float]]]]:
        """Search for asteroid(s) by name or designation.

        Args:
            identifier: Single asteroid identifier (int, str) or list of identifiers.
                       Examples: 1, '433', '2017HV1', '4150T-3', [1, 2, 3]

        Returns:
            For single asteroid: dict of orbital elements, or None if not found
            For multiple asteroids: dict mapping asteroid names to their elements

        Example:
            >>> astdys.search(1)  # Get Ceres
            {'name': '1', 'a': 2.766, 'e': 0.078, ...}

            >>> astdys.search([1, 2, 3])  # Get multiple asteroids
            {'1': {...}, '2': {...}, '3': {...}}
        """
        if cls._catalog() is None:
            cls.load()

        if isinstance(identifier, (int, str)):
            name_str = str(identifier)
            matches = cls._catalog()[cls._catalog()['name'] == name_str]
            if len(matches) > 0:
                return matches.iloc[0].to_dict()
            return None
        else:
            name_list = [str(n) for n in identifier]
            filtered_catalog = cls._catalog()[cls._catalog()['name'].isin(name_list)]
            result = {row['name']: row.to_dict() for _, row in filtered_catalog.iterrows()}
            return result

    @classmethod
    def search_by_axis(cls, axis: float, sigma: float = 0.1) -> pd.DataFrame:
        """Find asteroids within a range of semi-major axis.

        Args:
            axis: Semi-major axis in AU (must be positive)
            sigma: Search range in AU (default: 0.1, must be positive)

        Returns:
            DataFrame containing matching asteroids

        Raises:
            ValueError: If axis or sigma are not positive

        Example:
            >>> astdys.search_by_axis(2.7, sigma=0.1)  # Find asteroids around 2.7 AU
        """
        if axis <= 0:
            raise ValueError(f"Semi-major axis must be positive, got {axis}")
        if sigma <= 0:
            raise ValueError(f"Sigma must be positive, got {sigma}")

        if cls._catalog() is None:
            cls.load()

        min_axis = axis - sigma
        max_axis = axis + sigma
        df = cls._catalog()[(cls._catalog()['a'] >= min_axis) & (cls._catalog()['a'] <= max_axis)]
        return df

    @classmethod
    def load(cls) -> None:
        """Load the current catalog type from disk.

        If the catalog file doesn't exist, it will be downloaded and built first.
        This method is called automatically by search methods when needed.
        """
        filename = cls._catalog_full_filename()
        if cls._catalog() is None:
            output_file = Path(filename)
            if not output_file.exists():
                cls._build()

        cls.catalogs[cls.catalog_type] = pd.read_csv(filename, dtype={'name': str})

    @classmethod
    def _catalog(cls) -> Optional[pd.DataFrame]:
        """Get the current catalog DataFrame (internal use)."""
        if cls.catalog_type in cls.catalogs:
            return cls.catalogs[cls.catalog_type]
        return None

    @classmethod
    def get_catalog(cls) -> Optional[pd.DataFrame]:
        """Get the current catalog DataFrame for advanced usage.

        Returns:
            pandas DataFrame with asteroid data. The 'name' column contains numbered
            asteroids (e.g., '1', '433') and provisional designations (e.g., '2017HV1',
            '4150T-3').
        """
        if cls._catalog() is None:
            cls.load()
        return cls._catalog()

    @classmethod
    def set_type(cls, catalog_type: str) -> None:
        """Switch between catalog types.

        Args:
            catalog_type: Either 'osculating' or 'synthetic'

        Raises:
            ValueError: If catalog_type is not supported
        """
        if catalog_type in cls.catalogs_configs:
            cls.catalog_type = catalog_type
            cls.load()
        else:
            raise ValueError(f"Catalog type '{catalog_type}' is not supported. Valid options: {list(cls.catalogs_configs.keys())}")

    @classmethod
    def _catalog_config(cls) -> Optional[Catalog]:
        """Get configuration for current catalog type (internal use)."""
        if cls.catalog_type in cls.catalogs_configs:
            return cls.catalogs_configs[cls.catalog_type]
        return None

    @classmethod
    def _log(cls, text: str) -> None:
        """Log a message (internal use)."""
        if cls.logger is None:
            print(text)
        else:
            cls.logger.debug(text)

    @classmethod
    def get_catalog_time(cls) -> str:
        """Get the catalog epoch as a formatted string.

        Only works for osculating catalog (which has epoch column).

        Returns:
            Formatted date string (YYYY-MM-DD HH:MM:SS)

        Raises:
            ValueError: If current catalog doesn't have epoch information
        """
        if cls.catalog_type != 'osculating':
            raise ValueError("Catalog epoch is only available for osculating catalog")

        if cls._catalog() is None:
            cls.load()

        elems = cls.search(1)
        if elems is None or "epoch" not in elems:
            raise ValueError("Could not retrieve epoch information from catalog")
        return convert_mjd_to_date(elems["epoch"])

    @classmethod
    def get_catalog_datetime(cls) -> datetime.datetime:
        """Get the catalog epoch as a datetime object.

        Only works for osculating catalog (which has epoch column).

        Returns:
            datetime object representing the catalog epoch

        Raises:
            ValueError: If current catalog doesn't have epoch information
        """
        if cls.catalog_type != 'osculating':
            raise ValueError("Catalog epoch is only available for osculating catalog")

        if cls._catalog() is None:
            cls.load()

        elems = cls.search(1)
        if elems is None or "epoch" not in elems:
            raise ValueError("Could not retrieve epoch information from catalog")
        return convert_mjd_to_datetime(elems["epoch"])

    @classmethod
    def _astdys_full_filename(cls) -> str:
        """Get full path to original AstDyS catalog file (internal use)."""
        return str(Path.cwd() / cls._catalog_config().original_filename)

    @classmethod
    def _catalog_full_filename(cls) -> str:
        """Get full path to processed CSV catalog file (internal use)."""
        return str(Path.cwd() / cls._catalog_config().filename)

    @classmethod
    def rebuild(cls) -> None:
        """Force rebuild of catalog from fresh download.

        Deletes existing catalog files and downloads fresh data from AstDyS.
        """
        input_file = Path(cls._astdys_full_filename())
        if input_file.exists():
            input_file.unlink()
        cls._build()

    @classmethod
    def _build(cls) -> None:
        """Download and build catalog from AstDyS (internal use)."""
        input_file = Path(cls._astdys_full_filename())
        if not input_file.exists():
            cls._log(f"Cannot find {cls.catalog_type} catalog. Trying to download it...")
            try:
                urllib.request.urlretrieve(cls._catalog_config().url, cls._catalog_config().original_filename)
            except Exception as e:
                raise Exception(
                    f"Cannot download {cls.catalog_type} catalog from {cls._catalog_config().url}. "
                    f"Error: {e}. You can manually download the catalog file to {cls._catalog_config().original_filename}"
                )
            cls._log("Successfully downloaded. Continue working...")

        cat = cls._transform_astdys_catalog()
        cat.to_csv(cls._catalog_full_filename(), index=False)

    @classmethod
    def _transform_astdys_catalog(cls) -> pd.DataFrame:
        """Parse and transform AstDyS catalog file to DataFrame (internal use)."""
        catalog = pd.read_csv(
            cls._astdys_full_filename(),
            sep="\\s+",
            header=None,
            skiprows=cls._catalog_config().skip_rows,
            names=cls._catalog_config().columns,
            index_col=False,
            dtype={'name': str},  # Ensure name column is always string
        )
        # Remove quote marks from string fields
        catalog = catalog.replace("'", '', regex=True)

        # Drop temporary columns (del_1, del_2, del_3) used in original file format
        columns_to_drop = [col for col in catalog.columns if col.startswith('del_')]
        catalog.drop(columns=columns_to_drop, inplace=True)

        # Convert angular elements from degrees to radians for astronomical calculations
        for col in cls._catalog_config().degree_columns:
            catalog[col] = catalog[col].astype(float) * np.pi / 180

        # Move epoch column to end for better readability
        if 'epoch' in catalog.columns:
            columns_except_epoch = [col for col in catalog.columns if col != 'epoch']
            new_column_order = columns_except_epoch + ['epoch']
            catalog = catalog[new_column_order]

        return catalog
