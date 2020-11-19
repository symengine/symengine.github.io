# Symengine Wiki

The user-wiki for the Symengine project.

```{tip}
You may be looking for the [API documentation instead](https://symengine.github.io/api-docs/index.html)
```

## Generating Tutorials

In order to run these tutorials locally, the following setup is suggested:

```{code-cell} bash
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

```{code-cell} bash
# In an activated environment
jupyter-server
```

## Other Resources

- [API Documentation](https://symengine.github.io/api-docs)
- [Mailing List](https://groups.google.com/g/symengine)
- [GH Wiki](https://github.com/symengine/symengine/wiki)
- [Gitter](https://gitter.im/symengine/symengine?at=53ac6f80b7f5a3321716c7eb)
