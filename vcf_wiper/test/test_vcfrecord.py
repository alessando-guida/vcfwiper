from vcf_wiper.vcfrecord import VcfRecord
from vcf_wiper import ROOT_DIR
import pytest
import os

vcf1 = VcfRecord()

# reading vcf file
vcf1.read_vcf(file_path=os.path.join(ROOT_DIR, "../data", "test_vcf_validator.vcf"))

# Test line parsing
def test_number_lines():
    assert len(vcf1.header_lines) == 4
#     assert len(vcf1.body_lines) == 3

# VALIDATION

#def test_validation():

def test_empty_line():
    vcf1.validate()

vcf1.validate(verbose=True)

