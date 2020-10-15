# Documentation

This section describes the workflow used for generating, testing, and contributing to the documentation.

## Local Setup

The generation of the docs depends primarily on `miniconda`, with some partial support for `nix`.

```bash
tree
.
```

## API Contributions

## Tutorial Contributions

Ensure the `conda` environment is setup. For working on tutorial contributions, it is not always desirable rebuild the API documentation (which can take up 2 minutes). The environment variable `dev` can be set to prevent them from being rebuilt.

```bash
conda activate symedocs
export dev="True"
rake clean
bundle exec filewatcher "docs/Sphinx/source/**/*.{md,py}" "rake mkDocs[html,nix]"
```

In another terminal, it is possible to run the development server so as to view the changes as they occur.

```bash
rake darkServe
```
