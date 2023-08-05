# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ncbi/datasets/v2/reports/gene.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#ncbi/datasets/v2/reports/gene.proto\x12\x18ncbi.datasets.v2.reports\x1a%ncbi/datasets/v2/reports/common.proto\x1a\"ncbi/datasets/options/report.proto\"\xb2\x02\n\x0fGeneReportMatch\x12>\n\x04gene\x18\x01 \x01(\x0b\x32(.ncbi.datasets.v2.reports.GeneDescriptorH\x00R\x04gene\x12G\n\x07product\x18\x05 \x01(\x0b\x32+.ncbi.datasets.v2.reports.ProductDescriptorH\x00R\x07product\x12\x14\n\x05query\x18\x02 \x03(\tR\x05query\x12=\n\x08warnings\x18\x03 \x03(\x0b\x32!.ncbi.datasets.v2.reports.WarningR\x08warnings\x12\x37\n\x06\x65rrors\x18\x04 \x03(\x0b\x32\x1f.ncbi.datasets.v2.reports.ErrorR\x06\x65rrorsB\x08\n\x06report\"\xb5\x01\n\x12GeneReportMetadata\x12=\n\x08messages\x18\x01 \x03(\x0b\x32!.ncbi.datasets.v2.reports.MessageR\x08messages\x12?\n\x05genes\x18\x02 \x03(\x0b\x32).ncbi.datasets.v2.reports.GeneReportMatchR\x05genes\x12\x1f\n\x0btotal_count\x18\x03 \x01(\rR\ntotalCount\"\x91\x01\n\x0bOrthologSet\x12&\n\x0fortholog_set_id\x18\x01 \x01(\rR\rorthologSetId\x12\x16\n\x06method\x18\x02 \x01(\tR\x06method\x12\x42\n\x05genes\x18\x03 \x01(\x0b\x32,.ncbi.datasets.v2.reports.GeneReportMetadataR\x05genes\"\xcc\x02\n\x12GeneDataReportPage\x12\x43\n\x07reports\x18\x01 \x03(\x0b\x32).ncbi.datasets.v2.reports.GeneReportMatchR\x07reports\x12=\n\x08messages\x18\x02 \x03(\x0b\x32!.ncbi.datasets.v2.reports.MessageR\x08messages\x12\x1f\n\x0btotal_count\x18\x03 \x01(\rR\ntotalCount\x12&\n\x0fnext_page_token\x18\x04 \x01(\tR\rnextPageToken\x12!\n\x0c_report_type\x18\xf4\x03 \x01(\tR\nReportType\x12%\n\x0e_report_fields\x18\xf5\x03 \x03(\tR\x0cReportFields\x12\x1f\n\x0b_first_page\x18\xf6\x03 \x01(\x08R\tFirstPage\"\xac\x01\n\rMaturePeptide\x12G\n\x11\x61\x63\x63\x65ssion_version\x18\x01 \x01(\tB\x1a\xc2\xf3\x18\x16\n\taccession\x12\tAccessionR\x10\x61\x63\x63\x65ssionVersion\x12$\n\x04name\x18\x02 \x01(\tB\x10\xc2\xf3\x18\x0c\n\x04name\x12\x04NameR\x04name\x12,\n\x06length\x18\x03 \x01(\rB\x14\xc2\xf3\x18\x10\n\x06length\x12\x06LengthR\x06length\"\xed\x03\n\x07Protein\x12W\n\x11\x61\x63\x63\x65ssion_version\x18\x01 \x01(\tB*\xc2\xf3\x18&\n\taccession\x12\tAccession2\x0eNP_001296812.1R\x10\x61\x63\x63\x65ssionVersion\x12\x32\n\x04name\x18\x02 \x01(\tB\x1e\xc2\xf3\x18\x1a\n\x04name\x12\x04Name2\x0cprotein ALEXR\x04name\x12\x31\n\x06length\x18\x03 \x01(\rB\x19\xc2\xf3\x18\x15\n\x06length\x12\x06Length2\x03\x36\x32\x36R\x06length\x12G\n\x0cisoform_name\x18\x05 \x01(\tB$\xc2\xf3\x18 \n\x07isoform\x12\x07Isoform2\x0cisoform AlexR\x0bisoformName\x12\x62\n\x0f\x65nsembl_protein\x18\x06 \x01(\tB9\xc2\xf3\x18\x35\n\x0f\x65nsembl-protein\x12\x0f\x45nsembl Protein2\x11\x45NSP00000302237.3R\x0e\x65nsemblProtein\x12u\n\x0fmature_peptides\x18\x04 \x03(\x0b\x32\'.ncbi.datasets.v2.reports.MaturePeptideB#\xc2\xf3\x18\x1f\n\x0cmat-peptide-\x12\x0fMature Peptide R\x0ematurePeptides\"\xc9\x02\n\x0fGenomicLocation\x12W\n\x19genomic_accession_version\x18\x01 \x01(\tB\x1b\xc2\xf3\x18\x17\n\taccession\x12\nAccession R\x17genomicAccessionVersion\x12=\n\rsequence_name\x18\x02 \x01(\tB\x18\xc2\xf3\x18\x14\n\x08seq-name\x12\x08Seq NameR\x0csequenceName\x12R\n\rgenomic_range\x18\x03 \x01(\x0b\x32\x1f.ncbi.datasets.v2.reports.RangeB\x0c\xc2\xf3\x18\x08\n\x06range-R\x0cgenomicRange\x12J\n\x05\x65xons\x18\x04 \x03(\x0b\x32\x1f.ncbi.datasets.v2.reports.RangeB\x13\xc2\xf3\x18\x0f\n\x05\x65xon-\x12\x06\x45xons R\x05\x65xons\"\xd3\x07\n\nTranscript\x12G\n\x11\x61\x63\x63\x65ssion_version\x18\x01 \x01(\tB\x1a\xc2\xf3\x18\x16\n\taccession\x12\tAccessionR\x10\x61\x63\x63\x65ssionVersion\x12\x46\n\x04name\x18\x02 \x01(\tB2\xc2\xf3\x18.\n\x04name\x12\x0fTranscript Name2\x15transcript variant 12R\x04name\x12=\n\x06length\x18\x03 \x01(\rB%\xc2\xf3\x18!\n\x06length\x12\x11Transcript Length2\x04\x33\x31\x38\x30R\x06length\x12N\n\rgenomic_range\x18\x04 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB\x02\x18\x01R\x0cgenomicRange\x12?\n\x05\x65xons\x18\x05 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB\x02\x18\x01R\x05\x65xons\x12I\n\x03\x63\x64s\x18\x06 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB\x10\xc2\xf3\x18\x0c\n\x04\x63\x64s-\x12\x04\x43\x44S R\x03\x63\x64s\x12y\n\x11genomic_locations\x18\n \x03(\x0b\x32).ncbi.datasets.v2.reports.GenomicLocationB!\xc2\xf3\x18\x1d\n\x11genomic-location-\x12\x08Genomic R\x10genomicLocations\x12n\n\x12\x65nsembl_transcript\x18\x08 \x01(\tB?\xc2\xf3\x18;\n\x12\x65nsembl-transcript\x12\x12\x45nsembl Transcript2\x11\x45NST00000306120.3R\x11\x65nsemblTranscript\x12U\n\x07protein\x18\x07 \x01(\x0b\x32!.ncbi.datasets.v2.reports.ProteinB\x18\xc2\xf3\x18\x14\n\x08protein-\x12\x08Protein R\x07protein\x12\x64\n\x04type\x18\t \x01(\x0e\x32\x33.ncbi.datasets.v2.reports.Transcript.TranscriptTypeB\x1b\xc2\xf3\x18\x17\n\x0ftranscript-type\x12\x04TypeR\x04type\"q\n\x0eTranscriptType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0ePROTEIN_CODING\x10\x01\x12\x0e\n\nNON_CODING\x10\x02\x12\x18\n\x14PROTEIN_CODING_MODEL\x10\x03\x12\x14\n\x10NON_CODING_MODEL\x10\x04\"\xd9\x02\n\rGenomicRegion\x12\x64\n\ngene_range\x18\x01 \x01(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB\x1e\xc2\xf3\x18\x1a\n\x0bgene-range-\x12\x0bGene Range R\tgeneRange\x12}\n\x04type\x18\x02 \x01(\x0e\x32\x39.ncbi.datasets.v2.reports.GenomicRegion.GenomicRegionTypeB.\xc2\xf3\x18*\n\x13genomic-region-type\x12\x13Genomic Region TypeR\x04type\"c\n\x11GenomicRegionType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0f\n\x0bREFSEQ_GENE\x10\x01\x12\x0e\n\nPSEUDOGENE\x10\x02\x12\x15\n\x11\x42IOLOGICAL_REGION\x10\x03\x12\t\n\x05OTHER\x10\x04\"\xa8\x02\n\nAnnotation\x12\x43\n\x0crelease_name\x18\x01 \x01(\tB \xc2\xf3\x18\x1c\n\x0crelease-name\x12\x0cRelease NameR\x0breleaseName\x12\x43\n\x0crelease_date\x18\x02 \x01(\tB \xc2\xf3\x18\x1c\n\x0crelease-date\x12\x0cRelease DateR\x0breleaseDate\x12\x8f\x01\n\x13\x61ssemblies_in_scope\x18\x03 \x03(\x0b\x32-.ncbi.datasets.v2.reports.AnnotatedAssembliesB0\xc2\xf3\x18,\n\x14\x61ssemblies-in-scope-\x12\x14\x41ssemblies in Scope R\x11\x61ssembliesInScope\"u\n\x13\x41nnotatedAssemblies\x12\x38\n\taccession\x18\x01 \x01(\tB\x1a\xc2\xf3\x18\x16\n\taccession\x12\tAccessionR\taccession\x12$\n\x04name\x18\x02 \x01(\tB\x10\xc2\xf3\x18\x0c\n\x04name\x12\x04NameR\x04name\"\x83\x12\n\x0eGeneDescriptor\x12\x39\n\x07gene_id\x18\x01 \x01(\x04\x42 \xc2\xf3\x18\x1c\n\x07gene-id\x12\x0bNCBI GeneID2\x04\x32\x37\x37\x38R\x06geneId\x12\x32\n\x06symbol\x18\x02 \x01(\tB\x1a\xc2\xf3\x18\x16\n\x06symbol\x12\x06Symbol2\x04GNASR\x06symbol\x12T\n\x0b\x64\x65scription\x18\x03 \x01(\tB2\xc2\xf3\x18.\n\x0b\x64\x65scription\x12\x0b\x44\x65scription2\x12GNAS complex locusR\x0b\x64\x65scription\x12\x37\n\x06tax_id\x18\x04 \x01(\x04\x42 \xc2\xf3\x18\x1c\n\x06tax-id\x12\x0cTaxonomic ID2\x04\x39\x36\x30\x36R\x05taxId\x12\x46\n\x07taxname\x18\x05 \x01(\tB,\xc2\xf3\x18(\n\x08tax-name\x12\x0eTaxonomic Name2\x0cHomo sapiensR\x07taxname\x12\x46\n\x0b\x63ommon_name\x18\x0c \x01(\tB%\xc2\xf3\x18!\n\x0b\x63ommon-name\x12\x0b\x43ommon Name2\x05humanR\ncommonName\x12\x61\n\x04type\x18\x06 \x01(\x0e\x32\x31.ncbi.datasets.v2.reports.GeneDescriptor.GeneTypeB\x1a\xc2\xf3\x18\x16\n\tgene-type\x12\tGene TypeR\x04type\x12\x65\n\x08rna_type\x18\x0b \x01(\x0e\x32\x30.ncbi.datasets.v2.reports.GeneDescriptor.RnaTypeB\x18\xc2\xf3\x18\x14\n\x08rna-type\x12\x08RNA TypeR\x07rnaType\x12g\n\x0borientation\x18\x07 \x01(\x0e\x32%.ncbi.datasets.v2.reports.OrientationB\x1e\xc2\xf3\x18\x1a\n\x0borientation\x12\x0bOrientationR\x0borientation\x12r\n\x0egenomic_ranges\x18\x08 \x03(\x0b\x32%.ncbi.datasets.v2.reports.SeqRangeSetB$\xc2\xf3\x18 \n\x0egenomic-range-\x12\x0eGenomic Range R\rgenomicRanges\x12\x82\x01\n\x13reference_standards\x18\x15 \x03(\x0b\x32\'.ncbi.datasets.v2.reports.GenomicRegionB(\xc2\xf3\x18$\n\rref-standard-\x12\x13Reference Standard R\x12referenceStandards\x12x\n\x0fgenomic_regions\x18\x16 \x03(\x0b\x32\'.ncbi.datasets.v2.reports.GenomicRegionB&\xc2\xf3\x18\"\n\x0fgenomic-region-\x12\x0fGenomic Region R\x0egenomicRegions\x12\"\n\nchromosome\x18\r \x01(\tB\x02\x18\x01R\nchromosome\x12H\n\x0b\x63hromosomes\x18\x0e \x03(\tB&\xc2\xf3\x18\"\n\x0b\x63hromosomes\x12\x0b\x43hromosomes2\x01\x31\x32\x03X,YR\x0b\x63hromosomes\x12\x82\x01\n\x16nomenclature_authority\x18\x0f \x01(\x0b\x32/.ncbi.datasets.v2.reports.NomenclatureAuthorityB\x1a\xc2\xf3\x18\x16\n\x05name-\x12\rNomenclature R\x15nomenclatureAuthority\x12\x64\n\x15swiss_prot_accessions\x18\x10 \x03(\tB0\xc2\xf3\x18,\n\x14swissprot-accessions\x12\x14SwissProt AccessionsR\x13swissProtAccessions\x12P\n\x10\x65nsembl_gene_ids\x18\x11 \x03(\tB&\xc2\xf3\x18\"\n\x0f\x65nsembl-geneids\x12\x0f\x45nsembl GeneIDsR\x0e\x65nsemblGeneIds\x12\x33\n\x08omim_ids\x18\x12 \x03(\tB\x18\xc2\xf3\x18\x14\n\x08omim-ids\x12\x08OMIM IDsR\x07omimIds\x12\x34\n\x08synonyms\x18\x13 \x03(\tB\x18\xc2\xf3\x18\x14\n\x08synonyms\x12\x08SynonymsR\x08synonyms\x12V\n\x10replaced_gene_id\x18\x14 \x01(\x04\x42,\xc2\xf3\x18(\n\x10replaced-gene-id\x12\x14Replaced NCBI GeneIDR\x0ereplacedGeneId\x12\x66\n\x0b\x61nnotations\x18\x17 \x03(\x0b\x32$.ncbi.datasets.v2.reports.AnnotationB\x1e\xc2\xf3\x18\x1a\n\x0b\x61nnotation-\x12\x0b\x41nnotation R\x0b\x61nnotations\x12)\n\x10transcript_count\x18\x1a \x01(\rR\x0ftranscriptCount\x12#\n\rprotein_count\x18\x1b \x01(\rR\x0cproteinCount\x12\x63\n\x16transcript_type_counts\x18\x1c \x03(\x0b\x32-.ncbi.datasets.v2.reports.TranscriptTypeCountR\x14transcriptTypeCounts\x12\x44\n\x0bgene_groups\x18\x1d \x03(\x0b\x32#.ncbi.datasets.v2.reports.GeneGroupR\ngeneGroups\"\xb8\x01\n\x08GeneType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04tRNA\x10\x01\x12\x08\n\x04rRNA\x10\x02\x12\t\n\x05snRNA\x10\x03\x12\t\n\x05scRNA\x10\x04\x12\n\n\x06snoRNA\x10\x05\x12\x12\n\x0ePROTEIN_CODING\x10\x06\x12\n\n\x06PSEUDO\x10\x07\x12\x0e\n\nTRANSPOSON\x10\x08\x12\x0b\n\x07miscRNA\x10\t\x12\t\n\x05ncRNA\x10\n\x12\x15\n\x11\x42IOLOGICAL_REGION\x10\x0b\x12\n\n\x05OTHER\x10\xff\x01\"1\n\x07RnaType\x12\x0f\n\x0brna_UNKNOWN\x10\x00\x12\n\n\x06premsg\x10\x01\x12\t\n\x05tmRna\x10\x02\"3\n\tGeneGroup\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x16\n\x06method\x18\x02 \x01(\tR\x06method\"\x88\x07\n\x11ProductDescriptor\x12\x39\n\x07gene_id\x18\x01 \x01(\x04\x42 \xc2\xf3\x18\x1c\n\x07gene-id\x12\x0bNCBI GeneID2\x04\x32\x37\x37\x38R\x06geneId\x12\x32\n\x06symbol\x18\x02 \x01(\tB\x1a\xc2\xf3\x18\x16\n\x06symbol\x12\x06Symbol2\x04GNASR\x06symbol\x12T\n\x0b\x64\x65scription\x18\x03 \x01(\tB2\xc2\xf3\x18.\n\x0b\x64\x65scription\x12\x0b\x44\x65scription2\x12GNAS complex locusR\x0b\x64\x65scription\x12\x37\n\x06tax_id\x18\x04 \x01(\x04\x42 \xc2\xf3\x18\x1c\n\x06tax-id\x12\x0cTaxonomic ID2\x04\x39\x36\x30\x36R\x05taxId\x12\x46\n\x07taxname\x18\x05 \x01(\tB,\xc2\xf3\x18(\n\x08tax-name\x12\x0eTaxonomic Name2\x0cHomo sapiensR\x07taxname\x12\x46\n\x0b\x63ommon_name\x18\x0c \x01(\tB%\xc2\xf3\x18!\n\x0b\x63ommon-name\x12\x0b\x43ommon Name2\x05humanR\ncommonName\x12\x61\n\x04type\x18\x06 \x01(\x0e\x32\x31.ncbi.datasets.v2.reports.GeneDescriptor.GeneTypeB\x1a\xc2\xf3\x18\x16\n\tgene-type\x12\tGene TypeR\x04type\x12\x65\n\x08rna_type\x18\x0b \x01(\x0e\x32\x30.ncbi.datasets.v2.reports.GeneDescriptor.RnaTypeB\x18\xc2\xf3\x18\x14\n\x08rna-type\x12\x08RNA TypeR\x07rnaType\x12\x66\n\x0btranscripts\x18\t \x03(\x0b\x32$.ncbi.datasets.v2.reports.TranscriptB\x1e\xc2\xf3\x18\x1a\n\x0btranscript-\x12\x0bTranscript R\x0btranscripts\x12)\n\x10transcript_count\x18\x1a \x01(\rR\x0ftranscriptCount\x12#\n\rprotein_count\x18\x1b \x01(\rR\x0cproteinCount\x12\x63\n\x16transcript_type_counts\x18\x1c \x03(\x0b\x32-.ncbi.datasets.v2.reports.TranscriptTypeCountR\x14transcriptTypeCounts\"t\n\x13TranscriptTypeCount\x12G\n\x04type\x18\x01 \x01(\x0e\x32\x33.ncbi.datasets.v2.reports.Transcript.TranscriptTypeR\x04type\x12\x14\n\x05\x63ount\x18\x02 \x01(\rR\x05\x63ount\"\x90\x01\n\x15NomenclatureAuthority\x12>\n\tauthority\x18\x01 \x01(\tB \xc2\xf3\x18\x1c\n\tauthority\x12\tAuthority2\x04HGNCR\tauthority\x12\x37\n\nidentifier\x18\x02 \x01(\tB\x17\xc2\xf3\x18\x13\n\x02id\x12\x02ID2\tHGNC:4392R\nidentifier\"Q\n\x0fGeneDescriptors\x12>\n\x05genes\x18\x01 \x03(\x0b\x32(.ncbi.datasets.v2.reports.GeneDescriptorR\x05genesB\x9d\nZ\x18ncbi/datasets/v2/reports\xf8\x01\x01\xc2\xf3\x18\xfb\t\n\x0bGene Report\x12\x0eGeneDescriptor\x1a=<p>The downloaded gene package contains a gene data report in\x1a:<a href=\"https://jsonlines.readthedocs.io/\">JSON Lines</a>\x1aOformat in the file:<br><br><em>ncbi_dataset/data/data_report.jsonl</em><br><br>\x1amEach line of the gene data report file is a hierarchical <a href=\"https://www.json.org/json-en.html\">JSON</a>\x1aiobject that represents a single gene record. The schema of the gene record is defined in the tables below\x1ajwhere each row describes a single field in the report or a sub-structure, which is a collection of fields.\x1a\x45The outermost structure of the report is <em>GeneDescriptor</em>.</p>\x1aQ<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\x1a\x91\x01<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s <nobr><code>--fields</code></nobr> option.\x1a\x93\x01Refer to the <a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how you can use this tool\x1a\x46to transform gene data reports from JSON Lines to tabular formats.</p>\"\x0fLineageOrganism\"\x08Organism\"\x0fGeneDescriptors*\x91\x01{{< readfile-code-block lang=\"json\" file=\"/docs_samples/dataformat-cli/gene-to-tsv.cli.output\" begin=\"START data-report\" end=\"END data-report\">}}b\x06proto3')



