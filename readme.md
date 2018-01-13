# DroPass - Automatically Encrypting Text File Editor

>An encrypted text file on your computer is safer than a browser extension password manager. Think of how it would be compromised: someone would need to get at least user-level access to your computer, and then either read it when it's temporarily unencrypted, or wait for you to unencrypt it. That cannot be done by efficient attackers at scale. And if they've compromised your machine, you have bigger things to worry about. - [Sean Cassidy](https://www.seancassidy.me/browser-extension-password-managers-should-not-be-used.html)

## Dependencies:
- Python 3+
- Cryptography (python module, you can install it via pip)

## How to use: Just run main.py from the command line (e.g python3 main.py)
1. Decide on where your new encrypted file is to be stored
2. Once you have the path, enter it into the config as the program prompts you to. 
3. Choose a strong and secure master password which will be used to encrypt your file. MAKE SURE YOU DO NOT LOSE THIS AS IT WILL NOT BE STORED ANYWHERE!!! You should write it down since you will need to re-enter this password every time you wish you edit your file. 
4. You can then edit your file. Be sure to save before closing. 

## Keyboard shortcuts:
### - Ctrl-s to save file (file will be automatically encrypted with your master password when saved - plaintext will be deleted - gone -  once you close the editor). Cool thing to notice is that every time you save, a new IV will be randomly generated so the ciphertext will be completely different to before (even if the plaintext is exactly the same)! Pretty cool imo. 
### - Ctrl-w to close editor 
### - Ctrl-a to select all
### - Ctrl-l to select current line 

# Please be aware that the undo function is somewhat buggy so don't count on being able to undo any changes you make to the file. 
