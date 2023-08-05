# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v2/reports/microbigge.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ncbi.datasets.v2.reports import common_pb2 as ncbi_dot_datasets_dot_v2_dot_reports_dot_common__pb2
from ncbi.datasets.options import report_pb2 as ncbi_dot_datasets_dot_options_dot_report__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)ncbi/datasets/v2/reports/microbigge.proto\x12\x18ncbi.datasets.v2.reports\x1a%ncbi/datasets/v2/reports/common.proto\x1a\"ncbi/datasets/options/report.proto\"\x86\x03\n\x07\x45lement\x12G\n\x06symbol\x18\x01 \x01(\tB/\xc2\xf3\x18+\n\x0b\x65lem-symbol\x12\x0e\x45lement symbol2\x06vanS-A2\x04\x63opBR\x06symbol\x12\x9a\x01\n\x04name\x18\x02 \x01(\tB\x85\x01\xc2\xf3\x18\x80\x01\n\telem-name\x12\x0c\x45lement name25VanA-type vancomycin resistance histidine kinase VanS2.copper/silver-translocating P-type ATPase CopBR\x04name\x12\x39\n\x06length\x18\x03 \x01(\x05\x42!\xc2\xf3\x18\x1d\n\x0b\x65lem-length\x12\x0e\x45lement lengthR\x06length\x12Z\n\x10reference_length\x18\x04 \x01(\x05\x42/\xc2\xf3\x18+\n\x0f\x65lem-ref-length\x12\x18\x45lement reference lengthR\x0freferenceLength\"\xef\x03\n\x10\x43losestReference\x12V\n\taccession\x18\x01 \x01(\tB8\xc2\xf3\x18\x34\n\x15\x63losest-ref-accession\x12\x1b\x43losest reference accessionR\taccession\x12\x42\n\x04name\x18\x02 \x01(\tB.\xc2\xf3\x18*\n\x10\x63losest-ref-name\x12\x16\x43losest reference nameR\x04name\x12m\n\x10percent_coverage\x18\x03 \x01(\x02\x42\x42\xc2\xf3\x18>\n\x18\x63losest-ref-pct-coverage\x12\"Closest reference percent coverageR\x0fpercentCoverage\x12l\n\x11percent_identical\x18\x04 \x01(\x02\x42?\xc2\xf3\x18;\n\x15\x63losest-ref-pct-ident\x12\"Closest reference percent identityR\x10percentIdentical\x12\x62\n\x0c\x61lign_length\x18\x05 \x01(\x05\x42?\xc2\xf3\x18;\n\x15\x63losest-ref-align-len\x12\"Closest reference alignment lengthR\x0b\x61lignLength\"\xc1\x01\n\x08Taxonomy\x12L\n\x05group\x18\x01 \x01(\tB6\xc2\xf3\x18\x32\n\ttax-group\x12\x0fTaxonomic group2\x14\x45nterococcus faeciumR\x05group\x12g\n\x0fscientific_name\x18\x02 \x01(\tB>\xc2\xf3\x18:\n\x08tax-name\x12\x0eTaxonomic name2\x1e\x45nterococcus faecium EnGen0172R\x0escientificName\"\xcb\x04\n\tBiosample\x12}\n\x11geographic_origin\x18\x01 \x01(\tBP\xc2\xf3\x18L\n\x14\x62iosample-geo-origin\x12\x1b\x42ioSample geographic origin2\x07\x44\x65nmark2\x0enot determinedR\x10geographicOrigin\x12@\n\x06source\x18\x02 \x01(\tB(\xc2\xf3\x18$\n\x10\x62iosample-source\x12\x10\x42ioSample sourceR\x06source\x12W\n\x04type\x18\x03 \x01(\tBC\xc2\xf3\x18?\n\x0e\x62iosample-type\x12\x0e\x42ioSample type2\x08\x63linical2\x13\x65nvironmental/otherR\x04type\x12Z\n\taccession\x18\x04 \x01(\tB<\xc2\xf3\x18\x38\n\x13\x62iosample-accession\x12\x13\x42ioSample accession2\x0cSAMN00808999R\taccession\x12\x63\n\x08\x61ssembly\x18\x05 \x01(\tBG\xc2\xf3\x18\x43\n\x12\x62iosample-assembly\x12\x1c\x42ioSample assembly accession2\x0fGCA_000395725.1R\x08\x61ssembly\x12\x63\n\x0f\x63ollection_date\x18\x06 \x01(\tB:\xc2\xf3\x18\x36\n\x19\x62iosample-collection-date\x12\x19\x42ioSample collection dateR\x0e\x63ollectionDate\"\xad\x02\n\x16ReadToAssemblyCoverage\x12Y\n\x06\x63ontig\x18\x01 \x01(\rBA\xc2\xf3\x18=\n\x19read-assm-coverage-contig\x12 Read-to-Assembly-Coverage contigR\x06\x63ontig\x12\x61\n\x08\x61ssembly\x18\x02 \x01(\rBE\xc2\xf3\x18\x41\n\x1bread-assm-coverage-assembly\x12\"Read-to-Assembly-Coverage assemblyR\x08\x61ssembly\x12U\n\x05ratio\x18\x03 \x01(\x02\x42?\xc2\xf3\x18;\n\x18read-assm-coverage-ratio\x12\x1fRead-to-Assembly-Coverage ratioR\x05ratio\"\xfe\x01\n\rAmrFinderPlus\x12L\n\x07version\x18\x01 \x01(\tB2\xc2\xf3\x18.\n\x15\x61mrfinderplus-version\x12\x15\x41MRFinderPlus versionR\x07version\x12@\n\x04type\x18\x02 \x01(\tB,\xc2\xf3\x18(\n\x12\x61mrfinderplus-type\x12\x12\x41MRFinderPlus typeR\x04type\x12]\n\ndb_version\x18\x03 \x01(\tB>\xc2\xf3\x18:\n\x18\x61mrfinderplus-db-version\x12\x1e\x41MRFinderPlus database versionR\tdbVersion\"\xec\x08\n\x10MicroBiggeReport\x12G\n\ntarget_acc\x18\x01 \x01(\tB(\xc2\xf3\x18$\n\x10target-accession\x12\x10Target accessionR\ttargetAcc\x12;\n\x07\x65lement\x18\x02 \x01(\x0b\x32!.ncbi.datasets.v2.reports.ElementR\x07\x65lement\x12\x41\n\x08location\x18\x03 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetR\x08location\x12\x31\n\x04type\x18\x04 \x01(\tB\x1d\xc2\xf3\x18\x19\n\x04type\x12\x04Type2\x03\x41MR2\x06STRESSR\x04type\x12<\n\x07subtype\x18\x05 \x01(\tB\"\xc2\xf3\x18\x1e\n\x07subtype\x12\x07Subtype2\x03\x41MR2\x05METALR\x07subtype\x12\x45\n\x05\x63lass\x18\x06 \x01(\tB/\xc2\xf3\x18+\n\x05\x63lass\x12\x05\x43lass2\x0cGLYCOPEPTIDE2\rCOPPER/SILVERR\x05\x63lass\x12O\n\x08subclass\x18\x07 \x01(\tB3\xc2\xf3\x18/\n\x08subclass\x12\x08Subclass2\nVANCOMYCIN2\rCOPPER/SILVERR\x08subclass\x12\x43\n\namr_method\x18\x08 \x01(\tB$\xc2\xf3\x18 \n\namr-method\x12\nAMR method2\x06\x45XACTPR\tamrMethod\x12/\n\x07is_plus\x18\t \x01(\x08\x42\x16\xc2\xf3\x18\x12\n\x07is-plus\x12\x07Is plusR\x06isPlus\x12}\n%closest_reference_sequence_comparison\x18\n \x01(\x0b\x32*.ncbi.datasets.v2.reports.ClosestReferenceR\"closestReferenceSequenceComparison\x12>\n\x08taxonomy\x18\x0b \x01(\x0b\x32\".ncbi.datasets.v2.reports.TaxonomyR\x08taxonomy\x12\x41\n\tbiosample\x18\x0c \x01(\x0b\x32#.ncbi.datasets.v2.reports.BiosampleR\tbiosample\x12k\n\x19read_to_assembly_coverage\x18\r \x01(\x0b\x32\x30.ncbi.datasets.v2.reports.ReadToAssemblyCoverageR\x16readToAssemblyCoverage\x12O\n\x0f\x61mr_finder_plus\x18\x0e \x01(\x0b\x32\'.ncbi.datasets.v2.reports.AmrFinderPlusR\ramrFinderPlus\x12&\n\x0fgenes_on_contig\x18\x0f \x03(\tR\rgenesOnContig\x12(\n\x10genes_on_isolate\x18\x10 \x03(\tR\x0egenesOnIsolateB\xea\nZ\x18ncbi/datasets/v2/reports\xf8\x01\x01\xc2\xf3\x18\xc8\n\n\x17MicroBiGG-E Data Report\x12\x10MicroBiggeReport\x1aK<p>The downloaded MicroBIGG-E package contains a MicroBIGG-E data report in\x1a:<a href=\"https://jsonlines.readthedocs.io/\">JSON lines</a>\x1ajformat at the following location in the file: <br><br><em>ncbi_dataset/data/data_report.jsonl</em><br><br>\x1auEach line of the  MicroBIGG-E data report file is a hierarchical <a href=\"https://www.json.org/json-en.html\">JSON</a>\x1awobject that represents a single MicroBIGG-E record. The schema of the MicroBIGG-E record is defined in the tables below\x1ajwhere each row describes a single field in the report or a sub-structure, which is a collection of fields.\x1aGThe outermost structure of the report is <em>MicroBiggeReport</em>.</p>\x1aQ<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\x1a\x66<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s\x1a\x37<nobr><code>--fields</code></nobr> option. Refer to the\x1ap<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how\x1a\x63you can use this tool to transform MicroBIGG-E data reports from JSON Lines to tabular formats.</p>\"\x0fLineageOrganism\"\x08Organism*\x9a\x01{{< readfile-code-block lang=\"json\" file=\"/docs_samples/datasets-cli/microbigge-data-report.cli.output\" begin=\"START data-report\" end=\"END data-report\">}}b\x06proto3')



