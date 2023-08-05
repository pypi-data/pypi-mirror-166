# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v2/reports/prokaryote_gene_location.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7ncbi/datasets/v2/reports/prokaryote_gene_location.proto\x12\x18ncbi.datasets.v2.reports\x1a%ncbi/datasets/v2/reports/common.proto\x1a\"ncbi/datasets/options/report.proto\"\xe4\x01\n\x14SeqRangeWithAssembly\x12l\n\x12\x61ssembly_accession\x18\x01 \x01(\tB=\xc2\xf3\x18\x39\n\x12\x61ssembly-accession\x12\x12\x41ssembly Accession2\x0fGCF_000010385.1R\x11\x61ssemblyAccession\x12^\n\x0esequence_range\x18\x02 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB\x10\xc2\xf3\x18\x0c\n\nseq-range-R\rsequenceRange\"\xc2\x06\n\x16ProkaryoteGeneLocation\x12\x84\x01\n\x11protein_accession\x18\x01 \x01(\tBW\xc2\xf3\x18\x36\n\x11protein-accession\x12\x11Protein Accession2\x0eWP_000443665.1\xca\xf3\x18\x19\x08\x06\x12\x15The protein accessionR\x10proteinAccession\x12\xa0\x01\n\x17refseq_genomic_location\x18\x02 \x01(\x0b\x32..ncbi.datasets.v2.reports.SeqRangeWithAssemblyB8\xc2\xf3\x18\x34\n\x18refseq-genomic-location-\x12\x18RefSeq Genomic Location R\x15refseqGenomicLocation\x12\xa4\x01\n\x18genbank_genomic_location\x18\x03 \x01(\x0b\x32..ncbi.datasets.v2.reports.SeqRangeWithAssemblyB:\xc2\xf3\x18\x36\n\x19genbank-genomic-location-\x12\x19GenBank Genomic Location R\x16genbankGenomicLocation\x12Z\n\x08organism\x18\x04 \x01(\x0b\x32\".ncbi.datasets.v2.reports.OrganismB\x1a\xc2\xf3\x18\x16\n\torganism-\x12\tOrganism R\x08organism\x12\x83\x01\n\x0c\x63ompleteness\x18\x05 \x01(\x0e\x32=.ncbi.datasets.v2.reports.ProkaryoteGeneLocation.CompletenessB \xc2\xf3\x18\x1c\n\x0c\x63ompleteness\x12\x0c\x43ompletenessR\x0c\x63ompleteness\x12J\n\x0f\x63hromosome_name\x18\x06 \x01(\tB!\xc2\xf3\x18\x1d\n\x0f\x63hromosome_name\x12\nChromosomeR\x0e\x63hromosomeName\")\n\x0c\x43ompleteness\x12\x0c\n\x08\x63omplete\x10\x00\x12\x0b\n\x07partial\x10\x01\"\xce\x01\n\x1dProkaryoteGeneLocationDefline\x12U\n\rgene_location\x18\x01 \x01(\x0b\x32\x30.ncbi.datasets.v2.reports.ProkaryoteGeneLocationR\x0cgeneLocation\x12)\n\x04name\x18\x02 \x01(\tB\x15\xca\xf3\x18\x11\x08\x08\x12\rThe gene nameR\x04name\x12+\n\x04gene\x18\x03 \x01(\tB\x17\xca\xf3\x18\x13\x08\x05\x12\x0fThe gene symbolR\x04geneB\x96\x0bZ\x18ncbi/datasets/v2/reports\xf8\x01\x01\xc2\xf3\x18\xf4\n\n\x1fProkaryote Gene Location Report\x12\x16ProkaryoteGeneLocation\x1aW<p>The downloaded prokaryote package contains a prokaryote gene location data report in\x1a:<a href=\"https://jsonlines.readthedocs.io/\">JSON Lines</a>\x1aVformat in the file:<br><br><em> ncbi_dataset/data/annotation_report.jsonl</em><br><br>\x1aLEach line of the prokaryote gene location data report file is a hierarchical\x1a\x34<a href=\"https://www.json.org/json-en.html\">JSON</a>\x1a]object that represents a single prokaryote gene location record. The schema of the prokaryote\x1a^gene location record is defined in the tables below where each row describes a single field in\x1a?the report or a sub-structure, which is a collection of fields.\x1aMThe outermost structure of the report is <em>ProkaryoteGeneLocation</em>.</p>\x1aQ<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\x1a\x66<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s\x1a\x37<nobr><code>--fields</code></nobr> option. Refer to the\x1at<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how you\x1alcan use this tool to transform prokaryote gene location data reports from JSON Lines to tabular formats.</p>*\xa0\x01{{< readfile-code-block lang=\"json\" file=\"/docs_samples/datasets-cli/prok-gene-report.cli.output\" begin=\"START annotation-report\" end=\"END annotation-report\">}}b\x06proto3')



_SEQRANGEWITHASSEMBLY = DESCRIPTOR.message_types_by_name['SeqRangeWithAssembly']
_PROKARYOTEGENELOCATION = DESCRIPTOR.message_types_by_name['ProkaryoteGeneLocation']
_PROKARYOTEGENELOCATIONDEFLINE = DESCRIPTOR.message_types_by_name['ProkaryoteGeneLocationDefline']
_PROKARYOTEGENELOCATION_COMPLETENESS = _PROKARYOTEGENELOCATION.enum_types_by_name['Completeness']
SeqRangeWithAssembly = _reflection.GeneratedProtocolMessageType('SeqRangeWithAssembly', (_message.Message,), {
  'DESCRIPTOR' : _SEQRANGEWITHASSEMBLY,
  '__module__' : 'ncbi.datasets.v2.reports.prokaryote_gene_location_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.SeqRangeWithAssembly)
  })
