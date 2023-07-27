#!/bin/sh

BASEDIR='/c/Temp/icarus'

# clean up
echo -e "\n# Cleaning up old build"
cd $BASEDIR
rm -rf icarus_staging
rm icarus_mod.pak
rm modfiles.txt


# create modfiles.txt
echo -e "\n# Creating modfile.txt"
cd $BASEDIR/icarus_mod/icarus_rebalance 
git diff --name-only mod..rocket data/ > $BASEDIR/modfiles.txt

# build staging area
echo -e "\n# Create & populate staging area"
cd $BASEDIR
mkdir icarus_staging
rsync -avz --files-from=modfiles.txt icarus_mod/icarus_rebalance icarus_staging/.

# validate json files
echo -e "\n# Validate JSON files"
find icarus_staging -type f -name '*.json' -exec python icarus_utils/icarus_rebalance/utils/validate_json.py {} \;

# build mod file
echo -e "\n# Create icarus_mod.pak"
cd icarus_staging/data
$BASEDIR/repak/repak.exe pack --version V11 --mount-point ../../../Icarus/Content/data/ . $BASEDIR/icarus_mod.pak