_GENEREPORTMATCH = DESCRIPTOR.message_types_by_name['GeneReportMatch']
_GENEREPORTMETADATA = DESCRIPTOR.message_types_by_name['GeneReportMetadata']
_ORTHOLOGSET = DESCRIPTOR.message_types_by_name['OrthologSet']
_GENEDATAREPORTPAGE = DESCRIPTOR.message_types_by_name['GeneDataReportPage']
_MATUREPEPTIDE = DESCRIPTOR.message_types_by_name['MaturePeptide']
_PROTEIN = DESCRIPTOR.message_types_by_name['Protein']
_GENOMICLOCATION = DESCRIPTOR.message_types_by_name['GenomicLocation']
_TRANSCRIPT = DESCRIPTOR.message_types_by_name['Transcript']
_GENOMICREGION = DESCRIPTOR.message_types_by_name['GenomicRegion']
_ANNOTATION = DESCRIPTOR.message_types_by_name['Annotation']
_ANNOTATEDASSEMBLIES = DESCRIPTOR.message_types_by_name['AnnotatedAssemblies']
_GENEDESCRIPTOR = DESCRIPTOR.message_types_by_name['GeneDescriptor']
_GENEGROUP = DESCRIPTOR.message_types_by_name['GeneGroup']
_PRODUCTDESCRIPTOR = DESCRIPTOR.message_types_by_name['ProductDescriptor']
_TRANSCRIPTTYPECOUNT = DESCRIPTOR.message_types_by_name['TranscriptTypeCount']
_NOMENCLATUREAUTHORITY = DESCRIPTOR.message_types_by_name['NomenclatureAuthority']
_GENEDESCRIPTORS = DESCRIPTOR.message_types_by_name['GeneDescriptors']
_TRANSCRIPT_TRANSCRIPTTYPE = _TRANSCRIPT.enum_types_by_name['TranscriptType']
_GENOMICREGION_GENOMICREGIONTYPE = _GENOMICREGION.enum_types_by_name['GenomicRegionType']
_GENEDESCRIPTOR_GENETYPE = _GENEDESCRIPTOR.enum_types_by_name['GeneType']
_GENEDESCRIPTOR_RNATYPE = _GENEDESCRIPTOR.enum_types_by_name['RnaType']
GeneReportMatch = _reflection.GeneratedProtocolMessageType('GeneReportMatch', (_message.Message,), {
  'DESCRIPTOR' : _GENEREPORTMATCH,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneReportMatch)
  })
