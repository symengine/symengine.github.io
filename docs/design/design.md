# Design

Summary of our design decisions and some pointers to the literature.

## SymEngine is used in different languages

The C++ SymEngine library doesn't care about SymPy objects at all. We are just trying to implement things in some maintainable way, currently we settled on using `Basic`, `Mul`, `Pow`, ... hierarchy and implement most functionality using the visitor pattern or single dispatch, so `Basic` doesn't need many methods. We are keeping an option to perhaps do things differently if they turn out to be faster. Either way though, this shouldn't matter at all for how it is actually used from Python, Ruby or Julia.

Let's talk about just Python: the wrappers are in the [symengine.py project](https://github.com/symengine/symengine.py). They are implemented using Cython, and they are free to introduce any kind of classes (including SymPy's `Expr` or Sage's `Expression` if needed), and the point of the wrappers is to make sure that things work out of the box from SymPy and Sage. The only job of the C++ SymEngine library is to ensure that the library's C++ API is implemented in such a way so that the wrappers can be written to do what they need. For example, we could easily introduce SymPy's `Expr` into the wrappers, by simply introducing the `Expr` class and make all the other classes subclass from it instead of from `Basic`.

That was the reason we split the wrappers, so now in the (pure) C++ `symengine/symengine` repository, we only have to worry about speed, correctness, maintainability and a usable API, and we can concentrate on these things without worrying or even testing any kind of wrappers. In the wrappers (`symengine/symengine.py`, or `.jl`, `.rb`), we simply just use the C++ (or C) API and the only thing we care is so that the (Python) wrapper can be used from sympy/Sage (and we test that in the test suite), and that it doesn't introduce unnecessary overhead in terms of speed. Ruby or Julia (or R) wrappers then care about interoperability with other libraries in those languages.

