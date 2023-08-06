# Import the argparse library
import argparse
import os
import sys
import platform
import requests
import stat
import subprocess

def main():
    PLATFORM_MAP = {'Linux': 'linux',
                    'Darwin': 'mac',
                    'Windows': 'windows'}

    def get_install_dir(package: str, platform: str):
        if platform == 'linux' or platform == 'mac':
            return "/usr/local/bin"
        elif platform == 'windows':
            return os.path.join('C:\Program Files', package, "bin")

    def get_install_file(install_dir: str, package: str, platform: str):
        if platform == 'linux' or platform == 'mac':
            return os.path.join(install_dir, package)
        elif platform == 'windows':
            return os.path.join(install_dir, f'{package}.exe')

    def get_download_temp_file(package: str, platform: str):
        if platform == 'linux' or platform == 'mac':
            return os.path.join(os.environ['HOME'],  f'gro_snap_temp_file_{package}')
        else:
            raise Exception("Shouldn't be using a temp file on Windows")


    PLATFORM = PLATFORM_MAP[platform.system()]
    DOWNLOAD_ENDPOINT = "http://10.20.25.249:8001/download?path=packages"

# Create the parser
    grosnap_parser = argparse.ArgumentParser(description='grosnap makes it easy to install and upgrade custom Gro binaries')
    subparsers = grosnap_parser.add_subparsers(help="grosnap commands")
    install_parser = subparsers.add_parser('install', help="Install a binary package")
    install_parser.add_argument('package', type=str, help='The name of the package to install')
    install_parser.add_argument('--upgrade', default=False, action='store_true')
    install_parser.set_defaults(install_parser=True)

    args = grosnap_parser.parse_args()

    if 'install_parser' in args and args.install_parser:
        print(f"Installing {args.package}")
        install_dir = get_install_dir(args.package, PLATFORM)
        install_file = get_install_file(install_dir, args.package, PLATFORM)
        print(f"Installation directory: {install_dir}")
        print(f"Installation file: {install_file}")
        fetch_url = f"{DOWNLOAD_ENDPOINT}/{args.package}/{PLATFORM}/latest/{args.package}"
       
        if PLATFORM=='windows':
            fetch_url+=".exe"
            if not os.path.isdir(install_dir):
                try:
                    os.makedirs(install_dir, exist_ok=True)
                except PermissionError:
                    raise Exception(f"\n\nCan't get permission to create directory {install_dir}! Try running 'as administrator'")
                except Exception as e:
                    raise Exception(e)
            
            result = subprocess.run(["powershell", f"if ($Env:PATH -notlike '*{args.package}*') {{$oldpath = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).path;", 
                f'$newpath = “$oldpath;{install_dir}";' 
                , "Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH -Value $newPath",
             f"}} else {{echo '{args.package} dir already on PATH, thus will not add again'}}"], capture_output=True)
            print(result)
            assert result.returncode == 0, f"Couldn't add {args.package} to PATH--try running 'as administrator'"
        
        #Download appropriate version of package to directory where it should go
        already_installed = False
        if os.path.isfile(install_file):
            already_installed=True
        
        if already_installed and not args.upgrade:
            print(f"Detected an existing installation of {args.package}. Run with --upgrade to overwrite with the latest version")
            sys.exit()

        if already_installed:
            print(f"Detected an existing installation of {args.package}, will upgrade to latest version")

        #Download the file 
        print(f"Downloading {args.package} through Twingate...")
        
        #If on Windows, we download directly to the relevant directory
        if PLATFORM=='windows':
            try:
                with open(install_file, "wb") as f:
                    response = requests.get(fetch_url)
                    if response.status_code==200:
                        f.write(response.content)
                    else:
                        raise Exception(f"Download failed, server response: {response.text}")
            except PermissionError:
                raise Exception(f"\n\nCan't get permission to write to {install_file}! Try running 'as administrator'")
            except Exception as e:
                raise Exception(e)

        elif PLATFORM=='linux' or PLATFORM=='mac':
            #For permissions reasons, on UNIX we first download to a temp directory and then move the file into place in /usr/local/bin
            try:
                download_temp_file = get_download_temp_file(args.package, PLATFORM)
                with open(download_temp_file, "wb") as f:
                    response = requests.get(fetch_url)
                    if response.status_code==200:
                        f.write(response.content)
                    else:
                        raise Exception(f"Download failed, server response: {response.text}")
            except PermissionError:
                raise Exception(f"\n\nCan't get permission to write to {download_temp_file}!")
            except Exception as e:
                raise Exception(e)

            #Now move the file into place
            if os.getenv("RUNNING_IN_DOCKER", False)=='true':
                #If we are in Docker, we don't need sudo
                move_res = subprocess.run(["mv", download_temp_file, install_file])
            else:
                try:
                    move_res = subprocess.run(["sudo", "mv", download_temp_file, install_file])
                except FileNotFoundError as e:
                    if 'sudo' in str(e):
                        raise Exception("Could not find sudo. If running in Docker, have you set the RUNNING_IN_DOCKER env variable to 'true'?")
                    else:
                        raise Exception(e)
                except Exception as e:
                    raise Exception(e)
            assert move_res.returncode==0, f"Couldn't move {download_temp_file} to {install_file}!"

        else:
            raise Exception(f"Platform {PLATFORM} not recognized!")

        #Set file to have execute permissions
        print(f"Setting {args.package} to be executable")
        try:
            st = os.stat(install_file)
            os.chmod(install_file, st.st_mode | stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)
        except:
            raise Exception(f"Couldn't make the file {install_file} executable. Try running 'as administrator' on Windows")
        
        if already_installed:
            print(f"Have successfully upgraded {args.package} to the latest version")
        else:
            print(f"Have successfully installed {args.package}. You can access it by running {args.package} on the command line.")
            if PLATFORM == 'windows':
                print(f"\nPlease restart your computer to update your PATH variable so that it includes {args.package}")
            else:
                print(f"\nIf {args.package} does not work in terminal, please make sure that /usr/local/bin is on your PATH variable.")
