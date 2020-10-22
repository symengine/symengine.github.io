# Documentation

This section describes the workflow used for generating, testing, and contributing to the documentation.

## Local Setup

The generation of the docs depends primarily on `miniconda`, with some partial support for `nix`.

```bash
tree
.
```

## API Contributions

## Wiki Contributions

Ensure the `conda` environment is setup. The task for the wiki contributions are under a separate `Rakefile` namespace, that is, the `tut:` space.

```bash
conda activate symedocs
rake clean
bundle exec filewatcher "docs/wiki/Sphinx/**/*.{md,py}" "rake tut:mkDocs[html,nix]"
```

In another terminal, it is possible to run the development server so as to view the changes as they occur.

```bash
rake darkServe
```

Run the task to convert notebooks to markdown, or recall the manual option:

```bash
jupytext --to ipynb firststeps.md
jupytext mynotebook.ipynb --to myst
```
