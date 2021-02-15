# Following Along
Though the static version of the site is of use as a supplement to the API docs, users will benefit maximally by playing around with the code snippets.

## Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Symengine/symengine.github.io/sources)

- Note that the `binder` instance can take up-to fifteen minutes for the first build
- It is therefore not very highly recommended

## Locally
In order to run these tutorials locally, the following setup is suggested [[^1]]:

```bash
# First run
conda env create -f symedocs.yml
# On pulls and syncs
conda env update -f symedocs.yml
# Activate
conda activate symedocs
# Generate ipynb
rake genJup
```

### Running

The simplest way is to now spin up the `jupyter-server` and navigate through the `use/` folders.

```bash
# In an activated environment
jupyter-server
```


[^1]: To **add** to the documentation, see the {ref}`contributing` details
