import typing
import uuid
from collections import namedtuple

from newt.transform.abstract import AbstractTransformer


# Welcome to the gen3 transformer. Here is an overview of how the gen3 data is parsed and transformed.
#
# To transform data from sheepdog's gen3 output we need to parse the dictionaries that sheepdog outputs.
# Each of these are parsed and stored in self._data_objects_dict (although not all are used). These
# dictionaries contain metadata of their respective categories, but the metadata is linked to other
# metadata fields in other categories and data objects only by reference.
#
# Starting with 'aligned_reads_index' we can get all of the related data files and metadata just by
# following the links in the metadata. These links are hardcoded in MetadataLink tuples. This little
# network of connected metadata and files is what ends up comprising a bundle.
#
# The metadata for a bundle is linked together pretty consistently and is done iteratively using
# self._add_metadata_field(). Files are linked in a slightly different way, so a different helper
# function (self._add_file_to_bundle()) takes care of this process.


"""A metadata link is all the information necessary to get metadata
for a particular field from the field that links to it."""
MetadataLink = namedtuple('MetadataLink', ['source_field_name', 'linked_field_name', 'link_name'])


class Gen3Transformer(AbstractTransformer):

    @staticmethod
    def _build_data_objects_dict(data_objects: list):
        return {entry['id']: entry for entry in data_objects}

    @staticmethod
    def _build_metadata_dict(input_metadata):
        def build_metadata_field(metadata, field_name: str, key: str):
            """
            Builds dict from metadata where key is node_id, value is the corresponding metadata
            """
            return {entry[key]: entry for entry in metadata[field_name]}
        for field in input_metadata:
            if field == 'project' or field == 'program':
                key = 'id'
            else:
                key = 'node_id'
            input_metadata[field] = build_metadata_field(input_metadata, field, key)
        return input_metadata

    def __init__(self, input_dict: dict) -> None:
        super().__init__()
        self._metadata = self._build_metadata_dict(input_dict['metadata'])
        self._data_objects_dict = self._build_data_objects_dict(input_dict['data_objects'])
        self._metadata_links = [MetadataLink('aligned_reads_index', 'submitted_aligned_reads',
                                             'submitted_aligned_reads_files.id'),
                                MetadataLink('submitted_aligned_reads', 'read_group', 'read_groups.id#1'),
                                MetadataLink('read_group', 'aliquot', 'aliquots.id'),
                                MetadataLink('aliquot', 'sample', 'samples.id#1'),
                                MetadataLink('sample', 'case', 'cases.id'),
                                ]

    def _add_file_to_bundle(self, bundle: dict, link_source: str):
        source_dict = bundle['metadata'][link_source]
        file_key = source_dict['object_id']
        file_dict = self._data_objects_dict[file_key]

        # The format of the bundle is a little broken. Here we fix it:
        # put filename in file_dict since it's only stored in the metadata for some reason...
        file_name = source_dict['file_name']
        file_dict['name'] = file_name
        # This is ugly and sketchy, but should do the job for now
        file_dict['updated_datetime'] = file_dict['created'] + 'Z'
        bundle['manifest'].append(file_dict)

    def _add_metadata_field(self, metadata_dict, source_field_name: str, linked_field_name: str, link_name: str):
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

    def transform(self) -> typing.Iterator[dict]:
        def index_to_bundle(aligned_read_index):
            # prepackage the bundle with the tree root that is used to fill in the rest of the fields
            metadata_dict = {'aligned_reads_index': aligned_read_index}
            bundle = {'metadata': metadata_dict}
            self._build_bundle(bundle)
            return bundle
        return (index_to_bundle(aligned_read_index)
                for aligned_read_index in self._metadata['aligned_reads_index'].values())
