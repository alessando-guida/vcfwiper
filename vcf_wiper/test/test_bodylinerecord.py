import pytest
from vcf_wiper.header.header import Header
from vcf_wiper.body import BodyLineRecord


# Create tester header
header_lines = [
    '##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">',
    '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">',
    '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">',
    '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">',
    '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">',
    '##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">'
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
    nine_cols_header = "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT"
    bodyrecord = BodyLineRecord(body_header_line=nine_cols_header)
    with pytest.raises(AssertionError,
                match=r"Error in body record line: 1. Number of Columns not matching Body Header. Found: 8, Expected: 9"):
        bodyrecord.read_body_record(line=body_line1, line_number=1)

bodyrecord = BodyLineRecord(body_header_line=body_header1)
bodyrecord.read_body_record(line=body_line1, line_number=1)

print(bodyrecord)