#! /usr/bin/env nix-shell
#! nix-shell deps.nix -i bash

# Build Doxygen
cd docs/Doxygen
doxygen Doxyfile-syme.cfg

# Build Sphinx
cd ../Sphinx
make html
mv build/html ../../public

# Local Variables:
# mode: shell-script
# End:
