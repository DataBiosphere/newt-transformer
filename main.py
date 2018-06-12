#!/usr/local/bin/python3.6
import json
import logging
import sys

import argparse
import typing

from transform.gen3 import Gen3Transformer


def open_json_file(json_path):
    """opens and parses json file at path"""
    with open(json_path, 'r') as fp:
        return json.load(fp)


def write_output(bundles: typing.Iterator[dict], out_file):
    with open(out_file, 'w') as fp:
        json.dump(list(bundles), fp)


def add_parser_to_subparser(sub_parser, parse_name, parse_help):
    """used to give all sub-parsers the same arguments"""
    parser = sub_parser.add_parser(parse_name, help=parse_help)

    parser.add_argument('input_json', help='metadata json to be transformed')
    parser.add_argument('--output-json', dest='output_json',
                        help='where to write transformed output.', required=False,
                        default='out.json')


def main(argv):
    parser = argparse.ArgumentParser()

    transform_source = parser.add_subparsers(dest='transform_source', help='Metadata source format')

    add_parser_to_subparser(transform_source, 'gen3', 'Gen3 metadata as formatted by sheepdog exporter')

    options = parser.parse_args(argv)

    json_dict = open_json_file(options.input_json)
    transformer = Gen3Transformer(json_dict)
    bundle_iterator = transformer.transform()
    write_output(bundle_iterator, options.output_json)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    main(sys.argv[1:])
