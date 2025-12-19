"""AstDyS Python Wrapper - Access to asteroid orbital elements catalogs.

This module provides a simple interface to the AstDyS database of asteroid
orbital elements. Import and use the module-level functions directly:

    import astdys

    # Search for asteroids
    elements = astdys.search(1)

    # Switch to synthetic proper elements
    astdys.set_type("synthetic")
    proper = astdys.search(1)

Note: Catalogs are loaded lazily - importing this module does NOT download
or load any data. Data is only loaded when you call search functions.
"""

from .astdys import AstDys
from .catalog import Catalog

# Module-level API - these are lazy references to class methods
# No data is loaded at import time
search = AstDys.search
search_by_axis = AstDys.search_by_axis
set_type = AstDys.set_type
get_catalog_time = AstDys.get_catalog_time
get_catalog_datetime = AstDys.get_catalog_datetime
rebuild = AstDys.rebuild
load = AstDys.load
get_catalog = AstDys.get_catalog

# Backward compatibility aliases (deprecated)
catalog_time = AstDys.get_catalog_time
datetime = AstDys.get_catalog_datetime

__all__ = [
    'search',
    'search_by_axis',
    'set_type',
    'get_catalog_time',
    'get_catalog_datetime',
    'rebuild',
    'load',
    'get_catalog',
    'AstDys',
    'Catalog',
    # Deprecated
    'catalog_time',
    'datetime',
]

__version__ = '0.9.4'
