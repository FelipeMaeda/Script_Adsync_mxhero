# Script_Adsync_mxhero
Script to synchronize existing domains in MxHero database (mysql) in AdSync database (sqlite3).

### Instalation:

Clone this repo and move the script in the base directory of the AdSync.

```sh
git clone https://github.com/FelipeMaeda/Script_Adsync_mxhero.git
mv Script_Adsync_mxhero/script_sync.py /root/ADSynCode/mxG-ADSync/
chmod a+x /root/ADSynCode/mxG-ADSync/script_sync.py
```

### Usage:
This script uses the AdSync virtual interpreter to perform the synchronization. To run, change the login credentials in Script and the name of MxHero registered in AdSync.

cd /root/ADSynCode/mxG-ADSync/
./script_sync.py
