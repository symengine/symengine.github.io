---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: C++11
  language: C++11
  name: xcpp11
---

# Matrices

```{code-cell}
#include <chrono>
#include <xcpp/xdisplay.hpp>
#include <symengine/parser.h>

#include <symengine/matrix.h>
#include <symengine/add.h>
#include <symengine/pow.h>
#include <symengine/symengine_exception.h>
#include <symengine/visitor.h>
```

## Base Elements
We will need a set of basic elements to cover a reasonable set of operations. Namely we would like:
- Two Matrices (A,B)
- A Vector (X)

```{code-cell}
SymEngine::vec_basic elemsA{SymEngine::integer(1),
                           SymEngine::integer(0),
                           SymEngine::integer(-1),
                           SymEngine::integer(-2)};
SymEngine::DenseMatrix A = SymEngine::DenseMatrix(2, 2, elemsA);
```

```{code-cell}
A.__str__()
```

```{code-cell}
SymEngine::vec_basic elemsB{SymEngine::integer(5),
                           SymEngine::integer(2),
                           SymEngine::integer(-7),
                           SymEngine::integer(-3)};
SymEngine::DenseMatrix B = SymEngine::DenseMatrix(2, 2, elemsB);
B.__str__()
```

## Basic Operations
The key thing to remember that as a `C++` library, we need to pre-allocated variable sizes and types. Furthermore, the unary operators are **not** overloaded, so we will call functions for each of the standard operations. The general form of each of these is:

**operation**(*term1*,*term2*,**output**)

+++

## Addition
For 

```{code-cell}
// Addition
SymEngine::DenseMatrix C = SymEngine::DenseMatrix(2, 2);
add_dense_dense(A, B,C);
C.__str__()
```

## Gaussian Elimination
One of the main use-cases for any library with matrices is the ability to perform Gaussian elimination. We will consider an example from the literature {cite}`nakosFractionfreeAlgorithmsLinear1997`.

```{code-cell}
    // Fraction-Free Algorithms for Linear and Polynomial Equations, George C
    // Nakos,
    // Peter R Turner et. al.
   SymEngine::DenseMatrix A = SymEngine::DenseMatrix(4, 4, {SymEngine::integer(1), SymEngine::integer(2), SymEngine::integer(3), SymEngine::integer(4),
                           SymEngine::integer(2), SymEngine::integer(2), SymEngine::integer(3), SymEngine::integer(4),
                           SymEngine::integer(3), SymEngine::integer(3), SymEngine::integer(3), SymEngine::integer(4),
                           SymEngine::integer(9), SymEngine::integer(8), SymEngine::integer(7), SymEngine::integer(6)});
  SymEngine::DenseMatrix  B = SymEngine::DenseMatrix(4, 4);
fraction_free_gaussian_elimination(A, B);
B.__str__()
```

```{bibliography} ../../references.bib
```
