---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

# First Steps

This is meant to be a gentle introduction to the `symengine` C++ library.

## Working with Expressions

We will start by inspecting the use of {ref}`Expression <doxid-class_sym_engine_1_1_expression>`.

```{code-cell}
#include <symengine/expression.h>
using SymEngine::Expression;
```

```{code-cell}
Expression x("x");
```

```{code-cell}
auto ex = pow(x+sqrt(Expression(2)), 6);
ex
```

```{code-cell}
expand(ex)
```
