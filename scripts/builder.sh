#! /usr/bin/env nix-shell
#! nix-shell deps.nix -i bash

# Build Doxygen
cd docs/Doxygen
doxygen Doxyfile-mcss.cfg

# Build Sphinx
cd ../Sphinx
make html
