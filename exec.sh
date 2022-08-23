#!/bin/bash
export CurrentUseWine=$(which wine) &&
export WINEPREFIX=$HOME/.rowpref &&
export WINEESYNC=1 && 
export WINEFSYNC=1 &&
export ENV=cat $HOME/.rowpref/config.json | jq '.env' &&
if [-d $HOME/.rowpref/comWine] then export CurrentUseWine= $HOME/.rowpref/comWine fi &&
cp -r $WINEPREFIX/ClientSettings $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type d -name 'version-*') &&
$ENV $CurrentUseWine $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type f -name 'RobloxPlayerLauncher.exe') %U &&