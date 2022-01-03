import pytest
from vcf_wiper.header.header import Header
from vcf_wiper.body import BodyLineRecord


# Create tester header
header_lines = [
    '##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">\n',
    '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n',
    '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">\n',
    '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">\n',
    '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">\n',
    '##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">\n'
]

# create obj
header = Header()
header.read_header(header_lines)


wrong_body_header1 = "#CHROM	POS	ID	REF	ALT	QUAL	LTER	INFO	FORMAT"
body_header1 = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO"
body_header2 = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA00001	NA00002	NA00003"


def test_wrong_bodyheader():
    with pytest.raises(ValueError, match="Expected column not found: FILTER"):
        BodyLineRecord(body_header_line=wrong_body_header1)

body_line1 = "chr7	117180244	rs56093012	A	C	.	filter=cancer;cancer;SO:0001583|missense_variant;AF=0.1	AF=0.1;Uncertain_significance"
body_line2 = "20	14370	rs6054257	G	A	29	PASS	NS=3;DP=14;AF=0.5;DB;H2	GT:AF:GQ:DP:HQ	0|0:0.1:48:1:51,51	1|a:0.2:48:8:51,51	1/1:0.3:43:5:.,."


def test_col_num_not_matching():
    """col number shold match the number of cols in the body header"""
    nine_cols_header = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT"
    bodyrecord = BodyLineRecord(body_header_line=nine_cols_header)
    with pytest.raises(ValueError,
                match=r"Error in body record line: 1. Number of Columns not matching Body Header. Found: 8, Expected: 9"):
        bodyrecord.read_body_line(line=body_line1, line_number=1)


def test_bodyrecord_import():
    bodyrecord = BodyLineRecord(body_header_line=body_header1)
    bodyrecord.read_body_line(line=body_line1, line_number=1)

    assert bodyrecord.chrom == "chr7"
    assert bodyrecord.ref == "A"
    assert bodyrecord.alt == "C"
    assert bodyrecord.qual == "."
    assert bodyrecord.info == "AF=0.1;Uncertain_significance"
    assert bodyrecord.filter == "filter=cancer;cancer;SO:0001583|missense_variant;AF=0.1"