_sym_db.RegisterMessage(GeneReportMatch)

GeneReportMetadata = _reflection.GeneratedProtocolMessageType('GeneReportMetadata', (_message.Message,), {
  'DESCRIPTOR' : _GENEREPORTMETADATA,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneReportMetadata)
  })
_sym_db.RegisterMessage(GeneReportMetadata)

OrthologSet = _reflection.GeneratedProtocolMessageType('OrthologSet', (_message.Message,), {
  'DESCRIPTOR' : _ORTHOLOGSET,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.OrthologSet)
  })
_sym_db.RegisterMessage(OrthologSet)

GeneDataReportPage = _reflection.GeneratedProtocolMessageType('GeneDataReportPage', (_message.Message,), {
  'DESCRIPTOR' : _GENEDATAREPORTPAGE,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneDataReportPage)
  })
_sym_db.RegisterMessage(GeneDataReportPage)

MaturePeptide = _reflection.GeneratedProtocolMessageType('MaturePeptide', (_message.Message,), {
  'DESCRIPTOR' : _MATUREPEPTIDE,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.MaturePeptide)
  })
_sym_db.RegisterMessage(MaturePeptide)

Protein = _reflection.GeneratedProtocolMessageType('Protein', (_message.Message,), {
  'DESCRIPTOR' : _PROTEIN,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Protein)
  })
