# -*- mode: nix-mode -*-
let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  customPython = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./.; };
in pkgs.mkShell {
  buildInputs = with pkgs; [ doxygen customPython rake lcov darkhttpd ];
}
