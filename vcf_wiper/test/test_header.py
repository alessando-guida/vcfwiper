from vcf_wiper.header.header import Header

# Create tester header
header_lines = [
    '##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">',
    '##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">',
    '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">',
    '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">',
    '##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">',
    '##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">',
]

# create obj
header = Header()
#header.read_header(header_lines)