_sym_db.RegisterMessage(Protein)

GenomicLocation = _reflection.GeneratedProtocolMessageType('GenomicLocation', (_message.Message,), {
  'DESCRIPTOR' : _GENOMICLOCATION,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GenomicLocation)
  })
_sym_db.RegisterMessage(GenomicLocation)

Transcript = _reflection.GeneratedProtocolMessageType('Transcript', (_message.Message,), {
  'DESCRIPTOR' : _TRANSCRIPT,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Transcript)
  })
_sym_db.RegisterMessage(Transcript)

GenomicRegion = _reflection.GeneratedProtocolMessageType('GenomicRegion', (_message.Message,), {
  'DESCRIPTOR' : _GENOMICREGION,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GenomicRegion)
  })
_sym_db.RegisterMessage(GenomicRegion)

Annotation = _reflection.GeneratedProtocolMessageType('Annotation', (_message.Message,), {
  'DESCRIPTOR' : _ANNOTATION,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.Annotation)
  })
_sym_db.RegisterMessage(Annotation)

AnnotatedAssemblies = _reflection.GeneratedProtocolMessageType('AnnotatedAssemblies', (_message.Message,), {
  'DESCRIPTOR' : _ANNOTATEDASSEMBLIES,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.AnnotatedAssemblies)
  })
