# __main__.py

import argparse


def main():

    parser = argparse.ArgumentParser(description='Telegram Connector.')

    parser.add_argument('--token', dest='token',
                        type=str,
                        required=True,
                        help='token set')

    args = parser.parse_args()

    print(args.token)


if __name__ == "__main__":
    main()
