import sys
import common
import directory


def modes():
    if sys.argv[2] == '':
        directory.root()
    elif common.args.mode == 'full_episodes':
        directory.full_episodes()
    else:
        print common.args

modes()
sys.modules.clear()
