import os, re, winreg, platform, shutil, requests, time

def get_steam_install_path():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam") # Default Place
        steam_path, regtype = winreg.QueryValueEx(registry_key, "SteamPath")
        winreg.CloseKey(registry_key)
        return steam_path
    except FileNotFoundError:
        print("Steam is not installed or the registry key could not be found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

steam_install_path = get_steam_install_path()
steamworld_games = {}
defualt_os_type = 64

def parse_vdf(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    paths = re.findall(r'"path"\s+"([^"]+)"', content)
    return paths

def parse_acf(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'"installdir"\s+"([^"]+)"', content)
    return matches[0] if matches else None

def find_steamworld_installations():
    global steam_install_path
    steam_path = steam_install_path.replace("/",'\\')
    drive_letters = [f"{chr(i)}:\\" for i in range(ord('a'), ord('z') + 1)]
    
    for drive in drive_letters:
        if steam_path.startswith(drive):
            steam_path = steam_path.replace(drive, drive.upper(), 1)
            break

    steam_path = f"{steam_path}\\steamapps"
    
    if '\\steam' in steam_path:
        steam_path = steam_path.replace('\\steam\\','\\Steam\\')
    
    if "\\program files (x86)" in steam_path:
        steam_path = steam_path.replace('\\program files (x86)','\\Program Files (x86)')

    library_folders_file = os.path.join(steam_path, 'libraryfolders.vdf')
    
    if not os.path.exists(library_folders_file):
        return None
    
    library_paths = parse_vdf(library_folders_file)
    library_paths.append(steam_path)

    steamworld_installations = []

    for path in library_paths:
        steamapps_path = os.path.join(path, 'steamapps')
        if not os.path.exists(steamapps_path):
            continue

        for file_name in os.listdir(steamapps_path):
            if file_name.startswith('appmanifest_') and file_name.endswith('.acf'):
                acf_file_path = os.path.join(steamapps_path, file_name)
                install_dir = parse_acf(acf_file_path)

                if install_dir and 'SteamWorld' in install_dir:
                    game_path = os.path.join(steamapps_path, 'common', install_dir)
                    steamworld_installations.append(game_path)

    return steamworld_installations

def none_found_mode(game_path=None,os_type=64):
    if game_path == None:exit(1)
    if "SteamWorld" not in game_path:print("Provided Game isn't a Valid SteamWorld Title.");exit(1)
    save_path = f"{os.path.dirname(__file__)}\\openalsoft.dll"
    os.system('cls')
    if not os.path.exists(save_path):
        if os_type == 64:
            print("Getting 64-Bit *.dll...")
            url = "https://github.com/Cracko298/SteamWorld-OpenAL-Fixer/releases/download/vDLL/64_oal.dll"
        else:
            print("Getting 32-Bit *.dll...")
            url = "https://github.com/Cracko298/SteamWorld-OpenAL-Fixer/releases/download/vDLL/32_oal.dll"
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to Download {os_type}-Bit *.dll\nStatus Code: {response.status_code}.")
            exit(1)

    print("Removing outdated OpenAL32.dll...")
    os.remove(f"{game_path}\\OpenAL32.dll")
    time.sleep(0.25)
    print("Copying over updated OpenAL32.dll...")
    time.sleep(0.25)
    shutil.copy2(save_path,f"{game_path}\\OpenAL32.dll")
    print("\nCompleted Patching/DLL Fix.\nGame Should work as intended now.")
    time.sleep(5)
    exit(1)

def auto_find_mode(os_type=64,game0=None,game1=None,game2=None,game3=None): # Build isn't affected by this Bug
    if game0 == None:exit(1)
    save_path = f"{os.path.dirname(__file__)}\\openalsoft.dll"
    os.system('cls')
    if not os.path.exists(save_path):
        if os_type == 64:
            print("Getting 64-Bit *.dll...")
            url = "https://github.com/Cracko298/SteamWorld-OpenAL-Fixer/releases/download/vDLL/64_oal.dll"
        else:
            print("Getting 32-Bit *.dll...")
            url = "https://github.com/Cracko298/SteamWorld-OpenAL-Fixer/releases/download/vDLL/32_oal.dll"
        time.sleep(1)
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to Download {os_type}-Bit *.dll\nStatus Code: {response.status_code}.")
            exit(1)
    
    print("Removing outdated OpenAL32.dll(s) from all Installations...")
    time.sleep(0.75);print(os.path.basename(game0));os.remove(f"{game0}\\OpenAL32.dll")
    if os.path.exists(game1):print(os.path.basename(game1));os.remove(f"{game1}\\OpenAL32.dll")
    if os.path.exists(game2):print(os.path.basename(game2));os.remove(f"{game2}\\OpenAL32.dll")
    if os.path.exists(game2):print(os.path.basename(game3));shutil.copy2(save_path,f"{game3}\\OpenAL32.dll")
    print("\nCopying over updated OpenAL32.dll(s) to all Installations...")
    time.sleep(0.75);print(os.path.basename(game0));shutil.copy2(save_path,f"{game0}\\OpenAL32.dll")
    if os.path.exists(game1):print(os.path.basename(game1));shutil.copy2(save_path,f"{game1}\\OpenAL32.dll")
    if os.path.exists(game2):print(os.path.basename(game2));shutil.copy2(save_path,f"{game2}\\OpenAL32.dll")
    if os.path.exists(game2):print(os.path.basename(game3));shutil.copy2(save_path,f"{game3}\\OpenAL32.dll")
    print("\nCompleted Patching/DLL Fixes.\nGame(s) Should work as intended now.")
    time.sleep(5)
    exit(1)

if __name__ == '__main__':
    architecture = platform.architecture()[0]
    if architecture == "64bit": defualt_os_type = 64
    else: defualt_os_type = 32
    installations = find_steamworld_installations()
    if installations:
        for i, install in enumerate(installations):
            gametype = os.path.basename(install)
            install = install.replace('\\\\','\\')
            install = install.replace('\\','/')
            steamworld_games[f"{i+1}"] = install
            
    else:
        print("No SteamWorld Installations Found.\nPlease Provide a PATH to the Game Installation.")
        user_i = input("Provide your SteamWorld Game PATH: ")
        user_i = user_i.replace("\\","/")
        user_i = user_i.replace('"',"")
        none_found_mode(user_i,defualt_os_type)
        exit(1)

    exception_list = ["Build"] # Build uses Unity, and not the latest version of Image & Forms inhouse Engine. No work is needed to be done, as such it's excluded.
    steamworld_games_copy = steamworld_games.copy()

    for k, v in steamworld_games_copy.items():
        if any(keyword in k or keyword in str(v) for keyword in exception_list):
            del steamworld_games[k]
    for i, values in enumerate(steamworld_games.values(), 1):
        globals()[f"var{i}"] = str(values)
    for i in range(1, len(steamworld_games) + 1):
        print(globals()[f"var{i}"])
    print("\nAttempting to Path/Fix All detected Installations...")
    time.sleep(0.5)
    if 'var3' in globals() and 'var4' in globals():
        auto_find_mode(defualt_os_type, var1, var2, var3, var4)
    elif 'var3' in globals() and 'var4' not in globals():
        auto_find_mode(defualt_os_type, var1, var2, var3)
    elif 'var2' in globals() and 'var3' not in globals():
        auto_find_mode(defualt_os_type, var1, var2)
    else:
        auto_find_mode(defualt_os_type, var1) # If no games found, this is useless, and instead calls 'none_found_mode()'