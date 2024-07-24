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

## License

MIT
