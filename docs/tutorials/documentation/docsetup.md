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

Ensure the `conda` environment is setup. The task for the tutorials are under a separate `Rakefile` namespace, that is, the `tut:` space.

```bash
conda activate symedocs
rake clean
bundle exec filewatcher "docs/tutorials/Sphinx/**/*.{md,py}" "rake tut:mkDocs[html,nix]"
```

In another terminal, it is possible to run the development server so as to view the changes as they occur.

```bash
rake darkServe
```
