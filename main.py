# Imports
import subprocess
import sys
import os
from os.path import exists
import time
import getpass
import shutil
import wget
import json
# variables
user=getpass.getuser()
homeFolder=f'/home/{user}/'
config=open('config.json','r')
# Check Packages
try:
    subprocess.check_output("jq --version",stderr=subprocess.STDOUT,shell=True)
except subprocess.CalledProcessError:
    print('Please install JQ!')
    sys.exit()
# functions
def graphicApiChange(directory,choice):
    jsonLocation=directory+'/ClientAppSettings.json'
    if choice=='vulkan':    
        with open(jsonLocation,'w') as file:
            file.write('{"FFlagDebugGraphicsPreferVulkan": true }')
    elif choice=='opengl':
        with open(jsonLocation,'w') as file:
            file.write('{"FFlagDebugGraphicsPreferOpenGL": true,\n "FFlagGraphicsGLUseDefaultVAO": true }')
    elif choice=='dxvk':
        with open(jsonLocation,'w') as file:
            file.write('{"FFlagDebugGraphicsPreferD3D11": true }')
def revertChanges():
    try:
        shutil.rmtree(homeFolder+'.rowpref')
        os.remove(f'{homeFolder}.local/share/applications/Rowblox.desktop')
        print('Uninstall Complete')
    except FileNotFoundError:
        print("Rowblocks doesn't seem to be installed in this machine!")
def lookForVersionFolder():
    obj = os.scandir(f'{homeFolder}.rowpref/drive_c/users/{user}/AppData/Local/Roblox/Versions')
    for entry in obj:
        if entry.is_dir:
            return f"{homeFolder}.rowpref/drive_c/users/{user}/AppData/Local/Roblox/Versions/{entry.name}/"
def installRblx():
    # Checks for packages
    try:
        subprocess.check_output("wine --version",stderr=subprocess.STDOUT,shell=True)
    except subprocess.CalledProcessError:
        print('Please install wine!')
        sys.exit()
    if os.path.exists(homeFolder+'.rowpref'):
        shutil.rmtree(homeFolder+'.rowpref')
        print('Pre-existing prefix folder, deleting!')
    os.system(f'chmod +x {os.getcwd()}/exec.sh')
    # Set up wineprefix
    print('--------------------------------------------\nSetting up WinePrefix\n--------------------------------------------')
    time.sleep(2)
    path = os.mkdir(f'{homeFolder}.rowpref')
    os.system(f'WINEPREFIX={homeFolder}.rowpref wine init')
    print('--------------------------------------------\nWinePrefix Made\n--------------------------------------------')
    time.sleep(1)
    # Install rblx
    print('--------------------------------------------\nInstalling Roblox\n--------------------------------------------')
    wget.download('https://setup.rbxcdn.com/RobloxPlayerLauncher.exe',out='/home/zion/.rowpref')
    os.popen(f'WINEPREFIX={homeFolder}.rowpref wine {homeFolder}.rowpref/RobloxPlayerLauncher.exe').read()
    # input('----------------------\n Press any key as soon as roblox is done installing to proceed with installation. \n----------------------')
    print('--------------------------------------------\nFinished Rblx Installation\n--------------------------------------------')
    # Final Setup
    if os.path.exists(f'{homeFolder}.rowpref/drive_c/users/{user}/AppData/Local/Roblox') == False:
        print('Roblox installation not found.')
    verDirect=lookForVersionFolder()
    clientSDir=os.mkdir(verDirect+'ClientSettings')
    os.mkdir(f'{homeFolder}.rowpref/ClientSettings')
    mainDir=f'{homeFolder}.rowpref/ClientSettings'
    grapAPI=input('Which graphics API will you be using with roblox[[1]vulkan*,[2]opengl,[3]dxvk]')
    if grapAPI=='1':
        graphicApiChange(mainDir, 'vulkan')
    elif grapAPI=='2':
        graphicApiChange(mainDir, 'opengl')
    elif grapAPI=='3':
        graphicApiChange(mainDir, 'dxvk')
    else:
        graphicApiChange(mainDir, 'vulkan')
    os.popen(f'cp exec.sh {homeFolder}.rowpref/ && cp config.json {homeFolder}.rowpref/')
    with open(f'{homeFolder}.local/share/applications/Rowblox.desktop','w') as f:
    #    f.write("[Desktop Entry]\nName=Rowblox\nExec=bash -c 'CurrentUseWine=$(which wine) && export WINEPREFIX=$HOME/.rowpref && export WINEESYNC=1 && export WINEFSYNC=1 && cp -r $WINEPREFIX/ClientSettings $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type d -name 'version-*') && $CurrentUseWine $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type f -name 'RobloxPlayerLauncher.exe') '%U'\nMimeType=x-scheme-handler/roblox-player\nType=Application\nTerminal=true")
        f.write("[Desktop Entry]\nName=Rowblox\nExec=$HOME/.rowpref/exec.sh %u\nMimeType=x-scheme-handler/roblox-player\nType=Application\nTerminal=true")
    #    f.write("[Desktop Entry]\nName=Rowblox\nExec=bash -c 'export CurrentUseWine=$(which wine) && export WINEPREFIX=$HOME/.rowpref && export WINEESYNC=1 && export WINEFSYNC=1 && ENV=cat $HOME/.rowpref/config.json | jq '.env' && if [-d $HOME/.rowpref/comWine]; then export CurrentUseWine= $HOME/.rowpref/comWine fi && cp -r $WINEPREFIX/ClientSettings $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type d -name 'version-*') && $ENV $CurrentUseWine $(find $WINEPREFIX/drive_c/users/$USER/AppData/Local/Roblox/Versions -type f -name 'RobloxPlayerLauncher.exe') %U'\nMimeType=x-scheme-handler/roblox-player\nType=Application\nTerminal=true")
    os.popen('xdg-mime default "Rowblox.desktop" x-scheme-handler/roblox-player')
    print('--------------------------------------------\nInstallation Finished')
    startup()
def texturesDelete():
    versFold=lookForVersionFolder()
    pcFold=versFold+'PlatformContent/pc/'
    print(pcFold)
    os.rename(pcFold+'textures',pcFold+' texturesR')
    startup()
def conf():
    oldcon=json.load(config)
    ans=input("Old env:"+ oldcon['env']+'\nNew env:')
    oldcon['env']=ans
    json.dump(oldcon,open('config.json','w'),indent=6)
    if os.path.exists(homeFolder+'.rowpref'):
        os.popen(f'cp config.json {homeFolder}.rowpref/')
    startup()
def startup():
    print('--------------------------------------------')
    aestartin = input('Welcome to the store what do you need?\n[1]Install Roblox\n[2]Uninstall Roblox\n[3]Edit Config\n[4]Delete Textures\n[other]Exit\ninput: ')
    if aestartin=='1':
        installRblx()
    elif aestartin=='2':
        revertChanges()
        startup()
    elif aestartin=='3':
        conf()
    elif aestartin=='4':
        texturesDelete()
    else:
        sys.exit()
# Main Code
if __name__=='__main__':
    startup()