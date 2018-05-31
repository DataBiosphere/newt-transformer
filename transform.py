#!/usr/local/bin/python3.6
import json
import logging
import sys
import uuid
from collections import namedtuple
from typing import Generator

import argparse


MetadataLink = namedtuple('MetadataLink', ['source_field_name', 'linked_field_name', 'link_name'])


class Transformer:

    @staticmethod
    def _build_data_objects_dict(data_objects: list):
        return {entry['id']: entry for entry in data_objects}


    @staticmethod
    def _build_metadata_dict(input_metadata):
        def build_metadata_field(metadata, field_name: str):
            """
            Builds dict from metadata where key is node_id, value is the corresponding metadata
            """
            return {entry['node_id']: entry for entry in metadata[field_name]}
        for field in input_metadata:
            input_metadata[field] = build_metadata_field(input_metadata, field)
        return input_metadata

    def __init__(self, input_dict: dict):
        self._metadata = self._build_metadata_dict(input_dict['metadata'])
        self._data_objects_dict = self._build_data_objects_dict(input_dict['data_objects'])
        self._metadata_links = [MetadataLink('aligned_reads_index', 'submitted_aligned_reads', 'submitted_aligned_reads_files.id'),
                                MetadataLink('submitted_aligned_reads', 'read_group', 'read_groups.id#1'),
                                MetadataLink('read_group', 'aliquot', 'aliquots.id'),
                                MetadataLink('aliquot', 'sample', 'samples.id#1'),
                                ]

    @staticmethod
    def _get_link(metadata_field: dict, link_key: str) -> dict:
        return metadata_field['link_fields'][link_key]

    def _add_file_to_bundle(self, bundle, link_source):
        file_key = bundle['metadata'][link_source]['object_id']
        file_dict = self._data_objects_dict[file_key]
        bundle['manifest'].append(file_dict)

    def _add_metadata_field(self, metadata_dict, source_field_name: str, linked_field_name: str, link_name :str):
        linked_field_key = metadata_dict[source_field_name]['link_fields'][link_name]
        linked_field_dict = self._metadata[linked_field_name][linked_field_key]
        metadata_dict[linked_field_name] = linked_field_dict

    def _build_bundle(self, bundle: dict):
        for link_details in self._metadata_links:
            self._add_metadata_field(bundle['metadata'], *link_details)

        bundle['manifest'] = []
        self._add_file_to_bundle(bundle, 'aligned_reads_index')
        self._add_file_to_bundle(bundle, 'submitted_aligned_reads')

        bundle['bundle_did'] = str(uuid.uuid4())

    def transform(self) -> Generator[dict, None, None]:
        """
        Builds bundles from the initialized metadata

        :return: bundle generator
        """
        def index_to_bundle(aligned_read_index):
            # prepackage the bundle with the tree root that is used to fill in the rest of the fields
            metadata_dict = {'aligned_reads_index': aligned_read_index}
            bundle = {'metadata': metadata_dict}
            self._build_bundle(bundle)
            return bundle
        return (index_to_bundle(aligned_read_index)
                for aligned_read_index in self._metadata['aligned_reads_index'].values())


def open_json_file(json_path):
    """opens and parses json file at path"""
    with open(json_path, 'r') as fp:
        return json.load(fp)


def write_output(bundles: Generator[dict, None, None], out_file):
    with open(out_file, 'w') as fp:
        json.dump(list(bundles), fp)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json', help='metadata json to be transformed')
    parser.add_argument('--output-json', dest='output_json',
                        help='where to write transformed output.', required=False,
                        default='out.json')

    options = parser.parse_args(argv)

    json_dict = open_json_file(options.input_json)
    transformer = Transformer(json_dict)
    bundle_list = list(transformer.transform())
    write_output(bundle_list, options.output_json)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    main(sys.argv[1:])