- [https://github.com/symengine/symengine.py](https://github.com/symengine/symengine.py)
- <https://github.com/symengine/symengine.rb>
- <https://github.com/symengine/SymEngine.jl>
- <https://github.com/symengine/symengine.R>

## Reference Counted Pointers

### Teuchos `RCP`

Memory management is handled by RCP (reference counted pointers) from
`Trilinos` (the module `Teuchos`). We have copied the relevant files into
`src/teuchos`, so no external dependencies need to be obtained. Brief code snippets of the
most frequent operations are given in our [C++ Style
Guide](style_guide.md), and should be consulted if you are unsure about
the syntax. In order to understand how these pointers work under the hood, read the
[Teuchos::RCP Beginner's
Guide](https://docs.trilinos.org/dev/packages/teuchos/doc/html/RefCountPtrBeginnersGuideSAND.pdf) (pdf).
Finally, a more thorough exposition is given in [Teuchos C++ Memory Management
Classes, Idioms, and Related Topics --- The Complete
Reference](https://docs.trilinos.org/dev/packages/teuchos/doc/html/TeuchosMemoryManagementSAND.pdf)
(pdf).

`Teuchos`' RCP implements reference counting of objects, in the exact way Python
does. When an object runs out of scope, its reference count is decreased. When
it is copied, its reference count is increased. When the reference count goes to
zero, it is deallocated. This all happens automatically, so; as long as our C++
Style Guide is followed, things just work.

When `CMAKE_BUILD_TYPE=Debug` is set during the `CMake` build (which is the
default type), then `Teuchos` is compiled with debugging support, which means
that as long as the C++ Style Guide is followed; the C++ code should never
segfault (since no access is provided to raw pointers that could segfault and
`Teuchos` raises a nice exception with full stack trace instead of raising a
segfault if there is any problem; this too, is reminiscent of very similar to
Python). Use this mode when developing.

When the production build is used; by setting `CMAKE_BUILD_TYPE=Release`, then
`Teuchos` is compiled without debugging support, which means that all pointer
operations become either as fast as raw pointers, or very close. As such, there
is pretty much zero overhead. However, in this mode, the program can segfault if
you access memory incorrectly. This segfault however would be prevented under
`CMAKE_BUILD_TYPE=Debug`, so always use the Debug build to test your code, only
when all tests pass should you enable Release mode.

The Trilinos RCP pointers as described above are only used when the
`WITH_SYMENGINE_RCP=OFF` is set in `CMake`. The default option is
`WITH_SYMENGINE_RCP=ON`, which uses our own implementation of `RCP` (see
`src/symengine_rcp.h`). Our implementation is faster, but it only implements a
subset of all the functionality and it requires that all our objects have a
`refcount_` variable. Otherwise the usage of our in-house RCP and the
`Teuchos::RCP` are identical, and continuous integration tests run both
implementations of RCP to make sure the code works with both.

### `Ptr` and `RCP`

The `RCP` has an overhead with every assignment due to the change
(increase/decrease) in the `refcount`. You can access the inner pointer as `Ptr`
(just call `.ptr()`), which has the same performance as raw pointer in Release
mode, yet it is 100% safe in Debug mode (i.e. if the original `RCP` goes out of
scope and the object deallocated; then the `Ptr` becomes dangling, but you get a
nice exception raised in Debug mode on subsequent access attempts ---- in
Release mode it will segfault or have undefined behavior, just like a raw
pointer). The idea is that for non-ownership access --- i.e. typically when you
just want to read some term in `Add`, we should be passing around `Ptr`, not
`RCP` (which has the extra `refcount` increment/decrement overhead, which
wasteful when we do not plan to own it). Such efficient implementations for the
basic classes have already been implmented in `SymEngine` and can be viewed [in the API documentation](https://github.com/symengine/symengine.py).

### `UniquePtr`

In terms of performance, the `std::unique_ptr` is similar to implementations involving raw pointers and manual calls to new and delete, so there are no reasons to use such manual new/delete calls and raw pointers; instead; one should use `std::unique_ptr`. One issue with `std::unique_ptr` is that if you get access to the raw pointer using `.get()`, then it will segfault if this pointer becomes dangling (i.e. there are no Debug time checks implemented in the standard library for this because it returns a raw pointer, not a `Ptr` object). This can however be fixed by writing a new class `UniquePtr` that returns a `Ptr` instead of a raw pointer and if you want to pass this around it is 100% Debug time checked, so it cannot segfault in Debug mode. Work on the implementation of this class has been ongoing in https://github.com/certik/trilinos/pull/1. The main bottleneck is that it needs to work with custom deallocators and be a drop-in replacement for `std::unique_ptr`, but it will be done in due time. The beauty of this new `UniquePtr` class is that together with `Ptr`, there will be no need to ever use manual new/delete calls and raw pointers. `UniquePtr` has the same performance in Release mode, yet it is 100% safe in Debug mode and allows for having your cake and eating it too. It's great.

However, the issue is that even manual new/delete patterns (or the equivalent `UniquePtr`) are slow, so we would like to avoid such operations, or perform them as little as possible. The feasibility of phasing out `RCP` in favor of `UniquePtr` is still under consideration. The benefits are substantial. It would mean that for example, the `Add` container would deallocate its contents (i.e. instead of having a hashtable full of `RCP` objects, it would have a hashtable full of `UniquePtr` objects), and on being accessed, would return a given term, which might just be a `Ptr` (which is very fast, but could become dangling if `Add` goes out of scope --- which would be checked at Debug time, so no segfault, but in Release builds it would segfault, and this error propagates for example; if one does an improper access at runtime from the Python wrappers in Release mode, it would segfault, which means then that the wrappers must be made aware of this behavior and prevented and must ensure such cases are not exposed to the user). Another simpler method is to make a copy of the object in such situations. For example, if you create some symbols and then use them in expressions, then currently we just pass around as `RCP`s, i.e. reference counted pointers to the original symbol. With the new approach, we would need to make a copy. Since we do not want to copy the `std::string` from inside Symbol, we want to store the symbols in some kind of table, and only pass a simple reference to the table (and also we need to deallocate things from the table if they are not used anymore). In other words, we just reinvented `RCP` again. So for Symbols, it seems that the `UniquePrt` wouldn't have many benefits. There might be cases where this formulation has some benefit for classes like `Add`. If they internally use `UniquePtr`, we can do an optimization in Release mode and store the contents directly in the hashtable (i.e. with no pointers at all), and still pass around the `Ptr` to other code (i.e in Debug mode it would use `UniquePtr`, thus we would make sure that things are not dangling, and in Release mode we just pass around `Ptr`, with the performance of a raw pointer, to the internal array), that way we avoid new/delete. Also with this one can do custom allocator, i.e. allocate a chunk of memory for the hashtable, and just do a placement new. This has been tested by the lead developer (Óndrej) and he was surprised to find that, the performance wasn't much different to `UniquePtr` (for smaller objects it was a bit faster, but for larger objects --- remember they are stored by value now --- it was even slower). Also the creation time for each type, `RCP` and `UniquePtr` was almost the same as well. The reason is that a simple refcount initialization is negligible in terms of time compared to the `new` call. What is slow is if you pass around `RCP` instead of `Ptr`, because a raw pointer (which is what `Ptr` is in Release mode) is much faster than a refcount increase/decrease. We should still investigate if we can get rid of new/delete using the approaches from this paragraph.

### Conclusion:

- We should pass around `Ptr` instead of `RCP` whenever possible, and we can do this right away.
- Use `UniquePtr` (after it is implemented) whenever possible instead of `RCP` --- though most places in `SymEngine` seem to require `RCP`. We should keep this in mind, there might still be one or two places where `UniquePtr` is the way to go.
- Never use raw new/delete calls and never use raw pointers (use `UniquePtr` + `Ptr`, and if it is not sufficient, use the slower `RCP` + `Ptr`).
- Never pass pointers to some internal data --- pass `Ptr` and have it checked at the Debug phase using `UniquePtr` in Debug mode, and use the data directly in Release mode

As an example of the last point, e.g. to give access to an internal `std::map` (as a pointer, so that the map is not copied), here is how to do it:

```c++
class A {
private:
#ifdef DEBUG_MODE
    UniquePtr<std::map<int, int> > m;
#else
    std::map<int, int> m;
#endif
public:
    Ptr<std::map<int, int>> get_access() {
#ifdef DEBUG_MODE
        return m.ptr();
#else
        return ptrFromRef(m);
#endif
    }
};
```

That way, in debug mode, you can catch dangling references but in the optimized mode it is optimally fast.

## Object creation and `is_canonical()`

Classes like `Add`, `Mul`, `Pow` are initialized through their constructor using their internal representation. `Add`, `Mul` have a `coeff` and `dict`, while `Pow` has a `base` and an `exp`. There are restrictions on what `coeff` and `dict` can be (for example `coeff` cannot be zero in `Mul`, and if `Mul` is used inside `Add`, then `Mul`'s coeff must be one, etc.). All these restrictions are checked when `SYMENGINE_ASSERT` is enabled inside constructors using the `is_canonical()` method. In this manner, you don't have to worry about creating `Add`/`Mul`/`Pow` with wrong arguments, as it will be caught by the tests. In the Release mode no checks are done, so you can construct `Add`/`Mul`/`Pow` very quickly. The idea is that depending on the algorithm, you sometimes know that things are already canonical, so you simply pass it directly to `Add`/`Mul`/`Pow` and you avoid expensive type checking and canonicalization. At the same time, you need to make sure that tests are still running with `SYMENGINE_ASSERT` enabled, so that `Add`/`Mul`/`Pow` is never in an inconsistent state.

The philosophy of SymEngine is that you impose as many restrictions as possible in the `is_canonical()` method for each class (and only check that in Debug mode), so that inside the class you can assume all those things can be taken for granted and thus call faster algorithms (e.g. in `Rational` you know it's not an integer, so you don't need to worry about that special case, at the same time if you have an integer, you are forced to use the `Integer` class, thus automatically using faster algorithms for just integers). Then the idea is to use the information about the algorithm to construct arguments of the SymEngine classes in canonical form and then call the constructor without any checks.

For cases where you can't or don't want to bother constructing in canonical form, we provide high-level functions like `add`, `mul`, `pow`, `rational`, where you just provide arguments that are not necessarily in canonical form, and these functions will check and simplify. E.g. `add(x, x)` will check and simplify to `Mul(2, x)`, e.g. you never have the instance `Add(x, x)`. In the same spirit, `rational(2, 1)` will check and convert to `Integer(2)`, e.g. you never have `Rational(2, 1)`.

Summary: always try to construct objects directly using their constructors and all the knowledge that you have for the given algorithm, that way things will be very fast. If you want slower but simpler code, you can use the `add()`, `mul()`, `pow()`, `rational()` functions that perform general and possibly slow canonicalization first.

## Operator Overloading

Ideally, we would like to be able to do:

    RCP<Basic> x  = make_rcp<Symbol>("x");
    RCP<Basic> y  = make_rcp<Symbol>("y");
    RCP<Basic> r = (x + y) + (y + x);
    std::cout << r << std::endl;

But the problem is, that the `+`, `-` and `<<` operations must be defined on the `RCP` objects.
However, just as you should not redefine what `double + double` is, you should not try to redefine operator overloading for an existing type (`RCP`). We can override operators for `Basic` objects, like so:

    ((*x) + (*y)) + ((*y) + (*x))

But here the problem is that the `+` operator only gets access to `Basic`, but it needs to access `RCP<Basic>`
for memory management. In order to allow for operator overloaded types that use dynamic memory allocation, we will need to create our own "handle" classes. It is hard to write a handle class in C++ that are const-correct and clean and simple to use for most C++ developers. It can be done, but it is very hard, especially since
we care about performance. In our opinion, we are better off writing such a layer in Python.
An example of handle classes is [2] --- it is non-const correct, but should give the ok performance.

Solution: using non-member non-friend functions is much more clear and much cleaner:

    add(add(x, y), add(y, x))

The function signature of `add` is:

    inline RCP<Basic> add(const RCP<Basic> &a, const RCP<Basic> &b);

For more complicated expressions, instead of `add`, we might also consider
using the naming scheme proposed in [1]. Another advantage of this approach is
that compiler errors are much easier to understand since it either finds
our function or it does not, while when overloading operators of our templated
classes (and RCP), any mistake typically results in pages of compiler errors in
gcc.

The Python wrappers then just call this `add` function and provide natural mathematical syntax `(x + y) + (y + x)` at the Python level.

[1] <https://docs.trilinos.org/dev/packages/thyra/doc/html/LinearAlgebraFunctionConvention.pdf>

[2] <http://www.math.ttu.edu/~kelong/Playa/html/>
