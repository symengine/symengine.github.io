# Documentation

This section describes the workflow used for generating, testing, and contributing to the documentation.

## Local Setup

The generation of the docs depends primarily on `miniconda`.

```bash
tree
.
```

## Contributions

Ensure the `conda` environment is setup. The task for the wiki contributions are under a separate `Rakefile` namespace, that is, the `tut:` space.

```bash
conda activate symedocs
rake clean
rake writeDocs
```

Run the task to convert notebooks to markdown, or recall the manual option:

```bash
jupytext --to ipynb firststeps.md
jupytext mynotebook.ipynb --to myst
```
