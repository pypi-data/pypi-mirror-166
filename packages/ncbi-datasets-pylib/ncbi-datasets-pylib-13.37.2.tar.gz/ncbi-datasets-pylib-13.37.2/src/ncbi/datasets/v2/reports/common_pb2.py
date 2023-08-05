# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v2/reports/common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ncbi.datasets.options import report_pb2 as ncbi_dot_datasets_dot_options_dot_report__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%ncbi/datasets/v2/reports/common.proto\x12\x18ncbi.datasets.v2.reports\x1a\"ncbi/datasets/options/report.proto\"\xc2\x05\n\x05\x45rror\x12\x63\n\x13\x61ssembly_error_code\x18\x06 \x01(\x0e\x32\x31.ncbi.datasets.v2.reports.Error.AssemblyErrorCodeH\x00R\x11\x61ssemblyErrorCode\x12W\n\x0fgene_error_code\x18\x07 \x01(\x0e\x32-.ncbi.datasets.v2.reports.Error.GeneErrorCodeH\x00R\rgeneErrorCode\x12Z\n\x10virus_error_code\x18\x08 \x01(\x0e\x32..ncbi.datasets.v2.reports.Error.VirusErrorCodeH\x00R\x0evirusErrorCode\x12\x16\n\x06reason\x18\x05 \x01(\tR\x06reason\x12\x18\n\x07message\x18\x02 \x01(\tR\x07message\x12/\n\x11valid_identifiers\x18\x03 \x03(\tB\x02\x18\x01R\x10validIdentifiers\x12/\n\x13invalid_identifiers\x18\x04 \x03(\tR\x12invalidIdentifiers\"\x86\x01\n\x11\x41ssemblyErrorCode\x12\x1f\n\x1bUNKNOWN_ASSEMBLY_ERROR_CODE\x10\x00\x12\x1a\n\x16INVALID_BIOPROJECT_IDS\x10\x01\x12!\n\x1dNO_ASSEMBLIES_FOR_BIOPROJECTS\x10\x02\x12\x11\n\rINVALID_TAXON\x10\x03\"J\n\rGeneErrorCode\x12\x1b\n\x17UNKNOWN_GENE_ERROR_CODE\x10\x00\x12\x1c\n\x18INCOMPLETE_LOOKUP_SYMBOL\x10\x05\".\n\x0eVirusErrorCode\x12\x1c\n\x18UNKNOWN_VIRUS_ERROR_CODE\x10\x00\x42\x06\n\x04\x63ode\"\xe7\x04\n\x07Warning\x12_\n\x11gene_warning_code\x18\x07 \x01(\x0e\x32\x31.ncbi.datasets.v2.reports.Warning.GeneWarningCodeH\x00R\x0fgeneWarningCode\x12\x16\n\x06reason\x18\x02 \x01(\tR\x06reason\x12\x18\n\x07message\x18\x03 \x01(\tR\x07message\x12M\n\x0breplaced_id\x18\x04 \x01(\x0b\x32,.ncbi.datasets.v2.reports.Warning.ReplacedIdR\nreplacedId\x12\x37\n\x17unrecognized_identifier\x18\x05 \x01(\tR\x16unrecognizedIdentifier\x1a\x46\n\nReplacedId\x12\x1c\n\trequested\x18\x01 \x01(\tR\trequested\x12\x1a\n\x08returned\x18\x02 \x01(\tR\x08returned\"\xf0\x01\n\x0fGeneWarningCode\x12\x1d\n\x19UNKNOWN_GENE_WARNING_CODE\x10\x00\x12\x1e\n\x1a\x41\x43\x43\x45SSION_VERSION_MISMATCH\x10\x01\x12\x14\n\x10REPLACED_GENE_ID\x10\x02\x12\x18\n\x14\x44ISCONTINUED_GENE_ID\x10\x03\x12\x18\n\x14UNRECOGNIZED_GENE_ID\x10\x04\x12\x1c\n\x18UNRECOGNIZED_GENE_SYMBOL\x10\x05\x12\x1a\n\x16UNRECOGNIZED_ACCESSION\x10\x06\x12\x1a\n\x16UNRECOGNIZED_TAX_TOKEN\x10\x07\x42\x06\n\x04\x63ode\"\x8c\x01\n\x07Message\x12\x37\n\x05\x65rror\x18\x01 \x01(\x0b\x32\x1f.ncbi.datasets.v2.reports.ErrorH\x00R\x05\x65rror\x12=\n\x07warning\x18\x02 \x01(\x0b\x32!.ncbi.datasets.v2.reports.WarningH\x00R\x07warningB\t\n\x07message\"^\n\x0fLineageOrganism\x12\"\n\x06tax_id\x18\x01 \x01(\rB\x0b\xc2\xf3\x18\x07\x32\x05\x31\x31\x31\x31\x38R\x05taxId\x12\'\n\x04name\x18\x02 \x01(\tB\x13\xc2\xf3\x18\x0f\x32\rCoronaviridaeR\x04name\"\xfd\x05\n\x08Organism\x12@\n\x06tax_id\x18\x01 \x01(\rB)\xc2\xf3\x18%\n\x06tax-id\x12\x0cTaxonomic ID2\x04\x39\x36\x30\x36\x32\x07\x32\x36\x39\x37\x30\x34\x39R\x05taxId\x12\x1d\n\x08sci_name\x18\x02 \x01(\tB\x02\x18\x01R\x07sciName\x12\xd8\x01\n\rorganism_name\x18\x07 \x01(\tB\xb2\x01\xc2\xf3\x18K\n\x04name\x12\x04Name2\x0cHomo sapiens2/Severe acute respiratory syndrome coronavirus 2\xca\xf3\x18%\x12#The scientific name of the organism\xd2\xf3\x18\x36\n\x0fscientific_name\x12#The scientific name of the organismR\x0corganismName\x12]\n\x0b\x63ommon_name\x18\x03 \x01(\tB<\xc2\xf3\x18\x38\n\x0b\x63ommon-name\x12\x0b\x43ommon Name2\x05human2\x08pangolin2\x04MERS2\x05SARS2R\ncommonName\x12\x43\n\x07lineage\x18\x05 \x03(\x0b\x32).ncbi.datasets.v2.reports.LineageOrganismR\x07lineage\x12\x1a\n\x06strain\x18\x06 \x01(\tB\x02\x18\x01R\x06strain\x12i\n\x17pangolin_classification\x18\x08 \x01(\tB0\xc2\xf3\x18,\n\x08pangolin\x12\x17Pangolin Classification2\x07\x42.1.1.7R\x16pangolinClassification\x12\x89\x01\n\x13infraspecific_names\x18\t \x01(\x0b\x32,.ncbi.datasets.v2.reports.InfraspecificNamesB*\xc2\xf3\x18&\n\x0einfraspecific-\x12\x14Infraspecific Names R\x12infraspecificNames\"\x8e\x03\n\x12InfraspecificNames\x12\x39\n\x05\x62reed\x18\x01 \x01(\tB#\xc2\xf3\x18\x1f\n\x05\x62reed\x12\x05\x42reed2\x08Hereford2\x05\x62oxerR\x05\x62reed\x12\x39\n\x08\x63ultivar\x18\x02 \x01(\tB\x1d\xc2\xf3\x18\x19\n\x08\x63ultivar\x12\x08\x43ultivar2\x03\x42\x37\x33R\x08\x63ultivar\x12\x38\n\x07\x65\x63otype\x18\x03 \x01(\tB\x1e\xc2\xf3\x18\x1a\n\x07\x65\x63otype\x12\x07\x45\x63otype2\x06\x41lpineR\x07\x65\x63otype\x12j\n\x07isolate\x18\x04 \x01(\tBP\xc2\xf3\x18L\n\x07isolate\x12\x07Isolate2/L1 Dominette 01449 registration number 421906802\x07Pmale09R\x07isolate\x12(\n\x03sex\x18\x05 \x01(\tB\x16\xc2\xf3\x18\x12\n\x03sex\x12\x03Sex2\x06\x66\x65maleR\x03sex\x12\x32\n\x06strain\x18\x06 \x01(\tB\x1a\xc2\xf3\x18\x16\n\x06strain\x12\x06Strain2\x04SE11R\x06strain\"\x97\x02\n\x05Range\x12(\n\x05\x62\x65gin\x18\x01 \x01(\x04\x42\x12\xc2\xf3\x18\x0e\n\x05start\x12\x05StartR\x05\x62\x65gin\x12\"\n\x03\x65nd\x18\x02 \x01(\x04\x42\x10\xc2\xf3\x18\x0c\n\x04stop\x12\x04StopR\x03\x65nd\x12g\n\x0borientation\x18\x03 \x01(\x0e\x32%.ncbi.datasets.v2.reports.OrientationB\x1e\xc2\xf3\x18\x1a\n\x0borientation\x12\x0bOrientationR\x0borientation\x12(\n\x05order\x18\x04 \x01(\rB\x12\xc2\xf3\x18\x0e\n\x05order\x12\x05OrderR\x05order\x12-\n\x12ribosomal_slippage\x18\x05 \x01(\x05R\x11ribosomalSlippage\"\xa4\x01\n\x0bSeqRangeSet\x12P\n\x11\x61\x63\x63\x65ssion_version\x18\x01 \x01(\tB#\xc2\xf3\x18\x1f\n\taccession\x12\x12Sequence AccessionR\x10\x61\x63\x63\x65ssionVersion\x12\x43\n\x05range\x18\x02 \x03(\x0b\x32\x1f.ncbi.datasets.v2.reports.RangeB\x0c\xc2\xf3\x18\x08\n\x06range-R\x05range\"\x98\x03\n\nBioProject\x12\x44\n\taccession\x18\x01 \x01(\tB&\xc2\xf3\x18\"\n\taccession\x12\tAccession2\nPRJEB35387R\taccession\x12h\n\x05title\x18\x02 \x01(\tBR\xc2\xf3\x18N\n\x05title\x12\x05Title2>Sciurus carolinensis (grey squirrel) genome assembly, mSciCar1R\x05title\x12U\n\x10parent_accession\x18\x03 \x01(\tB*\x18\x01\xc2\xf3\x18$\n\x10parent-accession\x12\x10Parent AccessionR\x0fparentAccession\x12\x82\x01\n\x11parent_accessions\x18\x04 \x03(\tBU\xc2\xf3\x18Q\n\x11parent-accessions\x12\x11Parent Accessions2)[\"PRJNA489243\",\"PRJEB33226\",\"PRJEB40665\"]R\x10parentAccessions\"u\n\x11\x42ioProjectLineage\x12`\n\x0b\x62ioprojects\x18\x01 \x03(\x0b\x32$.ncbi.datasets.v2.reports.BioProjectB\x18\xc2\xf3\x18\x14\n\x08lineage-\x12\x08Lineage R\x0b\x62ioprojects*N\n\rAssemblyLevel\x12\x0e\n\nchromosome\x10\x00\x12\x0c\n\x08scaffold\x10\x01\x12\n\n\x06\x63ontig\x10\x02\x12\x13\n\x0f\x63omplete_genome\x10\x03*e\n\x0e\x41ssemblyStatus\x12\x1b\n\x17\x41SSEMBLY_STATUS_UNKNOWN\x10\x00\x12\x0b\n\x07\x63urrent\x10\x01\x12\x0c\n\x08previous\x10\x02\x12\x0e\n\nsuppressed\x10\x03\x12\x0b\n\x07retired\x10\x04*,\n\x0bOrientation\x12\x08\n\x04none\x10\x00\x12\x08\n\x04plus\x10\x01\x12\t\n\x05minus\x10\x02\x42\x45Z\x18ncbi/datasets/v2/reports\xf8\x01\x01\xc2\xf3\x18$\n\x18\x43ommon Report Structures\x12\x08Organismb\x06proto3')