_sym_db.RegisterMessage(AnnotatedAssemblies)

GeneDescriptor = _reflection.GeneratedProtocolMessageType('GeneDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _GENEDESCRIPTOR,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneDescriptor)
  })
_sym_db.RegisterMessage(GeneDescriptor)

GeneGroup = _reflection.GeneratedProtocolMessageType('GeneGroup', (_message.Message,), {
  'DESCRIPTOR' : _GENEGROUP,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneGroup)
  })
_sym_db.RegisterMessage(GeneGroup)

ProductDescriptor = _reflection.GeneratedProtocolMessageType('ProductDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _PRODUCTDESCRIPTOR,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.ProductDescriptor)
  })
_sym_db.RegisterMessage(ProductDescriptor)

TranscriptTypeCount = _reflection.GeneratedProtocolMessageType('TranscriptTypeCount', (_message.Message,), {
  'DESCRIPTOR' : _TRANSCRIPTTYPECOUNT,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.TranscriptTypeCount)
  })
_sym_db.RegisterMessage(TranscriptTypeCount)

NomenclatureAuthority = _reflection.GeneratedProtocolMessageType('NomenclatureAuthority', (_message.Message,), {
  'DESCRIPTOR' : _NOMENCLATUREAUTHORITY,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.NomenclatureAuthority)
  })
_sym_db.RegisterMessage(NomenclatureAuthority)

GeneDescriptors = _reflection.GeneratedProtocolMessageType('GeneDescriptors', (_message.Message,), {
  'DESCRIPTOR' : _GENEDESCRIPTORS,
  '__module__' : 'ncbi.datasets.v2.reports.gene_pb2'
  # @@protoc_insertion_point(class_scope:ncbi.datasets.v2.reports.GeneDescriptors)
  })
