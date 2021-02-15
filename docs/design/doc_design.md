# Documentation Design

As befitting a project of SymEngine's scope, a discussion of the documentation design is appropriate. The overall design is spread across multiple repositories, but unified under a single domain.

```{note}
Not covered in this design document are the **manual** benchmarking requirements, and the project todo strategy
```

## Goals

The documentation goals are:

- Link to the API documentation when appropriate
- Allow each language binding to build and control the API documentation builds
- Supplement the existing channels of communication

In particular, the third point means that there is to be a clear separation of content between the User Wiki, the API documentation, and the main site.

## Decisions

These decisions codify the guiding principles of the documentation.

### No Versioning

Search engines are typically thrown by versions, e.g. CMake and its documentation setup; and since backward compatibility is not necessarily guaranteed, there is no point hosting multiple versions.

However, only the latest stable set of bindings are to be described here; that is; those published with the official distribution system, `conda`.

### Review Tutorials

The contents of the tutorials (the ones linked from the [organization site](https://symengine.org)) are built with sphinx-dust to ensure that they are checked routinely; every $60$ days by default.

### Doc Warnings are Errors

The documentation is built weekly, as discussed in the next section; and all warnings are treated as errors.

## Implementation

### CI and Hosting

All builds are through isolated [Github Actions](https://github.com/features/actions) jobs and hosted with [Github Pages](https://pages.github.com/). The documentation is rebuilt weekly on a `cron` job, and also tested for each pull request and push for the API and the main site.

### API Bindings

Given the separation of concerns; each language binding is built in the most native fashion; currently this means the tools

| **Language** |                                                           **Tool** |
| :----------- | -----------------------------------------------------------------: |
| `C++`        |                                 [Doxygen](https://www.doxygen.nl/) |
| `R`          |                              [pkgdown](https://pkgdown.r-lib.org/) |
| `Python`     |                    [Sphinx](https://www.sphinx-doc.org/en/master/) |
| `Julia`      | [Documenter.jl](https://juliadocs.github.io/Documenter.jl/stable/) |

Additionally, to ensure cross-linking of references; the `C++` outputs are additionally parsed with parsed with [sphinx](https://www.sphinx-doc.org/en/master/) using [doxyrest](https://github.com/vovkos/doxyrest).

### Main Site

The main site is meant to serve as an entry point to new users.

#### Build System

The site is to be built in production with the `rake` tasks provided; though for local development other methods and helpers are provided.

```{note}
Several common errors can be caught with the `prePub` task
```

#### Content and Syntax

The content is to be written in [Markedly Structured Text](https://myst-parser.readthedocs.io/) or `myST`, which is a super-set of [CommonMark markdown](https://commonmark.org/) and has additional extensions for Jupyter Notebooks (with [myST-NB](https://myst-nb.readthedocs.io/en/latest/) and [jupytext](https://jupytext.readthedocs.io/en/latest/)) and [reStructured Text](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).

Files which are meant to be **executed**; that is those which are tangled with `jupytext` **must have** the `.myst.md` extension.

```{warning}
Failure to specify the extension in the YAML header under the `text_representation` key in each `.myst.md` file **will cause unexpected behavior**
```

#### Interactivity

Every tutorial must be accompanied by the following:

Binder Button [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Symengine/symengine.github.io/sources)
: The launch in binder is to populated manually and placed on the first heading of the file and should point to the appropriate `myst.md` file which is on the `sources` branch

```{warning}
The `.binder/environment.yml` must be kept in sync with the `symedocs.yml` file
```

Colab Button [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Symengine/symengine.github.io/notebooks)
: The launch button, like the binder button above should point to the appropriate file, which in this case is the `.ipynb` file on the `notebooks` branch

Local Button [![Local Installation](https://img.shields.io/badge/Local-Instructions-orange)](https://symengine.org/use/tutorial.html)
: This button is required, and should direct the user to the [tutorial follow along instructions](../use/tutorial.md)

Furthermore, the tutorials **are to be proofread** every $60$ days, otherwise the `cron` builds will start to fail.

## Acknowledgments

Apart from the tireless efforts of the core development team and volunteers; part of the documentation process was supported over the course of the 2020 Season of Docs.

```{reviewer-meta}
:written-on: "2021-02-14"
:proofread-on: "2021-02-16"
:dust-days-limit: 360
```
