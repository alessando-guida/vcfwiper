from vcf_wiper.header.header import Header
import pytest

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


def test_read_header():
    header.read_header(header_lines)

