let
  sources = import ./../nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  inherit (pkgs.lib) optional optionals;
  customPython = pkgs.poetry2nix.mkPoetryEnv { projectDir = ./../.; };
in pkgs.runCommand "dummy" {
  buildInputs = with pkgs; [ doxygen customPython ];
} ""
