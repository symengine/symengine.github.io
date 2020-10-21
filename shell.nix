# -*- mode: nix-mode -*-
let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  customPython = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
  doxyrest =
    pkgs.callPackage ./nix/pkgs/doxyrest.nix { pythonEnv = customPython; };
in pkgs.mkShell { buildInputs = with pkgs; [ doxygen rake lcov darkhttpd ]; }