_ASSEMBLYLEVEL = DESCRIPTOR.enum_types_by_name['AssemblyLevel']
AssemblyLevel = enum_type_wrapper.EnumTypeWrapper(_ASSEMBLYLEVEL)
_ASSEMBLYSTATUS = DESCRIPTOR.enum_types_by_name['AssemblyStatus']
AssemblyStatus = enum_type_wrapper.EnumTypeWrapper(_ASSEMBLYSTATUS)
_ORIENTATION = DESCRIPTOR.enum_types_by_name['Orientation']
Orientation = enum_type_wrapper.EnumTypeWrapper(_ORIENTATION)
chromosome = 0
scaffold = 1
contig = 2
complete_genome = 3
ASSEMBLY_STATUS_UNKNOWN = 0
current = 1
previous = 2
suppressed = 3
retired = 4
none = 0
plus = 1
minus = 2


_ERROR = DESCRIPTOR.message_types_by_name['Error']
_WARNING = DESCRIPTOR.message_types_by_name['Warning']
_WARNING_REPLACEDID = _WARNING.nested_types_by_name['ReplacedId']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_LINEAGEORGANISM = DESCRIPTOR.message_types_by_name['LineageOrganism']
_ORGANISM = DESCRIPTOR.message_types_by_name['Organism']
_INFRASPECIFICNAMES = DESCRIPTOR.message_types_by_name['InfraspecificNames']
_RANGE = DESCRIPTOR.message_types_by_name['Range']
_SEQRANGESET = DESCRIPTOR.message_types_by_name['SeqRangeSet']
_BIOPROJECT = DESCRIPTOR.message_types_by_name['BioProject']
_BIOPROJECTLINEAGE = DESCRIPTOR.message_types_by_name['BioProjectLineage']
_ERROR_ASSEMBLYERRORCODE = _ERROR.enum_types_by_name['AssemblyErrorCode']
_ERROR_GENEERRORCODE = _ERROR.enum_types_by_name['GeneErrorCode']
_ERROR_VIRUSERRORCODE = _ERROR.enum_types_by_name['VirusErrorCode']
_WARNING_GENEWARNINGCODE = _WARNING.enum_types_by_name['GeneWarningCode']
Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Error)
  })
