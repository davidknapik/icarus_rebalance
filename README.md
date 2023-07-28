# icarus_rebalance
Rebalance Icarus from RocketWerkz 

Starting from this mod:
[https://github.com/WZG-Mods/wzg-icarus-balance-overhaul]
Check out their code & motivation

I wanted to see what it took to build my own modifications and pak files, and have attempted to document my process here.

## Environment
MINGW64 bash shell (with rsync & other gnu tools)

Unreal Editor (Epic) v4.26.2 (for unrealpak.exe)

repack [https://github.com/trumank/repak] (I used this as for some reason the Unreal pak.exe was giving an error when reading the rocketwerkz file)

winmerge

## GIT repository

Branch
mod  == mod files & release

rocket == original game files from RocketWerkz

utils == some utility files


## Updating the rocket branch
Upon release of new icarus/Icarus/Content/Data/data.pak file

Workspace Setup
```
$ cd /c/Temp/icarus
$ mkdir icarus_mod
$ cd icarus_mod
$ git clone --branch rocket git@github.com:davidknapik/icarus_rebalance.git
```

Populate rocket branch with new content
```
# Copy RocketWerkz data.pak file delivered through steam 
$ cp /d/Steam/steamapps/common/Icarus/Icarus/Content/Data/data.pak /c/Temp/icarus/icarus_mod/icarus_rebalance/.
$ cd /c/Temp/icarus/icarus_mod/icarus_rebalance
$ git checkout rocket
$ rm -rf data
$ /c/Temp/icarus/repak/repak.exe unpack -s "D:/BA/work/92bbbfa44df12262/Temp/Data/" data.pak -f
$ rm data.pak

# force unix line endings
$ find . -type f -name '*.json' -exec dos2unix {} \;

# verify changes
$ git status
$ git diff

# commit RocketWerkz changes into rocket branch 
$ git commit -m 'RocketWerkz WXX' -a

# push changes to remote repo
$ git push
```

## Merge rocket branch into mod

Workspace Setup
```
# Checkout mod branch
$ cd /c/Temp/icarus
$ mkdir icarus_mod
$ cd /c/Temp/icarus/icarus_mod
$ git clone --branch mod git@github.com:davidknapik/icarus_rebalance.git
```

Check out separate rocket branch directory
(I prefer using the diff/merge across the two repo directories instead of the builtin git mergetool)
```
$ cd /c/Temp/icarus
$ mkdir icarus_rocket
$ cd icarus_rocket
$ git clone --branch rocket git@github.com:davidknapik/icarus_rebalance.git
```

Verify and merge changes that are newly added into rocket branch, this is basically a manual and time intensive process as not to revert the actual modded data back to the original, while implementing new features released from RocketWerkz
```
$ cd /c/Temp/icarus
$ /c/Program\ Files/WinMerge/winmergeu.exe -r -e -u -wl /c/Temp/icarus/icarus_rocket/icarus_rebalance/data /c/Temp/icarus/icarus_mod/icarus_rebalance/data 
```

## Validate json files
In case some end of line commas got messed up somewhere.

Wrote a simple validate_json python script to read in files from the command line and validate the JSON

Workspace Setup
```
$ cd /c/Temp/Icarus
$ mkdir icarus_utils
# clone repo into icarus_utils
$ cd /c/Temp/icarus/icarus_utils
$ git clone --branch utils git@github.com:davidknapik/icarus_rebalance.git
```

```
$ cd /c/Temp/icarus
$ find icarus_mod -type f -name '*.json' -exec python icarus_utils/icarus_rebalance/utils/validate_json.py {} \;
```

## Commit merged rocket data into the 'modification' master
The icarus_mod directory should now have the new rocketwerkz conent merged in
```
$ cd /c/Temp/icarus/icarus_mod/icarus_rebalance

# verify you are on the 'mod' branch
$ git status

# commit updates
$ git commit -m 'merged Wxx updates' -a

# push to repo
git push
```

# Build mymod.pak

## Creating modfiles.txt 

Workspace setup
```
$ cd /c/temp/icarus
$ mkdir icarus_mod
$ git clone --branch mod git@github.com:davidknapik/icarus_rebalance.git
$ cd icarus_rebalance

# verify both branches mod and rocket are availabe locally
$ git branch
* mod
  rocket

# if rocket is missing, use the switch command to enable
$ git switch rocket

# make sure to switch back to the 'mod' branch before continuing
$ git switch mod
```

Build a list of files that are different than the original
```
$ cd /c/temp/icarus/icarus_mod/icarus_rebalance
$ git diff --name-only mod..rocket data/ > /c/Temp/icarus/modfiles.txt
```

## Sync changed files to staging area
Workspace Setup
```
$ cd /c/Temp/icarus
$ mkdir icarus_staging
```

Sync changed files (in modfiles.txt) to staging area
```
$ cd /c/Temp/icarus
$ rsync -avz --files-from=modfiles.txt icarus_mod/icarus_rebalance icarus_staging/.
```

## Build icarus_mod.pak file
Using 'repak.exe' to build pak file from the icarus_staging directory
```
$ cd /c/Temp/icarus/icarus_staging/data
$ /c/Temp/icarus/repak/repak.exe pack --version V11 --mount-point ../../../Icarus/Content/data/ . /c/Temp/icarus/icarus_mod.pak

Packed 28 files to icarus_mod.pak
```


## Verify/List file

### Using repak

Info
```
$ /c/Temp/icarus/repak/repak.exe info icarus_mod.pak

mount point: ../../../Icarus/Content/data/
version: V11
version major: FNameBasedCompression
28 file entries
```

List
```
$ /c/Temp/icarus/repak/repak.exe list icarus_mod.pak

Alterations/D_Alterations.json
Armour/D_ArmourSetBonus.json
Crafting/D_ProcessorRecipes.json
Inventory/D_InventoryInfo.json
Items/D_ItemRewards.json
Items/D_ItemTemplate.json
Items/D_ItemsStatic.json
Items/Types/D_BuildingTypes.json
MetaWorkshop/D_WorkshopItems.json
Modifiers/D_ModifierStates.json
Stats/D_ProspectStats.json
Talents/D_Talents.json
Tools/D_AmmoTypes.json
Tools/D_FirearmData.json
Tools/D_ToolDamage.json
Traits/D_Armour.json
Traits/D_Ballistic.json
Traits/D_Consumable.json
Traits/D_Decayable.json
Traits/D_Durable.json
Traits/D_Energy.json
Traits/D_Equippable.json
Traits/D_Fillable.json
Traits/D_Generator.json
Traits/D_Itemable.json
Traits/D_Processing.json
Traits/D_Thermal.json
World/D_OreDeposit.json
```

### Using unrealpak.exe

Info
```
$ /d/Epic\ Games/UE_4.26/Engine/Binaries/Win64/unrealpak.exe /c/temp/icarus/icarus_mod.pak -info

LogPakFile: Display: Using command line for crypto configuration
LogPakFile: Display: Pak File: C:/temp/icarus/icarus_mod.pak
LogPakFile: Display:     Version: 8
LogPakFile: Display:     IndexOffset: 8353966
LogPakFile: Display:     IndexSize: 2358
LogPakFile: Display:     IndexHash: 43FEA220052A10F8FC5961E95DEE11B8B674C4CB
LogPakFile: Display:     bEncryptedIndex: 0
LogPakFile: Display:     EncryptionKeyGuid: 00000000000000000000000000000000
LogPakFile: Display:     CompressionMethods:
LogPakFile: Display:         None
LogPakFile: Display: Unreal pak executed in 0.021631 seconds
```

Verify
```
$ /d/Epic\ Games/UE_4.26/Engine/Binaries/Win64/unrealpak.exe /c/temp/icarus/icarus_mod.pak -verify

LogPakFile: Display: Using command line for crypto configuration
LogPakFile: Display: Checking pak file "C:/temp/icarus/icarus_mod.pak". This may take a while...
LogPakFile: Display: Pak file "C:/temp/icarus/icarus_mod.pak" healthy, 28 files checked.
LogPakFile: Display: Pak file "C:/temp/icarus/icarus_mod.pak" checked in 0.02s
LogPakFile: Display: Unreal pak executed in 0.020993 seconds
```

List
```
$ /d/Epic\ Games/UE_4.26/Engine/Binaries/Win64/unrealpak.exe /c/temp/icarus/icarus_mod.pak -list

LogPakFile: Display: Using command line for crypto configuration
LogPakFile: Display: Mount point ../../../Icarus/Content/data/
LogPakFile: Display: "Alterations/D_Alterations.json" offset: 0, size: 73794 bytes, sha1: BE047DDB4A7D4CEFB204F93F3230BFBA9B5788A0, compression: None.
LogPakFile: Display: "Armour/D_ArmourSetBonus.json" offset: 73847, size: 9363 bytes, sha1: E16AF9283162DA99B71AAAA47DAEA46AA54A491B, compression: None.
LogPakFile: Display: "Crafting/D_ProcessorRecipes.json" offset: 83263, size: 1445279 bytes, sha1: E4D00C11360E0A5D500D5D8BC30FA5195D8F44D2, compression: None.
LogPakFile: Display: "Inventory/D_InventoryInfo.json" offset: 1528595, size: 39593 bytes, sha1: AE76B1A50992CC3A654840F08EC062EE10AF91D6, compression: None.
LogPakFile: Display: "Items/D_ItemRewards.json" offset: 1568241, size: 562188 bytes, sha1: B7221D1CF90039431663F0A00AF85A1B36D37E74, compression: None.
LogPakFile: Display: "Items/D_ItemTemplate.json" offset: 2130482, size: 234726 bytes, sha1: EB6D6348823A90225AF14FC4CB075DE3A3C275AD, compression: None.
LogPakFile: Display: "Items/D_ItemsStatic.json" offset: 2365261, size: 2983251 bytes, sha1: 0773567CFDE590C3E3582A331C25531E02BB8B10, compression: None.
LogPakFile: Display: "Items/Types/D_BuildingTypes.json" offset: 5348565, size: 4442 bytes, sha1: 769B465A67B6A17FBC013DD56C5309B2917B3099, compression: None.
LogPakFile: Display: "MetaWorkshop/D_WorkshopItems.json" offset: 5353060, size: 157920 bytes, sha1: 80CBE3F50D52EC51C8EF329FAE451A957E8BA9E9, compression: None.
LogPakFile: Display: "Modifiers/D_ModifierStates.json" offset: 5511033, size: 318433 bytes, sha1: D92B03C9F8F8091BF5BF4F6DCD1E2B4276C09072, compression: None.
LogPakFile: Display: "Stats/D_ProspectStats.json" offset: 5829519, size: 10701 bytes, sha1: 1D58F3B62FB48CA78DD9DE346868BFCB7C943C92, compression: None.
LogPakFile: Display: "Talents/D_Talents.json" offset: 5840273, size: 982064 bytes, sha1: 7A6278C74FA193F06D787B100915CCDBF940EA6C, compression: None.
LogPakFile: Display: "Tools/D_AmmoTypes.json" offset: 6822390, size: 6756 bytes, sha1: B8F5F6D7375C0C353E344FAB2EA22715E747DC64, compression: None.
LogPakFile: Display: "Tools/D_FirearmData.json" offset: 6829199, size: 80219 bytes, sha1: AD5BBA65A1B1D18BC6FD6C2F6F560EA7DDD573C0, compression: None.
LogPakFile: Display: "Tools/D_ToolDamage.json" offset: 6909471, size: 15367 bytes, sha1: 134C3416826C7E3559A022A23541612236CFDBF4, compression: None.
LogPakFile: Display: "Traits/D_Armour.json" offset: 6924891, size: 129237 bytes, sha1: C2098FF509AB5C687F4A5DD71A7D0626D99015E3, compression: None.
LogPakFile: Display: "Traits/D_Ballistic.json" offset: 7054181, size: 161144 bytes, sha1: 9FC45D46C48B48C6CF4B2AB840E733E46C69BB3E, compression: None.
LogPakFile: Display: "Traits/D_Consumable.json" offset: 7215378, size: 70658 bytes, sha1: 710716BB034B0793EC1C751E059734FC29959620, compression: None.
LogPakFile: Display: "Traits/D_Decayable.json" offset: 7286089, size: 4359 bytes, sha1: A42378F34CE8F8019F93D60BBF1EF156352C0F27, compression: None.
LogPakFile: Display: "Traits/D_Durable.json" offset: 7290501, size: 44242 bytes, sha1: 6289D7B2D4CB1AE12C2617E4BF2417F1ADC0388F, compression: None.
LogPakFile: Display: "Traits/D_Energy.json" offset: 7334796, size: 6372 bytes, sha1: 2D3E5632397CDF30D58EE7B06E579C81D7A1D70E, compression: None.
LogPakFile: Display: "Traits/D_Equippable.json" offset: 7341221, size: 15837 bytes, sha1: BF7820879FEB6353120B36D544D9DE12B0A73B41, compression: None.
LogPakFile: Display: "Traits/D_Fillable.json" offset: 7357111, size: 7355 bytes, sha1: 95745529F9873B9FAF426CE7F8FBF74F60E0841B, compression: None.
LogPakFile: Display: "Traits/D_Generator.json" offset: 7364519, size: 10528 bytes, sha1: 2A710D48A00BBFD892111F1CE6D8A431224B0E71, compression: None.
LogPakFile: Display: "Traits/D_Itemable.json" offset: 7375100, size: 950184 bytes, sha1: 4036BB8BC6808EA6B629C77231946F82B376410C, compression: None.
LogPakFile: Display: "Traits/D_Processing.json" offset: 8325337, size: 13245 bytes, sha1: 301E6B35270C33AF526703A6226FD510F75F4600, compression: None.
LogPakFile: Display: "Traits/D_Thermal.json" offset: 8338635, size: 5097 bytes, sha1: EFDF31325A047D10FFCDF525548DE12969145ABF, compression: None.
LogPakFile: Display: "World/D_OreDeposit.json" offset: 8343785, size: 9999 bytes, sha1: 87D4AB03F9D086B60CF5787A73079D14E0F1F55C, compression: None.
LogPakFile: Display: 28 files (8352353 bytes), (0 filtered bytes).
LogPakFile: Display: Unreal pak executed in 0.039118 seconds
```

# Deploy mymod.pak

Copy the icarus_mod.pak file to the local icarus game directories and any dedicated server directories (if running a dedicated server)
```
$ cp /c/temp/icarus/icarus_mod.pak /d/Steam/steamapps/common/Icarus/Icarus/Content/Paks/mods/.

$ scp /c/temp/icarus/icarus_mod.pak owner@192.168.1.55:/home/owner/Games/icarus/Icarus/Content/Paks/mods/.
```
