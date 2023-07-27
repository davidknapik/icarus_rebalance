#!/bin/sh

# clean up
cd /c/Temp/icarus
rm -rf staging
rm mymod.pak
rm modfiles.txt

# create modfiles.txt
cd /c/Temp/icarus/icarus_rebalance 
git diff --name-only master..rocket data/ > /c/Temp/icarus/modfiles.txt

# build staging area
cd /c/Temp/icarus
mkdir staging
rsync -avz --files-from=modfiles.txt icarus_rebalance staging/.

# build mod file
cd staging/data
/c/Temp/icarus/repak/repak.exe pack --version V11 --mount-point ../../../Icarus/Content/data/ . /c/Temp/icarus/mymod.pak


