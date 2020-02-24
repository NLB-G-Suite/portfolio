#Note: Start both this and the oracle virtual box with admin privileges.

c:
cd %programfiles%\oracle\virtualbox
VBoxManage.exe internalcommands createrawvmdk -filename "f:\Gdrive\Apps\Images\usb.vmdk" -rawdisk \\.\PhysicalDrive8