_ELEMENT = DESCRIPTOR.message_types_by_name['Element']
_CLOSESTREFERENCE = DESCRIPTOR.message_types_by_name['ClosestReference']
_TAXONOMY = DESCRIPTOR.message_types_by_name['Taxonomy']
_BIOSAMPLE = DESCRIPTOR.message_types_by_name['Biosample']
_READTOASSEMBLYCOVERAGE = DESCRIPTOR.message_types_by_name['ReadToAssemblyCoverage']
_AMRFINDERPLUS = DESCRIPTOR.message_types_by_name['AmrFinderPlus']
_MICROBIGGEREPORT = DESCRIPTOR.message_types_by_name['MicroBiggeReport']
Element = _reflection.GeneratedProtocolMessageType('Element', (_message.Message,), {
  'DESCRIPTOR' : _ELEMENT,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Element)
  })
_sym_db.RegisterMessage(Element)

ClosestReference = _reflection.GeneratedProtocolMessageType('ClosestReference', (_message.Message,), {
  'DESCRIPTOR' : _CLOSESTREFERENCE,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.ClosestReference)
  })
_sym_db.RegisterMessage(ClosestReference)

Taxonomy = _reflection.GeneratedProtocolMessageType('Taxonomy', (_message.Message,), {
  'DESCRIPTOR' : _TAXONOMY,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Taxonomy)
  })
