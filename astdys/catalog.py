from dataclasses import dataclass
from typing import List


@dataclass
class Catalog:
    """Configuration for an AstDyS catalog."""

    original_filename: str
    filename: str
    url: str
    catalog_type: str
    skip_rows: int
    columns: List[str]
    degree_columns: List[str]
