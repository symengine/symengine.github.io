# -*- mode: nix-mode -*-
# See https://github.com/HaoZeke/quip-nix
{ pythonVersion ? "38" }:
let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  inherit (pkgs.lib) optional optionals;
  buildpkgs = import ./nix { };
  hook = ''
    # Python Stuff
     export PIP_PREFIX="$(pwd)/_build/pip_packages"
     export PYTHONPATH="$(pwd)/_build/pip_packages/lib/python3.8/site-packages"
     export PATH="$PIP_PREFIX/bin:$PATH"
     unset SOURCE_DATE_EPOCH
  '';
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "2.2.2";
  });
  customPython = mach-nix.mkPython {
    pypi_deps_db_commit = "b5cd0ee30c9a3e4f076374fc4c90cdc4e5f17d3c";
    pypi_deps_db_sha256 =
      "0gkklm0zb3pjxkkvvsda0ckvxb54mnqyxz31pwcjxjpx9jlqlbld";
    requirements = ''
      pip
      # Documentation
        # exhale
        # sphinxcontrib-napoleon
        Jinja2
        coverxygen
        # Literate
        jupytext
        # Reproduce
        papermill
        papermill-jupytext
        # renku
        # Extended Python
        mypy
        typeguard
        returns
        pydantic
        # Formatters
        isort
        black
        darglint
        flake8
        # Coverage
        coverage
        codecov
        # Misc
        bump2version
    '';
    pkgs = pkgs;
  };
in pkgs.mkShell {
  buildInputs = with pkgs; [
    # Required for the shell
    zsh
    perl
    git
    direnv
    fzf
    ag
    fd

    # Docs
    doxygen
    # Core
    black
    customPython
  ];
  shellHook = hook;
}