_sym_db.RegisterMessage(SeqRangeWithAssembly)

ProkaryoteGeneLocation = _reflection.GeneratedProtocolMessageType('ProkaryoteGeneLocation', (_message.Message,), {
  'DESCRIPTOR' : _PROKARYOTEGENELOCATION,
  '__module__' : 'ncbi.datasets.v2.reports.prokaryote_gene_location_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.ProkaryoteGeneLocation)
  })
_sym_db.RegisterMessage(ProkaryoteGeneLocation)

ProkaryoteGeneLocationDefline = _reflection.GeneratedProtocolMessageType('ProkaryoteGeneLocationDefline', (_message.Message,), {
  'DESCRIPTOR' : _PROKARYOTEGENELOCATIONDEFLINE,
  '__module__' : 'ncbi.datasets.v2.reports.prokaryote_gene_location_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.ProkaryoteGeneLocationDefline)
  })
_sym_db.RegisterMessage(ProkaryoteGeneLocationDefline)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\030ncbi/datasets/v2/reports\370\001\001\302\363\030\364\n\n\037Prokaryote Gene Location Report\022\026ProkaryoteGeneLocation\032W<p>The downloaded prokaryote package contains a prokaryote gene location data report in\032:<a href=\"https://jsonlines.readthedocs.io/\">JSON Lines</a>\032Vformat in the file:<br><br><em> ncbi_dataset/data/annotation_report.jsonl</em><br><br>\032LEach line of the prokaryote gene location data report file is a hierarchical\0324<a href=\"https://www.json.org/json-en.html\">JSON</a>\032]object that represents a single prokaryote gene location record. The schema of the prokaryote\032^gene location record is defined in the tables below where each row describes a single field in\032?the report or a sub-structure, which is a collection of fields.\032MThe outermost structure of the report is <em>ProkaryoteGeneLocation</em>.</p>\032Q<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\032f<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s\0327<nobr><code>--fields</code></nobr> option. Refer to the\032t<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how you\032lcan use this tool to transform prokaryote gene location data reports from JSON Lines to tabular formats.</p>*\240\001{{< readfile-code-block lang=\"json\" file=\"/docs_samples/datasets-cli/prok-gene-report.cli.output\" begin=\"START annotation-report\" end=\"END annotation-report\">}}'
  _SEQRANGEWITHASSEMBLY.fields_by_name['assembly_accession']._options = None
  _SEQRANGEWITHASSEMBLY.fields_by_name['assembly_accession']._serialized_options = b'\302\363\0309\n\022assembly-accession\022\022Assembly Accession2\017GCF_000010385.1'
  _SEQRANGEWITHASSEMBLY.fields_by_name['sequence_range']._options = None
  _SEQRANGEWITHASSEMBLY.fields_by_name['sequence_range']._serialized_options = b'\302\363\030\014\n\nseq-range-'
  _PROKARYOTEGENELOCATION.fields_by_name['protein_accession']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['protein_accession']._serialized_options = b'\302\363\0306\n\021protein-accession\022\021Protein Accession2\016WP_000443665.1\312\363\030\031\010\006\022\025The protein accession'
  _PROKARYOTEGENELOCATION.fields_by_name['refseq_genomic_location']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['refseq_genomic_location']._serialized_options = b'\302\363\0304\n\030refseq-genomic-location-\022\030RefSeq Genomic Location '
  _PROKARYOTEGENELOCATION.fields_by_name['genbank_genomic_location']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['genbank_genomic_location']._serialized_options = b'\302\363\0306\n\031genbank-genomic-location-\022\031GenBank Genomic Location '
  _PROKARYOTEGENELOCATION.fields_by_name['organism']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['organism']._serialized_options = b'\302\363\030\026\n\torganism-\022\tOrganism '
  _PROKARYOTEGENELOCATION.fields_by_name['completeness']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['completeness']._serialized_options = b'\302\363\030\034\n\014completeness\022\014Completeness'
  _PROKARYOTEGENELOCATION.fields_by_name['chromosome_name']._options = None
  _PROKARYOTEGENELOCATION.fields_by_name['chromosome_name']._serialized_options = b'\302\363\030\035\n\017chromosome_name\022\nChromosome'
  _PROKARYOTEGENELOCATIONDEFLINE.fields_by_name['name']._options = None
  _PROKARYOTEGENELOCATIONDEFLINE.fields_by_name['name']._serialized_options = b'\312\363\030\021\010\010\022\rThe gene name'
  _PROKARYOTEGENELOCATIONDEFLINE.fields_by_name['gene']._options = None
  _PROKARYOTEGENELOCATIONDEFLINE.fields_by_name['gene']._serialized_options = b'\312\363\030\023\010\005\022\017The gene symbol'
  _SEQRANGEWITHASSEMBLY._serialized_start=161
  _SEQRANGEWITHASSEMBLY._serialized_end=389
  _PROKARYOTEGENELOCATION._serialized_start=392
  _PROKARYOTEGENELOCATION._serialized_end=1226
  _PROKARYOTEGENELOCATION_COMPLETENESS._serialized_start=1185
  _PROKARYOTEGENELOCATION_COMPLETENESS._serialized_end=1226
  _PROKARYOTEGENELOCATIONDEFLINE._serialized_start=1229
  _PROKARYOTEGENELOCATIONDEFLINE._serialized_end=1435
# @@protoc_insertion_point(module_scope)
