#!/bin/bash
#####################################################
#  Grab the notebooks in .myst.md form
#
#  Author: Rohit Goswami
#  Licence: MIT
#####################################################

groot=$(git rev-parse --show-toplevel)

# CPP
cppdir="$groot/docs/use/api/cpp"
if [ -d "$cppdir" ]; then
    echo "Folder exists!!! Y to overwrite"
    read delfol
    if [ $delfol == "Y" ]; then
        rm -rf $cppdir
    else
        echo "Exiting"
        exit 1
    fi
fi
echo "Getting files"
"$groot/scripts/gitfolder.sh" "https://github.com/symengine/symengine/tree/master/docs/mystMD"
echo "Moving to the API directory"
mv mystMD $cppdir
rm -rf $cppdir/readme.org
echo "Done CPP"

echo "Remember to commit changes to symengine/symengine!!!"
