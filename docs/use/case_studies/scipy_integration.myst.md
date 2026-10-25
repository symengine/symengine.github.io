---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Numerical integration with SciPy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Symengine/symengine.github.io/sources?filepath=docs/use/case_studies/scipy_integration.myst.md)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Symengine/symengine.github.io/blob/notebooks/use/case_studies/scipy_integration.myst.ipynb)
[![Local Installation](https://img.shields.io/badge/Local-Instructions-orange)](../tutorial.md)

SciPy's numerical integrators accept Python functions, but they can also call a
compiled SymEngine expression through a low-level callback. This example evaluates
the same double integral both ways and checks the result against its exact value.

Install SciPy in the [tutorial environment](../tutorial.md) before running the cells:

```bash
conda install scipy
```

## Define the integrand

```{code-cell} ipython3
import math

import symengine as se
from scipy import integrate

t, x = se.symbols("t x")
expression = se.exp(-x * t) / t**5
```

We integrate over $1 \leq t < \infty$ and $0 \leq x < \infty$.
Integrating with respect to $x$ first gives $t^{-6}$, whose integral from
$1$ to $\infty$ is $1/5$.

## Compile a SciPy callback

Pass `as_scipy=True` to `Lambdify` to obtain a callback that SciPy can use
directly. The order of the symbols must match the order of the integration
ranges: here `t` is the innermost variable and `x` is the outermost variable.

```{code-cell} ipython3
compiled = se.Lambdify([t, x], [expression], as_scipy=True)
ranges = [[1, math.inf], [0, math.inf]]
compiled_value, compiled_error = integrate.nquad(compiled, ranges)
assert math.isclose(compiled_value, 0.2, rel_tol=0, abs_tol=1e-7)
compiled_value, compiled_error
```

The second returned value is SciPy's estimate of the absolute integration error.
The callback evaluates the compiled expression without calling a Python function
for each integrand evaluation.

## Compare with a Python function

```{code-cell} ipython3
def python_integrand(t, x):
    return math.exp(-x * t) / t**5


python_value, python_error = integrate.nquad(python_integrand, ranges)
assert math.isclose(python_value, 0.2, rel_tol=0, abs_tol=1e-7)
assert math.isclose(compiled_value, python_value, rel_tol=0, abs_tol=1e-7)
python_value, python_error
```

Both calls use the same integration ranges and default tolerances. To compare
timings locally, construct `compiled` once before measuring repeated integration
calls; compiling the expression is a separate cost. The benefit depends on the
expression and the number of integrand evaluations, so this example does not
assume a fixed speedup.
