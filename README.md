# LessBrute
This script is designed to filter wordlists by [lespass](https://github.com/lesspass/lesspass) master-password fingerprint (3 emoji). Use this tool for educational purposes only.

# Usage
```
[gifi@ThinkPad lessbrute]$ python3 lessbrute.py -h
usage: lessbrute.py [-h] [-o OUTPUT] [-f] [-i] wordlist fingerprint

Filter lesspass wordlist by fingerprint

positional arguments:
  wordlist              path to word list
  fingerprint           the fingerprint to match (e.g., "💴 🎓 ₿")

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (default: match.txt)
  -f, --first           stop after first match
  -i, --icons           show available icons
```