# Frequently Asked Questions

## What are the main use-cases?

There are is a [growing list of projects](https://github.com/symengine/symengine/wiki/Projects-using-SymEngine) which use SymEngine. However, mostly
this is used for:

- Code Generation
- Optimization
- Providing an efficient backend for other languages

## What does this have to do with SymPy?

SymEngine has a different structure (organizational and financial). However,
there are many developers in common, and `sympy` is able to use `symengine` as a
back-end.

## What about Eigen / Armadillo / XTensor?

These are numerical libraries, they require explicit formulation of equations,
and due to the finite representation of digits on computers, they [are prone to
numerical
errors](https://docs.microsoft.com/en-us/cpp/build/why-floating-point-numbers-may-lose-precision?view=msvc-160).

## How do I convert my Eigen / Armadillo / Xtensor code?

There should not be any need to do so. If a symbolic library is required it
should be clear at the ideation phase. If inheriting legacy code which needs to
be converted, it should be done in terms of the underlying C++ data structures.
