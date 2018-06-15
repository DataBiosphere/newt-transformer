# newt Roadmap

Newt is software meant to be useful in the general transformation 
of metadata for later indexing and querying. It is meant to work 
with a variety of metadata descriptions and should be easily 
extensible.

## Transforming JSON and beyond

Metadata serialized from the UC-CDIS platform provided the impetus 
for this software and currently can be used with the output of 
[sheepdog-exporter](https://pypi.org/project/sheepdog-exporter/).

As sheepdog-exporter's output changes, or as new valuable metadata 
serialization formats are found, newt should be able to transform
them.

Bug fixes will be made to the latest version of the software and 
previous versions are not expected to be maintained.

## Milestones

### Egg (towards 0.1)

Tranformer works to transform sheepdog-exporter data and is 
released to pypi.

### Tadpole 0.2

Can now transform DATS JSON-LD as created by NIH DCPPC Team Phosphorous.

### Eft 0.3

Contains features that make it easier to transform data in parallel by 
merging results.

### Torosa 0.4

Additional features address usability by improving the interface for 
generating bundles.

### Newt related name 0.5

Newt ships with a small server that allows translation functions to be 
configured and used over HTTP.

### Newt related name 0.6

Since newts present an extensible Python interface for managing metadata 
transformation, as new valuable metadata serialization formats are 
discovered they can be added easily.

### Newt related name 0.7

Newt presents an easily extensible Python API for transforming metadata
for a variety of metadata input and export formats. It has been demonstrated 
to be useful in generating bundle oriented metadata that has been 
indexed and made queryable. It can be reused to transform metadata and 
easily extended to new formats.

## Managing Changes to the Roadmap

Past the first two milestones, it is expected this roadmap will be 
reevaluated against specific indexing and querying use cases. If new 
highly valuable import or output formats are discovered, these will be
rearranged as necessary.

This is the first version of the roadmap.

This roadmap is largely dictated by use cases described in [Metadata Serialization](https://github.com/david4096/metadata-serialization) which is under active development to satisfy Key Capability 7 of National Institute of Health [Data Commons Pilot](https://pilot.nihdatacommons.us/). 


