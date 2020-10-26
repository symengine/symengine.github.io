---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Python Bindings

```{code-cell} ipython3
from symengine import var
from symengine.printing import init_printing
```

```{code-cell} ipython3
init_printing()
var("x y z")
e = (x+y+z)**4
e.expand()
```
