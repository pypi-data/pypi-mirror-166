# wham
Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.

Tested on Version 2.0.9, 2.0.11.

## Installation
1. Download and compile WHAM from [here](http://membrane.urmc.rochester.edu/?page_id=126)
2. Install Python wrapper:

```
pip install git+https://github.com/bnovak1/wham
```

## Usage
Currently, the wrapper only supports 1D WHAM calculations but feel free to open an issue or a pull
request if you would like 2D WHAM implemented.

Make sure you check out
[WHAM documentation](http://membrane.urmc.rochester.edu/sites/default/files/wham/doc.pdf) before
using it. It's fairly short and very informative. All the parameters below would make much more
sense after you read it.

```python
from wham import Wham
wham_calculator = Wham()
```

Add your simulations with an id, simulation times (time), reaction coordinates (position), equilibrium reaction coordinate for the spring (eq_position), and spring constant in (energy unit)/(mol-(reaction coordinate unit)^2) (k_spring). Note that the energy unit can be chosen when compiling WHAM and is kcal by default (see page 6 of the [WHAM documentation](http://membrane.urmc.rochester.edu/sites/default/files/wham/doc.pdf)).

```python
wham_calculator.add_simulation(sim_id, time, position, eq_position, k_spring)
```

You can plot position histograms before running WHAM.

```python
wham_calculator.plot_histograms(title='WHAM histograms', save='wham-hist.png')
````

You can run WHAM 1D as follows. The input parameters are mostly in the same order as the WHAM executable: lower and upper boundary of the histogram, number of bins in the histogram, convergence tolerance, temperature at which the WHAM analysis is performed, number of “padding” values that should be printed for periodic PMFs, path to WHAM 1D executable, path to write input and output files for WHAM analysis, periodicity of the reaction coordinate (defaults to no periodicity), cleanup WHAM files after running, and finally WHAM verbosity.

```python
wham_calculator.run(hist_min, hist_max, num_bins, tolerance, temperature,
      numpad, executable, directory, periodicity='', cleanup=False, verbose=True)
```

Finally, you can plot the free energy barrier using the function below

```python
wham_calculator.plot_energy_barrier(save='wham-barrier.png'))
```
