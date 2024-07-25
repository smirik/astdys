This is a small wrapper to [AstDyS catalogue](https://newton.spacedys.com/astdys2/index.php?pc=0) of the asteroids in the Solar system.

## How to use it

### Installation

```bash
pip install astdys
```

### Usage

```python
import astdys

elements = astdys.search(1)
print(elements)
```

`elements` contains a dictionary of Keplerian elements of an asteroid.

Also, you can get a list of objects by the semi-major axis:

```python
import astdys

objects = astdys.search_by_axis(2.70, sigma=0.2)
print(objects)
```

The method will return a dataframe containing all records found. `sigma` is optional and represent the variation (from `axis-sigma` to `axis+sigma`). The default value of `sigma=0.1`.

## License

MIT