_sym_db.RegisterMessage(GeneDescriptors)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\030ncbi/datasets/v2/reports\370\001\001\302\363\030\373\t\n\013Gene Report\022\016GeneDescriptor\032=<p>The downloaded gene package contains a gene data report in\032:<a href=\"https://jsonlines.readthedocs.io/\">JSON Lines</a>\032Oformat in the file:<br><br><em>ncbi_dataset/data/data_report.jsonl</em><br><br>\032mEach line of the gene data report file is a hierarchical <a href=\"https://www.json.org/json-en.html\">JSON</a>\032iobject that represents a single gene record. The schema of the gene record is defined in the tables below\032jwhere each row describes a single field in the report or a sub-structure, which is a collection of fields.\032EThe outermost structure of the report is <em>GeneDescriptor</em>.</p>\032Q<p>Table fields that include a <em>Table Field Mnemonic</em> can be used with the\032\221\001<a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> command-line tool\'s <nobr><code>--fields</code></nobr> option.\032\223\001Refer to the <a href=\"/datasets/docs/v2/reference-docs/command-line/dataformat/\">dataformat</a> CLI tool reference to see how you can use this tool\032Fto transform gene data reports from JSON Lines to tabular formats.</p>\"\017LineageOrganism\"\010Organism\"\017GeneDescriptors*\221\001{{< readfile-code-block lang=\"json\" file=\"/docs_samples/dataformat-cli/gene-to-tsv.cli.output\" begin=\"START data-report\" end=\"END data-report\">}}'
  _MATUREPEPTIDE.fields_by_name['accession_version']._options = None
  _MATUREPEPTIDE.fields_by_name['accession_version']._serialized_options = b'\302\363\030\026\n\taccession\022\tAccession'
  _MATUREPEPTIDE.fields_by_name['name']._options = None
  _MATUREPEPTIDE.fields_by_name['name']._serialized_options = b'\302\363\030\014\n\004name\022\004Name'
  _MATUREPEPTIDE.fields_by_name['length']._options = None
  _MATUREPEPTIDE.fields_by_name['length']._serialized_options = b'\302\363\030\020\n\006length\022\006Length'
  _PROTEIN.fields_by_name['accession_version']._options = None
  _PROTEIN.fields_by_name['accession_version']._serialized_options = b'\302\363\030&\n\taccession\022\tAccession2\016NP_001296812.1'
  _PROTEIN.fields_by_name['name']._options = None
  _PROTEIN.fields_by_name['name']._serialized_options = b'\302\363\030\032\n\004name\022\004Name2\014protein ALEX'
  _PROTEIN.fields_by_name['length']._options = None
  _PROTEIN.fields_by_name['length']._serialized_options = b'\302\363\030\025\n\006length\022\006Length2\003626'
  _PROTEIN.fields_by_name['isoform_name']._options = None
  _PROTEIN.fields_by_name['isoform_name']._serialized_options = b'\302\363\030 \n\007isoform\022\007Isoform2\014isoform Alex'
  _PROTEIN.fields_by_name['ensembl_protein']._options = None
  _PROTEIN.fields_by_name['ensembl_protein']._serialized_options = b'\302\363\0305\n\017ensembl-protein\022\017Ensembl Protein2\021ENSP00000302237.3'
  _PROTEIN.fields_by_name['mature_peptides']._options = None
  _PROTEIN.fields_by_name['mature_peptides']._serialized_options = b'\302\363\030\037\n\014mat-peptide-\022\017Mature Peptide '
  _GENOMICLOCATION.fields_by_name['genomic_accession_version']._options = None
  _GENOMICLOCATION.fields_by_name['genomic_accession_version']._serialized_options = b'\302\363\030\027\n\taccession\022\nAccession '
  _GENOMICLOCATION.fields_by_name['sequence_name']._options = None
  _GENOMICLOCATION.fields_by_name['sequence_name']._serialized_options = b'\302\363\030\024\n\010seq-name\022\010Seq Name'
  _GENOMICLOCATION.fields_by_name['genomic_range']._options = None
  _GENOMICLOCATION.fields_by_name['genomic_range']._serialized_options = b'\302\363\030\010\n\006range-'
  _GENOMICLOCATION.fields_by_name['exons']._options = None
  _GENOMICLOCATION.fields_by_name['exons']._serialized_options = b'\302\363\030\017\n\005exon-\022\006Exons '
  _TRANSCRIPT.fields_by_name['accession_version']._options = None
  _TRANSCRIPT.fields_by_name['accession_version']._serialized_options = b'\302\363\030\026\n\taccession\022\tAccession'
  _TRANSCRIPT.fields_by_name['name']._options = None
  _TRANSCRIPT.fields_by_name['name']._serialized_options = b'\302\363\030.\n\004name\022\017Transcript Name2\025transcript variant 12'
  _TRANSCRIPT.fields_by_name['length']._options = None
  _TRANSCRIPT.fields_by_name['length']._serialized_options = b'\302\363\030!\n\006length\022\021Transcript Length2\0043180'
  _TRANSCRIPT.fields_by_name['genomic_range']._options = None
  _TRANSCRIPT.fields_by_name['genomic_range']._serialized_options = b'\030\001'
  _TRANSCRIPT.fields_by_name['exons']._options = None
  _TRANSCRIPT.fields_by_name['exons']._serialized_options = b'\030\001'
  _TRANSCRIPT.fields_by_name['cds']._options = None
  _TRANSCRIPT.fields_by_name['cds']._serialized_options = b'\302\363\030\014\n\004cds-\022\004CDS '
  _TRANSCRIPT.fields_by_name['genomic_locations']._options = None
  _TRANSCRIPT.fields_by_name['genomic_locations']._serialized_options = b'\302\363\030\035\n\021genomic-location-\022\010Genomic '
  _TRANSCRIPT.fields_by_name['ensembl_transcript']._options = None
  _TRANSCRIPT.fields_by_name['ensembl_transcript']._serialized_options = b'\302\363\030;\n\022ensembl-transcript\022\022Ensembl Transcript2\021ENST00000306120.3'
  _TRANSCRIPT.fields_by_name['protein']._options = None
  _TRANSCRIPT.fields_by_name['protein']._serialized_options = b'\302\363\030\024\n\010protein-\022\010Protein '
  _TRANSCRIPT.fields_by_name['type']._options = None
  _TRANSCRIPT.fields_by_name['type']._serialized_options = b'\302\363\030\027\n\017transcript-type\022\004Type'
  _GENOMICREGION.fields_by_name['gene_range']._options = None
  _GENOMICREGION.fields_by_name['gene_range']._serialized_options = b'\302\363\030\032\n\013gene-range-\022\013Gene Range '
  _GENOMICREGION.fields_by_name['type']._options = None
  _GENOMICREGION.fields_by_name['type']._serialized_options = b'\302\363\030*\n\023genomic-region-type\022\023Genomic Region Type'
  _ANNOTATION.fields_by_name['release_name']._options = None
  _ANNOTATION.fields_by_name['release_name']._serialized_options = b'\302\363\030\034\n\014release-name\022\014Release Name'
  _ANNOTATION.fields_by_name['release_date']._options = None
  _ANNOTATION.fields_by_name['release_date']._serialized_options = b'\302\363\030\034\n\014release-date\022\014Release Date'
  _ANNOTATION.fields_by_name['assemblies_in_scope']._options = None
  _ANNOTATION.fields_by_name['assemblies_in_scope']._serialized_options = b'\302\363\030,\n\024assemblies-in-scope-\022\024Assemblies in Scope '
  _ANNOTATEDASSEMBLIES.fields_by_name['accession']._options = None
  _ANNOTATEDASSEMBLIES.fields_by_name['accession']._serialized_options = b'\302\363\030\026\n\taccession\022\tAccession'
  _ANNOTATEDASSEMBLIES.fields_by_name['name']._options = None
  _ANNOTATEDASSEMBLIES.fields_by_name['name']._serialized_options = b'\302\363\030\014\n\004name\022\004Name'
  _GENEDESCRIPTOR.fields_by_name['gene_id']._options = None
  _GENEDESCRIPTOR.fields_by_name['gene_id']._serialized_options = b'\302\363\030\034\n\007gene-id\022\013NCBI GeneID2\0042778'
  _GENEDESCRIPTOR.fields_by_name['symbol']._options = None
  _GENEDESCRIPTOR.fields_by_name['symbol']._serialized_options = b'\302\363\030\026\n\006symbol\022\006Symbol2\004GNAS'
  _GENEDESCRIPTOR.fields_by_name['description']._options = None
  _GENEDESCRIPTOR.fields_by_name['description']._serialized_options = b'\302\363\030.\n\013description\022\013Description2\022GNAS complex locus'
  _GENEDESCRIPTOR.fields_by_name['tax_id']._options = None
  _GENEDESCRIPTOR.fields_by_name['tax_id']._serialized_options = b'\302\363\030\034\n\006tax-id\022\014Taxonomic ID2\0049606'
  _GENEDESCRIPTOR.fields_by_name['taxname']._options = None
  _GENEDESCRIPTOR.fields_by_name['taxname']._serialized_options = b'\302\363\030(\n\010tax-name\022\016Taxonomic Name2\014Homo sapiens'
  _GENEDESCRIPTOR.fields_by_name['common_name']._options = None
  _GENEDESCRIPTOR.fields_by_name['common_name']._serialized_options = b'\302\363\030!\n\013common-name\022\013Common Name2\005human'
  _GENEDESCRIPTOR.fields_by_name['type']._options = None
  _GENEDESCRIPTOR.fields_by_name['type']._serialized_options = b'\302\363\030\026\n\tgene-type\022\tGene Type'
  _GENEDESCRIPTOR.fields_by_name['rna_type']._options = None
  _GENEDESCRIPTOR.fields_by_name['rna_type']._serialized_options = b'\302\363\030\024\n\010rna-type\022\010RNA Type'
  _GENEDESCRIPTOR.fields_by_name['orientation']._options = None
  _GENEDESCRIPTOR.fields_by_name['orientation']._serialized_options = b'\302\363\030\032\n\013orientation\022\013Orientation'
  _GENEDESCRIPTOR.fields_by_name['genomic_ranges']._options = None
  _GENEDESCRIPTOR.fields_by_name['genomic_ranges']._serialized_options = b'\302\363\030 \n\016genomic-range-\022\016Genomic Range '
  _GENEDESCRIPTOR.fields_by_name['reference_standards']._options = None
  _GENEDESCRIPTOR.fields_by_name['reference_standards']._serialized_options = b'\302\363\030$\n\rref-standard-\022\023Reference Standard '
  _GENEDESCRIPTOR.fields_by_name['genomic_regions']._options = None
  _GENEDESCRIPTOR.fields_by_name['genomic_regions']._serialized_options = b'\302\363\030\"\n\017genomic-region-\022\017Genomic Region '
  _GENEDESCRIPTOR.fields_by_name['chromosome']._options = None
  _GENEDESCRIPTOR.fields_by_name['chromosome']._serialized_options = b'\030\001'
  _GENEDESCRIPTOR.fields_by_name['chromosomes']._options = None
  _GENEDESCRIPTOR.fields_by_name['chromosomes']._serialized_options = b'\302\363\030\"\n\013chromosomes\022\013Chromosomes2\00112\003X,Y'
  _GENEDESCRIPTOR.fields_by_name['nomenclature_authority']._options = None
  _GENEDESCRIPTOR.fields_by_name['nomenclature_authority']._serialized_options = b'\302\363\030\026\n\005name-\022\rNomenclature '
  _GENEDESCRIPTOR.fields_by_name['swiss_prot_accessions']._options = None
  _GENEDESCRIPTOR.fields_by_name['swiss_prot_accessions']._serialized_options = b'\302\363\030,\n\024swissprot-accessions\022\024SwissProt Accessions'
  _GENEDESCRIPTOR.fields_by_name['ensembl_gene_ids']._options = None
  _GENEDESCRIPTOR.fields_by_name['ensembl_gene_ids']._serialized_options = b'\302\363\030\"\n\017ensembl-geneids\022\017Ensembl GeneIDs'
  _GENEDESCRIPTOR.fields_by_name['omim_ids']._options = None
  _GENEDESCRIPTOR.fields_by_name['omim_ids']._serialized_options = b'\302\363\030\024\n\010omim-ids\022\010OMIM IDs'
  _GENEDESCRIPTOR.fields_by_name['synonyms']._options = None
  _GENEDESCRIPTOR.fields_by_name['synonyms']._serialized_options = b'\302\363\030\024\n\010synonyms\022\010Synonyms'
  _GENEDESCRIPTOR.fields_by_name['replaced_gene_id']._options = None
  _GENEDESCRIPTOR.fields_by_name['replaced_gene_id']._serialized_options = b'\302\363\030(\n\020replaced-gene-id\022\024Replaced NCBI GeneID'
  _GENEDESCRIPTOR.fields_by_name['annotations']._options = None
  _GENEDESCRIPTOR.fields_by_name['annotations']._serialized_options = b'\302\363\030\032\n\013annotation-\022\013Annotation '
  _PRODUCTDESCRIPTOR.fields_by_name['gene_id']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['gene_id']._serialized_options = b'\302\363\030\034\n\007gene-id\022\013NCBI GeneID2\0042778'
  _PRODUCTDESCRIPTOR.fields_by_name['symbol']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['symbol']._serialized_options = b'\302\363\030\026\n\006symbol\022\006Symbol2\004GNAS'
  _PRODUCTDESCRIPTOR.fields_by_name['description']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['description']._serialized_options = b'\302\363\030.\n\013description\022\013Description2\022GNAS complex locus'
  _PRODUCTDESCRIPTOR.fields_by_name['tax_id']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['tax_id']._serialized_options = b'\302\363\030\034\n\006tax-id\022\014Taxonomic ID2\0049606'
  _PRODUCTDESCRIPTOR.fields_by_name['taxname']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['taxname']._serialized_options = b'\302\363\030(\n\010tax-name\022\016Taxonomic Name2\014Homo sapiens'
  _PRODUCTDESCRIPTOR.fields_by_name['common_name']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['common_name']._serialized_options = b'\302\363\030!\n\013common-name\022\013Common Name2\005human'
  _PRODUCTDESCRIPTOR.fields_by_name['type']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['type']._serialized_options = b'\302\363\030\026\n\tgene-type\022\tGene Type'
  _PRODUCTDESCRIPTOR.fields_by_name['rna_type']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['rna_type']._serialized_options = b'\302\363\030\024\n\010rna-type\022\010RNA Type'
  _PRODUCTDESCRIPTOR.fields_by_name['transcripts']._options = None
  _PRODUCTDESCRIPTOR.fields_by_name['transcripts']._serialized_options = b'\302\363\030\032\n\013transcript-\022\013Transcript '
  _NOMENCLATUREAUTHORITY.fields_by_name['authority']._options = None
  _NOMENCLATUREAUTHORITY.fields_by_name['authority']._serialized_options = b'\302\363\030\034\n\tauthority\022\tAuthority2\004HGNC'
  _NOMENCLATUREAUTHORITY.fields_by_name['identifier']._options = None
  _NOMENCLATUREAUTHORITY.fields_by_name['identifier']._serialized_options = b'\302\363\030\023\n\002id\022\002ID2\tHGNC:4392'
  _GENEREPORTMATCH._serialized_start=141
  _GENEREPORTMATCH._serialized_end=447
  _GENEREPORTMETADATA._serialized_start=450
  _GENEREPORTMETADATA._serialized_end=631
  _ORTHOLOGSET._serialized_start=634
  _ORTHOLOGSET._serialized_end=779
  _GENEDATAREPORTPAGE._serialized_start=782
  _GENEDATAREPORTPAGE._serialized_end=1114
  _MATUREPEPTIDE._serialized_start=1117
  _MATUREPEPTIDE._serialized_end=1289
  _PROTEIN._serialized_start=1292
  _PROTEIN._serialized_end=1785
  _GENOMICLOCATION._serialized_start=1788
  _GENOMICLOCATION._serialized_end=2117
  _TRANSCRIPT._serialized_start=2120
  _TRANSCRIPT._serialized_end=3099
  _TRANSCRIPT_TRANSCRIPTTYPE._serialized_start=2986
  _TRANSCRIPT_TRANSCRIPTTYPE._serialized_end=3099
  _GENOMICREGION._serialized_start=3102
  _GENOMICREGION._serialized_end=3447
  _GENOMICREGION_GENOMICREGIONTYPE._serialized_start=3348
  _GENOMICREGION_GENOMICREGIONTYPE._serialized_end=3447
  _ANNOTATION._serialized_start=3450
  _ANNOTATION._serialized_end=3746
  _ANNOTATEDASSEMBLIES._serialized_start=3748
  _ANNOTATEDASSEMBLIES._serialized_end=3865
  _GENEDESCRIPTOR._serialized_start=3868
  _GENEDESCRIPTOR._serialized_end=6175
  _GENEDESCRIPTOR_GENETYPE._serialized_start=5940
  _GENEDESCRIPTOR_GENETYPE._serialized_end=6124
  _GENEDESCRIPTOR_RNATYPE._serialized_start=6126
  _GENEDESCRIPTOR_RNATYPE._serialized_end=6175
  _GENEGROUP._serialized_start=6177
  _GENEGROUP._serialized_end=6228
  _PRODUCTDESCRIPTOR._serialized_start=6231
  _PRODUCTDESCRIPTOR._serialized_end=7135
  _TRANSCRIPTTYPECOUNT._serialized_start=7137
  _TRANSCRIPTTYPECOUNT._serialized_end=7253
  _NOMENCLATUREAUTHORITY._serialized_start=7256
  _NOMENCLATUREAUTHORITY._serialized_end=7400
  _GENEDESCRIPTORS._serialized_start=7402
  _GENEDESCRIPTORS._serialized_end=7483
# @@protoc_insertion_point(module_scope)
