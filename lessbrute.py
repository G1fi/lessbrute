import argparse
import hashlib
import hmac
import time
import sys
import os

ICONS = (
    '#️', '❤️', '🏨', '🎓', '🔌',
    '🚑', '🚌', '🚗', '✈️', '🚀',
    '🚢', '🚇', '🚚', '💴', '💶',
    '₿', '💵', '💷', '🗄️', '📈',
    '🛏️', '🍺', '🔔', '🔭', '🎂',
    '💣', '💼', '🐛', '📷', '🛒',
    '⭐', '☕', '☁️', '☕', '🗨️',
    '📦', '🍴', '🖥️', '💎', '❗',
    '👁️', '🏁', '⚗️', '⚽', '🎮',
    '🎓'
)


def get_icon(hash_slice):
    return int(hash_slice, base=16) % 46


def get_fingerprint(hmac_sha256):
    return (
        get_icon(hmac_sha256[0:6]),
        get_icon(hmac_sha256[6:12]),
        get_icon(hmac_sha256[12:18])
    )


def get_hmac_sha256(password_bytes):
    return hmac.new(password_bytes, digestmod=hashlib.sha256).hexdigest()


def process_line(line, fingerprint, output_file, find_first):
    line = line.strip()
    hmac_sha256 = get_hmac_sha256(line.encode('utf-8'))

    if get_fingerprint(hmac_sha256) == fingerprint:
        print(line)
        with open(output_file, 'a') as f:
            f.write(line + '\n')
        if find_first:
            sys.exit(0)


def process_file(wordlist, fingerprint, output_file, find_first):
    with open(wordlist, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            process_line(line, fingerprint, output_file, find_first)


def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description='Filter lesspass wordlist by fingerprint')
    parser.add_argument('wordlist', metavar='wordlist', type=str, help='path to word list')
    parser.add_argument('fingerprint', metavar='fingerprint', type=str, help='the fingerprint to match (e.g., "💴 🎓 ₿")')
    parser.add_argument('-o', '--output', type=str, default='match.txt', help='output file (default: match.txt)')
    parser.add_argument('-f', '--first', action='store_true', help='stop after first match')
    parser.add_argument('-i', '--icons', action='store_true', help='show available icons')

    args = parser.parse_args()
    
    if args.icons:
        print('/'.join(ICONS))
        sys.exit(0)
    
    if ' ' not in args.fingerprint:
        print(f'Error: Icons must be separated by spaces.')
        sys.exit(1)
        
    fingerprint = args.fingerprint.split()
    
    if len(fingerprint) != 3:
        print(f'Error: There should be 3 icons ({len(fingerprint)} provided)')
        sys.exit(1)
    
    for icon in fingerprint:
        if icon not in ICONS:
            print(f'Error: Invalid fingerprint icon - {icon}.')
            sys.exit(1)
            
    if not os.path.isfile(args.wordlist):
        print(f'Error: The file "{args.wordlist}" does not exist.')
        sys.exit(1)
    
    with open(args.output, 'w') as f:
        pass
    
    print(f'Searching for fingerprint: {args.fingerprint}')
    
    fingerprint = tuple([ICONS.index(icon) for icon in fingerprint])
    process_file(args.wordlist, fingerprint, args.output, args.first)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Processing time: {elapsed_time:.2f} seconds')


if __name__ == '__main__':
    main()
