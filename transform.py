#!/usr/local/bin/python3.6
import logging
import sys


class Transformer:

    def __init__(self):
        pass
        # we should take in:
        #   - a dict equiv of sheepdog output
        #   - exactly which metadata fields we care about


def main(args):
    print('success')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    main(sys.argv[1:])
