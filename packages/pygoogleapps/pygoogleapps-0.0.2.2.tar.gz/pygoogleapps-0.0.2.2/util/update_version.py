import re
import argparse

parser = argparse.ArgumentParser(description='See or update the version number.')
parser.add_argument('--next', '-n', action='store_true', help='iterate to the next lowest-dimension version')
parser.add_argument('--milestone', '-m', action='store_true', help='iterate to the next milestone (second-order) version update')
parser.add_argument('--explicit', '-e', help='specify an explicit full version number')
args = parser.parse_args()

with open("VERSION.txt", "r") as fh:
    version = fh.read().strip()

match_exp = r'\.(\d+)\.(\d+)(?!\.|\d)'
regex = re.search(match_exp, version)

if not regex:
    raise Exception("Cannot determine milestone and revision information!")

milestone = regex.group(1)
rev = regex.group(2)

if args.next:
    version = re.sub(match_exp, f".{milestone}." + str(int(rev) + 1), version)

if args.milestone:
    version = re.sub(match_exp, "." + str(int(milestone) + 1) + f".{rev}", version)

if args.explicit:
    version = args.explicit

print('['+version+']')

with open("VERSION.txt", "w") as fh:
    fh.write(version)
