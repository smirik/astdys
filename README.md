# AstDyS Python Wrapper

Python interface to the [AstDyS database](https://newton.spacedys.com/astdys2/index.php?pc=0) - a comprehensive catalog of asteroid orbital elements.

## Features

-   **500,000+ numbered asteroids** with osculating orbital elements
-   **Osculating and synthetic proper elements** for asteroid studies
-   **Automatic downloads** - catalogs are fetched on first use
-   **Lazy loading** - imports are fast, data loads only when needed
-   **Pandas integration** - returns DataFrames for analysis

**Note on angles:** All angular orbital elements are returned in **radians** (not degrees) for direct use in calculations.

## Installation

```bash
pip install astdys
```

## Quick Start

```python
import astdys

# Get osculating elements for asteroid 1 (Ceres)
elements = astdys.search(1)
print(elements)

# Get synthetic proper elements for the same asteroid
astdys.set_type("synthetic")
proper_elements = astdys.search(1)
print(proper_elements)
```

## Usage

### Basic Search

Search for asteroids by name or designation in the AstDyS catalog. The catalog includes:

-   **Numbered asteroids**: Use numbers (e.g., `1` for Ceres, `433` for Eros)
-   **Provisional designations**: Use strings (e.g., `'2017HV1'`, `'4150T-3'`, `'4702P-L'`)

```python
import astdys

# Search for asteroid 1 (Ceres)
elements = astdys.search(1)
if elements:
    print(f"Semi-major axis: {elements['a']} AU")
    print(f"Eccentricity: {elements['e']}")
    print(f"Inclination: {elements['inc']} radians")

# Search for a provisional designation
elements = astdys.search('2017HV1')
if elements:
    print(f"Found provisional asteroid: {elements}")
```

Search for multiple asteroids:

```python
# Search for multiple asteroids
objects = astdys.search([1, 2, 3, 4, 5])
for name, elements in objects.items():
    print(f"Asteroid {name}: a={elements['a']:.3f} AU")
```

### Search by Semi-major Axis

Find asteroids within a specific range of semi-major axis:

```python
# Find asteroids around 2.7 AU (with default sigma=0.1 AU)
asteroids = astdys.search_by_axis(2.70)
print(f"Found {len(asteroids)} asteroids")

# Use custom range (sigma=0.05 AU)
asteroids = astdys.search_by_axis(2.70, sigma=0.05)
print(asteroids[['a', 'e', 'inc']].head())
```

### Working with Different Catalog Types

The library supports two types of orbital elements:

#### Osculating Elements (Default)

Classical Keplerian orbital elements at a specific epoch:

```python
# Default catalog type is 'osculating'
astdys.set_type("osculating")  # This is the default
elements = astdys.search(1)

# Available elements:
# - a: semi-major axis (AU)
# - e: eccentricity
# - inc: inclination (radians)
# - Omega: longitude of ascending node (radians)
# - omega: argument of perihelion (radians)
# - M: mean anomaly (radians)
# - epoch: epoch (MJD)
```

#### Synthetic Proper Elements

Proper elements are averaged orbital elements that eliminate short-term perturbations, useful for asteroid family studies:

```python
# Switch to synthetic proper elements
astdys.set_type("synthetic")
elements = astdys.search(1)

# Available elements:
# - a: proper semi-major axis (AU)
# - e: proper eccentricity
# - sinI: sine of proper inclination
# - n: mean motion frequency (arcsec/year)
# - g: perihelion precession frequency (arcsec/year)
# - s: node precession frequency (arcsec/year)
# - lce: Lyapunov Characteristic Exponent
# - my: integration time (Myr)
# - mag: absolute magnitude
```

### Catalog Information

Get the epoch of osculating elements (only available for osculating catalog):

```python
import astdys

# Make sure we're using osculating catalog
astdys.set_type("osculating")

# Get catalog epoch as string
date_str = astdys.get_catalog_time()
print(f"Catalog epoch: {date_str}")  # e.g., "2024-01-15 00:00:00"

# Or as datetime object for calculations
date = astdys.get_catalog_datetime()
print(f"Catalog date: {date}")
```

**Note:** Synthetic proper elements don't have a specific epoch since they're averaged over long timescales.

### Rebuilding the Catalog

Force a fresh download and rebuild of the catalog:

```python
# This will download fresh data from AstDyS
astdys.rebuild()
```

### Comparing Osculating and Proper Elements

```python
import astdys

asteroid_num = 4  # Vesta

# Get osculating elements
astdys.set_type("osculating")
osc = astdys.search(asteroid_num)

# Get proper elements
astdys.set_type("synthetic")
prop = astdys.search(asteroid_num)

print("Osculating vs Proper elements:")
print(f"Semi-major axis: {osc['a']:.4f} vs {prop['a']:.4f} AU")
print(f"Eccentricity: {osc['e']:.4f} vs {prop['e']:.4f}")
```

### Iterating Over Catalog Records

You can iterate over the entire catalog dataframe to access all asteroids:

```python
import astdys

# Set catalog type to synthetic
astdys.set_type("synthetic")

# Get the catalog dataframe (automatically loads if needed)
catalog = astdys.get_catalog()

# Iterate over first 100 records
for idx, row in catalog.head(100).iterrows():
    print(f"name={row['name']}, mag={row['mag']:.2f}, a={row['a']:.4f} AU, e={row['e']:.6f}, "
          f"sinI={row['sinI']:.6f}, n={row['n']:.6f}, g={row['g']:.6f}, s={row['s']:.6f}, "
          f"lce={row['lce']:.6f}, my={row['my']:.2f}")

print(f"\nTotal records in catalog: {len(catalog)}")
```

This approach is useful when you need to process or analyze multiple asteroids systematically, such as for statistical studies or family identification.

**Note:** The `get_catalog()` method returns the raw pandas DataFrame for advanced users who need direct access to all data at once. The 'name' column contains numbered asteroids (e.g., '1', '433') or provisional designations (e.g., '2017HV1', '4150T-3').

## API Reference

### Main Functions

-   **`search(identifier)`** - Find asteroid(s) by number or designation

    -   Returns: dict of orbital elements, or dict of dicts for multiple asteroids

-   **`search_by_axis(axis, sigma=0.1)`** - Find asteroids by semi-major axis

    -   `axis`: Semi-major axis in AU
    -   `sigma`: Search range in AU (default: 0.1)
    -   Returns: pandas DataFrame

-   **`set_type(catalog_type)`** - Switch between 'osculating' or 'synthetic'

-   **`get_catalog()`** - Get full catalog as pandas DataFrame

-   **`get_catalog_time()`** - Get osculating catalog epoch as string (osculating only)

-   **`get_catalog_datetime()`** - Get osculating catalog epoch as datetime (osculating only)

-   **`rebuild()`** - Force fresh download and rebuild of current catalog

### Data Columns

**Osculating elements:** `name`, `a` (AU), `e`, `inc` (rad), `Omega` (rad), `omega` (rad), `M` (rad), `epoch` (MJD)

**Synthetic proper elements:** `name`, `a` (AU), `e`, `sinI`, `n` (arcsec/yr), `g` (arcsec/yr), `s` (arcsec/yr), `lce`, `my` (Myr), `mag`

## Performance

-   **Catalog sizes**: ~100-200 MB for osculating, ~50 MB for synthetic
-   **First load**: 30-60 seconds (includes download and processing)
-   **Subsequent loads**: < 1 second (reads from cache)

## License

MIT

## Credits

This wrapper provides access to the AstDyS database. The AstDyS catalog and synthetic proper elements were created by:

**Zoran Knežević** (Astronomical Observatory, Belgrade) and **Andrea Milani** (University of Pisa)

Key references:

-   Knežević, Z. & Milani, A. (2003). "Proper element catalogs and asteroid families." _Astronomy & Astrophysics_, 403, 1165-1173.
-   Knežević, Z. & Milani, A. (2001). "Synthetic proper elements for outer main belt asteroids." _Celestial Mechanics and Dynamical Astronomy_, 78, 17-46.

The AstDyS service is available at: https://newton.spacedys.com/astdys2/