_sym_db.RegisterMessage(Error)

Warning = _reflection.GeneratedProtocolMessageType('Warning', (_message.Message,), {

  'ReplacedId' : _reflection.GeneratedProtocolMessageType('ReplacedId', (_message.Message,), {
    'DESCRIPTOR' : _WARNING_REPLACEDID,
    '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
    # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Warning.ReplacedId)
    })
  ,
  'DESCRIPTOR' : _WARNING,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Warning)
  })
_sym_db.RegisterMessage(Warning)
_sym_db.RegisterMessage(Warning.ReplacedId)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Message)
  })
_sym_db.RegisterMessage(Message)

LineageOrganism = _reflection.GeneratedProtocolMessageType('LineageOrganism', (_message.Message,), {
  'DESCRIPTOR' : _LINEAGEORGANISM,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.LineageOrganism)
  })
_sym_db.RegisterMessage(LineageOrganism)

Organism = _reflection.GeneratedProtocolMessageType('Organism', (_message.Message,), {
  'DESCRIPTOR' : _ORGANISM,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Organism)
  })
_sym_db.RegisterMessage(Organism)

InfraspecificNames = _reflection.GeneratedProtocolMessageType('InfraspecificNames', (_message.Message,), {
  'DESCRIPTOR' : _INFRASPECIFICNAMES,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.InfraspecificNames)
  })
