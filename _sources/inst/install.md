# Installation

Here we will discuss the different methods of interacting with the `symengine` library. This effectively involves two main options:

- Core C++ library
- Library Bindings
  - Python
  - Julia

We will start with a discussion on replicating the Jupyter setup which is used for the Binder interactive samples on the website.

## Jupyter Setup

This is the simplest aspect of this guide, as it is automated and requires only [miniconda, which can be obtained here](https://docs.conda.io/en/latest/miniconda.html)[^1]. Once this is obtained and activated, the setup involves a setup and update step.

```{code-cell} bash
# First run
conda env create -f symedocs.yml
# On pulls and syncs
conda env update -f symedocs.yml
# Activate
conda activate symedocs
```

At this stage we can now load the Jupyter environment to run the tutorials.

[^1]: Note that due to a version mismatch with RabbitMQ, we can't use Anaconda
