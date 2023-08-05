<h1 align="center">
    PySDNoise
</h1>
<p align="center">
    <strong>A Python wrapper for noise functions with derivatives.</strong>
</p>

Python wrapper for [Stefan Gustavson's](https://github.com/stegu) simplex noise
functions with analytical derivates, which can be found
[here](https://github.com/stegu/perlin-noise).

## Status
*This project is still under active development and has not yet reached a stable
version until v1.0.0 So when using this code currently expect random error and
dragons.*

## Usage
```Python
from sdnoise import sdnoise2

n, dx, dy = sdnoise2(25.52, 30.06)
```

## Download
 - https://github.com/open-terra/pysdnoise