_sym_db.RegisterMessage(InfraspecificNames)

Range = _reflection.GeneratedProtocolMessageType('Range', (_message.Message,), {
  'DESCRIPTOR' : _RANGE,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Range)
  })
_sym_db.RegisterMessage(Range)

SeqRangeSet = _reflection.GeneratedProtocolMessageType('SeqRangeSet', (_message.Message,), {
  'DESCRIPTOR' : _SEQRANGESET,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.SeqRangeSet)
  })
_sym_db.RegisterMessage(SeqRangeSet)

BioProject = _reflection.GeneratedProtocolMessageType('BioProject', (_message.Message,), {
  'DESCRIPTOR' : _BIOPROJECT,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.BioProject)
  })
_sym_db.RegisterMessage(BioProject)

BioProjectLineage = _reflection.GeneratedProtocolMessageType('BioProjectLineage', (_message.Message,), {
  'DESCRIPTOR' : _BIOPROJECTLINEAGE,
  '__module__' : 'ncbi.datasets.v2.reports.common_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.BioProjectLineage)
  })
_sym_db.RegisterMessage(BioProjectLineage)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\030ncbi/datasets/v2/reports\370\001\001\302\363\030$\n\030Common Report Structures\022\010Organism'
  _ERROR.fields_by_name['valid_identifiers']._options = None
  _ERROR.fields_by_name['valid_identifiers']._serialized_options = b'\030\001'
  _LINEAGEORGANISM.fields_by_name['tax_id']._options = None
  _LINEAGEORGANISM.fields_by_name['tax_id']._serialized_options = b'\302\363\030\0072\00511118'
  _LINEAGEORGANISM.fields_by_name['name']._options = None
  _LINEAGEORGANISM.fields_by_name['name']._serialized_options = b'\302\363\030\0172\rCoronaviridae'
  _ORGANISM.fields_by_name['tax_id']._options = None
  _ORGANISM.fields_by_name['tax_id']._serialized_options = b'\302\363\030%\n\006tax-id\022\014Taxonomic ID2\00496062\0072697049'
  _ORGANISM.fields_by_name['sci_name']._options = None
  _ORGANISM.fields_by_name['sci_name']._serialized_options = b'\030\001'
  _ORGANISM.fields_by_name['organism_name']._options = None
  _ORGANISM.fields_by_name['organism_name']._serialized_options = b'\302\363\030K\n\004name\022\004Name2\014Homo sapiens2/Severe acute respiratory syndrome coronavirus 2\312\363\030%\022#The scientific name of the organism\322\363\0306\n\017scientific_name\022#The scientific name of the organism'
  _ORGANISM.fields_by_name['common_name']._options = None
  _ORGANISM.fields_by_name['common_name']._serialized_options = b'\302\363\0308\n\013common-name\022\013Common Name2\005human2\010pangolin2\004MERS2\005SARS2'
  _ORGANISM.fields_by_name['strain']._options = None
  _ORGANISM.fields_by_name['strain']._serialized_options = b'\030\001'
  _ORGANISM.fields_by_name['pangolin_classification']._options = None
  _ORGANISM.fields_by_name['pangolin_classification']._serialized_options = b'\302\363\030,\n\010pangolin\022\027Pangolin Classification2\007B.1.1.7'
  _ORGANISM.fields_by_name['infraspecific_names']._options = None
  _ORGANISM.fields_by_name['infraspecific_names']._serialized_options = b'\302\363\030&\n\016infraspecific-\022\024Infraspecific Names '
  _INFRASPECIFICNAMES.fields_by_name['breed']._options = None
  _INFRASPECIFICNAMES.fields_by_name['breed']._serialized_options = b'\302\363\030\037\n\005breed\022\005Breed2\010Hereford2\005boxer'
  _INFRASPECIFICNAMES.fields_by_name['cultivar']._options = None
  _INFRASPECIFICNAMES.fields_by_name['cultivar']._serialized_options = b'\302\363\030\031\n\010cultivar\022\010Cultivar2\003B73'
  _INFRASPECIFICNAMES.fields_by_name['ecotype']._options = None
  _INFRASPECIFICNAMES.fields_by_name['ecotype']._serialized_options = b'\302\363\030\032\n\007ecotype\022\007Ecotype2\006Alpine'
  _INFRASPECIFICNAMES.fields_by_name['isolate']._options = None
  _INFRASPECIFICNAMES.fields_by_name['isolate']._serialized_options = b'\302\363\030L\n\007isolate\022\007Isolate2/L1 Dominette 01449 registration number 421906802\007Pmale09'
  _INFRASPECIFICNAMES.fields_by_name['sex']._options = None
  _INFRASPECIFICNAMES.fields_by_name['sex']._serialized_options = b'\302\363\030\022\n\003sex\022\003Sex2\006female'
  _INFRASPECIFICNAMES.fields_by_name['strain']._options = None
  _INFRASPECIFICNAMES.fields_by_name['strain']._serialized_options = b'\302\363\030\026\n\006strain\022\006Strain2\004SE11'
  _RANGE.fields_by_name['begin']._options = None
  _RANGE.fields_by_name['begin']._serialized_options = b'\302\363\030\016\n\005start\022\005Start'
  _RANGE.fields_by_name['end']._options = None
  _RANGE.fields_by_name['end']._serialized_options = b'\302\363\030\014\n\004stop\022\004Stop'
  _RANGE.fields_by_name['orientation']._options = None
  _RANGE.fields_by_name['orientation']._serialized_options = b'\302\363\030\032\n\013orientation\022\013Orientation'
  _RANGE.fields_by_name['order']._options = None
  _RANGE.fields_by_name['order']._serialized_options = b'\302\363\030\016\n\005order\022\005Order'
  _SEQRANGESET.fields_by_name['accession_version']._options = None
  _SEQRANGESET.fields_by_name['accession_version']._serialized_options = b'\302\363\030\037\n\taccession\022\022Sequence Accession'
  _SEQRANGESET.fields_by_name['range']._options = None
  _SEQRANGESET.fields_by_name['range']._serialized_options = b'\302\363\030\010\n\006range-'
  _BIOPROJECT.fields_by_name['accession']._options = None
  _BIOPROJECT.fields_by_name['accession']._serialized_options = b'\302\363\030\"\n\taccession\022\tAccession2\nPRJEB35387'
  _BIOPROJECT.fields_by_name['title']._options = None
  _BIOPROJECT.fields_by_name['title']._serialized_options = b'\302\363\030N\n\005title\022\005Title2>Sciurus carolinensis (grey squirrel) genome assembly, mSciCar1'
  _BIOPROJECT.fields_by_name['parent_accession']._options = None
  _BIOPROJECT.fields_by_name['parent_accession']._serialized_options = b'\030\001\302\363\030$\n\020parent-accession\022\020Parent Accession'
  _BIOPROJECT.fields_by_name['parent_accessions']._options = None
  _BIOPROJECT.fields_by_name['parent_accessions']._serialized_options = b'\302\363\030Q\n\021parent-accessions\022\021Parent Accessions2)[\"PRJNA489243\",\"PRJEB33226\",\"PRJEB40665\"]'
  _BIOPROJECTLINEAGE.fields_by_name['bioprojects']._options = None
  _BIOPROJECTLINEAGE.fields_by_name['bioprojects']._serialized_options = b'\302\363\030\024\n\010lineage-\022\010Lineage '
  _ASSEMBLYLEVEL._serialized_start=3817
  _ASSEMBLYLEVEL._serialized_end=3895
  _ASSEMBLYSTATUS._serialized_start=3897
  _ASSEMBLYSTATUS._serialized_end=3998
  _ORIENTATION._serialized_start=4000
  _ORIENTATION._serialized_end=4044
  _ERROR._serialized_start=104
  _ERROR._serialized_end=810
  _ERROR_ASSEMBLYERRORCODE._serialized_start=544
  _ERROR_ASSEMBLYERRORCODE._serialized_end=678
  _ERROR_GENEERRORCODE._serialized_start=680
  _ERROR_GENEERRORCODE._serialized_end=754
  _ERROR_VIRUSERRORCODE._serialized_start=756
  _ERROR_VIRUSERRORCODE._serialized_end=802
  _WARNING._serialized_start=813
  _WARNING._serialized_end=1428
  _WARNING_REPLACEDID._serialized_start=1107
  _WARNING_REPLACEDID._serialized_end=1177
  _WARNING_GENEWARNINGCODE._serialized_start=1180
  _WARNING_GENEWARNINGCODE._serialized_end=1420
  _MESSAGE._serialized_start=1431
  _MESSAGE._serialized_end=1571
  _LINEAGEORGANISM._serialized_start=1573
  _LINEAGEORGANISM._serialized_end=1667
  _ORGANISM._serialized_start=1670
  _ORGANISM._serialized_end=2435
  _INFRASPECIFICNAMES._serialized_start=2438
  _INFRASPECIFICNAMES._serialized_end=2836
  _RANGE._serialized_start=2839
  _RANGE._serialized_end=3118
  _SEQRANGESET._serialized_start=3121
  _SEQRANGESET._serialized_end=3285
  _BIOPROJECT._serialized_start=3288
  _BIOPROJECT._serialized_end=3696
  _BIOPROJECTLINEAGE._serialized_start=3698
  _BIOPROJECTLINEAGE._serialized_end=3815
# @@protoc_insertion_point(module_scope)
