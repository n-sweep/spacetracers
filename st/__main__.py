import os
from api import ST


def main():
    token_fp = os.path.expanduser('~/.config/st/tokens')
    st = ST(token_fp)


if __name__ == '__main__':
    main()