_sym_db.RegisterMessage(Taxonomy)

Biosample = _reflection.GeneratedProtocolMessageType('Biosample', (_message.Message,), {
  'DESCRIPTOR' : _BIOSAMPLE,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Biosample)
  })
_sym_db.RegisterMessage(Biosample)

ReadToAssemblyCoverage = _reflection.GeneratedProtocolMessageType('ReadToAssemblyCoverage', (_message.Message,), {
  'DESCRIPTOR' : _READTOASSEMBLYCOVERAGE,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.ReadToAssemblyCoverage)
  })
_sym_db.RegisterMessage(ReadToAssemblyCoverage)

AmrFinderPlus = _reflection.GeneratedProtocolMessageType('AmrFinderPlus', (_message.Message,), {
  'DESCRIPTOR' : _AMRFINDERPLUS,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.AmrFinderPlus)
  })
_sym_db.RegisterMessage(AmrFinderPlus)

MicroBiggeReport = _reflection.GeneratedProtocolMessageType('MicroBiggeReport', (_message.Message,), {
  'DESCRIPTOR' : _MICROBIGGEREPORT,
  '__module__' : 'ncbi.datasets.v2.reports.microbigge_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.MicroBiggeReport)
  })
_sym_db.RegisterMessage(MicroBiggeReport)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\030ncbi/datasets/v2/reports\370\001\001\302\363\030\310\n\n\027MicroBiGG-E Data Report\022\020MicroBiggeReport\032K<p>The downloaded MicroBIGG-E package contains a MicroBIGG-E data report in\032:<a href=\"https://jsonlines.readthedocs.io/\">JSON lines</a>\032jformat at the following location in the file: <br><br><em>ncbi_dataset/data/data_report.jsonl</em><br><br>\032uEach line of the  MicroBIGG-E data report file is a hierarchical <a href=\"https://www.json.org/json-en.html\">JSON</a>\032wobject that represents a single MicroBIGG-E record. The schema of the MicroBIGG-E record is defined in the tables below\032jwhere each row describes a single field in the report or a sub-structure, which is a collection of fields.\032GThe outermost structure of the report is <em>MicroBiggeReport</em>.</p>\032Q<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\032f<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s\0327<nobr><code>--fields</code></nobr> option. Refer to the\032p<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how\032cyou can use this tool to transform MicroBIGG-E data reports from JSON Lines to tabular formats.</p>\"\017LineageOrganism\"\010Organism*\232\001{{< readfile-code-block lang=\"json\" file=\"/docs_samples/datasets-cli/microbigge-data-report.cli.output\" begin=\"START data-report\" end=\"END data-report\">}}'
  _ELEMENT.fields_by_name['symbol']._options = None
  _ELEMENT.fields_by_name['symbol']._serialized_options = b'\302\363\030+\n\013elem-symbol\022\016Element symbol2\006vanS-A2\004copB'
  _ELEMENT.fields_by_name['name']._options = None
  _ELEMENT.fields_by_name['name']._serialized_options = b'\302\363\030\200\001\n\telem-name\022\014Element name25VanA-type vancomycin resistance histidine kinase VanS2.copper/silver-translocating P-type ATPase CopB'
  _ELEMENT.fields_by_name['length']._options = None
  _ELEMENT.fields_by_name['length']._serialized_options = b'\302\363\030\035\n\013elem-length\022\016Element length'
  _ELEMENT.fields_by_name['reference_length']._options = None
  _ELEMENT.fields_by_name['reference_length']._serialized_options = b'\302\363\030+\n\017elem-ref-length\022\030Element reference length'
  _CLOSESTREFERENCE.fields_by_name['accession']._options = None
  _CLOSESTREFERENCE.fields_by_name['accession']._serialized_options = b'\302\363\0304\n\025closest-ref-accession\022\033Closest reference accession'
  _CLOSESTREFERENCE.fields_by_name['name']._options = None
  _CLOSESTREFERENCE.fields_by_name['name']._serialized_options = b'\302\363\030*\n\020closest-ref-name\022\026Closest reference name'
  _CLOSESTREFERENCE.fields_by_name['percent_coverage']._options = None
  _CLOSESTREFERENCE.fields_by_name['percent_coverage']._serialized_options = b'\302\363\030>\n\030closest-ref-pct-coverage\022\"Closest reference percent coverage'
  _CLOSESTREFERENCE.fields_by_name['percent_identical']._options = None
  _CLOSESTREFERENCE.fields_by_name['percent_identical']._serialized_options = b'\302\363\030;\n\025closest-ref-pct-ident\022\"Closest reference percent identity'
  _CLOSESTREFERENCE.fields_by_name['align_length']._options = None
  _CLOSESTREFERENCE.fields_by_name['align_length']._serialized_options = b'\302\363\030;\n\025closest-ref-align-len\022\"Closest reference alignment length'
  _TAXONOMY.fields_by_name['group']._options = None
  _TAXONOMY.fields_by_name['group']._serialized_options = b'\302\363\0302\n\ttax-group\022\017Taxonomic group2\024Enterococcus faecium'
  _TAXONOMY.fields_by_name['scientific_name']._options = None
  _TAXONOMY.fields_by_name['scientific_name']._serialized_options = b'\302\363\030:\n\010tax-name\022\016Taxonomic name2\036Enterococcus faecium EnGen0172'
  _BIOSAMPLE.fields_by_name['geographic_origin']._options = None
  _BIOSAMPLE.fields_by_name['geographic_origin']._serialized_options = b'\302\363\030L\n\024biosample-geo-origin\022\033BioSample geographic origin2\007Denmark2\016not determined'
  _BIOSAMPLE.fields_by_name['source']._options = None
  _BIOSAMPLE.fields_by_name['source']._serialized_options = b'\302\363\030$\n\020biosample-source\022\020BioSample source'
  _BIOSAMPLE.fields_by_name['type']._options = None
  _BIOSAMPLE.fields_by_name['type']._serialized_options = b'\302\363\030?\n\016biosample-type\022\016BioSample type2\010clinical2\023environmental/other'
  _BIOSAMPLE.fields_by_name['accession']._options = None
  _BIOSAMPLE.fields_by_name['accession']._serialized_options = b'\302\363\0308\n\023biosample-accession\022\023BioSample accession2\014SAMN00808999'
  _BIOSAMPLE.fields_by_name['assembly']._options = None
  _BIOSAMPLE.fields_by_name['assembly']._serialized_options = b'\302\363\030C\n\022biosample-assembly\022\034BioSample assembly accession2\017GCA_000395725.1'
  _BIOSAMPLE.fields_by_name['collection_date']._options = None
  _BIOSAMPLE.fields_by_name['collection_date']._serialized_options = b'\302\363\0306\n\031biosample-collection-date\022\031BioSample collection date'
  _READTOASSEMBLYCOVERAGE.fields_by_name['contig']._options = None
  _READTOASSEMBLYCOVERAGE.fields_by_name['contig']._serialized_options = b'\302\363\030=\n\031read-assm-coverage-contig\022 Read-to-Assembly-Coverage contig'
  _READTOASSEMBLYCOVERAGE.fields_by_name['assembly']._options = None
  _READTOASSEMBLYCOVERAGE.fields_by_name['assembly']._serialized_options = b'\302\363\030A\n\033read-assm-coverage-assembly\022\"Read-to-Assembly-Coverage assembly'
  _READTOASSEMBLYCOVERAGE.fields_by_name['ratio']._options = None
  _READTOASSEMBLYCOVERAGE.fields_by_name['ratio']._serialized_options = b'\302\363\030;\n\030read-assm-coverage-ratio\022\037Read-to-Assembly-Coverage ratio'
  _AMRFINDERPLUS.fields_by_name['version']._options = None
  _AMRFINDERPLUS.fields_by_name['version']._serialized_options = b'\302\363\030.\n\025amrfinderplus-version\022\025AMRFinderPlus version'
  _AMRFINDERPLUS.fields_by_name['type']._options = None
  _AMRFINDERPLUS.fields_by_name['type']._serialized_options = b'\302\363\030(\n\022amrfinderplus-type\022\022AMRFinderPlus type'
  _AMRFINDERPLUS.fields_by_name['db_version']._options = None
  _AMRFINDERPLUS.fields_by_name['db_version']._serialized_options = b'\302\363\030:\n\030amrfinderplus-db-version\022\036AMRFinderPlus database version'
  _MICROBIGGEREPORT.fields_by_name['target_acc']._options = None
  _MICROBIGGEREPORT.fields_by_name['target_acc']._serialized_options = b'\302\363\030$\n\020target-accession\022\020Target accession'
  _MICROBIGGEREPORT.fields_by_name['type']._options = None
  _MICROBIGGEREPORT.fields_by_name['type']._serialized_options = b'\302\363\030\031\n\004type\022\004Type2\003AMR2\006STRESS'
  _MICROBIGGEREPORT.fields_by_name['subtype']._options = None
  _MICROBIGGEREPORT.fields_by_name['subtype']._serialized_options = b'\302\363\030\036\n\007subtype\022\007Subtype2\003AMR2\005METAL'
  _MICROBIGGEREPORT.fields_by_name['class']._options = None
  _MICROBIGGEREPORT.fields_by_name['class']._serialized_options = b'\302\363\030+\n\005class\022\005Class2\014GLYCOPEPTIDE2\rCOPPER/SILVER'
  _MICROBIGGEREPORT.fields_by_name['subclass']._options = None
  _MICROBIGGEREPORT.fields_by_name['subclass']._serialized_options = b'\302\363\030/\n\010subclass\022\010Subclass2\nVANCOMYCIN2\rCOPPER/SILVER'
  _MICROBIGGEREPORT.fields_by_name['amr_method']._options = None
  _MICROBIGGEREPORT.fields_by_name['amr_method']._serialized_options = b'\302\363\030 \n\namr-method\022\nAMR method2\006EXACTP'
  _MICROBIGGEREPORT.fields_by_name['is_plus']._options = None
  _MICROBIGGEREPORT.fields_by_name['is_plus']._serialized_options = b'\302\363\030\022\n\007is-plus\022\007Is plus'
  _ELEMENT._serialized_start=147
  _ELEMENT._serialized_end=537
  _CLOSESTREFERENCE._serialized_start=540
  _CLOSESTREFERENCE._serialized_end=1035
  _TAXONOMY._serialized_start=1038
  _TAXONOMY._serialized_end=1231
  _BIOSAMPLE._serialized_start=1234
  _BIOSAMPLE._serialized_end=1821
  _READTOASSEMBLYCOVERAGE._serialized_start=1824
  _READTOASSEMBLYCOVERAGE._serialized_end=2125
  _AMRFINDERPLUS._serialized_start=2128
  _AMRFINDERPLUS._serialized_end=2382
  _MICROBIGGEREPORT._serialized_start=2385
  _MICROBIGGEREPORT._serialized_end=3517
# @@protoc_insertion_point(module_scope)
