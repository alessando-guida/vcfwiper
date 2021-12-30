from vcf_wiper.header.info import InfoHeader
import pytest

# define header field by providing the matching string
testline1 = '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">'
testline2 = '##INFO=<ID=BB,Number=0,Type=String,Description="Something else">'

# Parse the string
AA_info = InfoHeader(line=testline1)
BB_info = InfoHeader(line=testline2)


# Positive tests
def test_parsing():
    assert AA_info.ID == "AA"
    assert AA_info.number == 1
    assert AA_info.type == "String"
    assert AA_info.description == '"Ancestral Allele"'


def test_value_checking_ones():
    # validate the info column in one of the vcf lines
    AA_info.validate_format(vcf_info_line="AA=3;DP=14;AF=0.5;")


def test_value_checking_zeros():
    BB_info.validate_format(vcf_info_line="BB;H2")


def test_value_checking_mixed():
    # add mix string, with assigned value and not
    body_str_to_validate = "AA=3;DP=14;AF=0.5;BB;H2"
    AA_info.validate_format(vcf_info_line=body_str_to_validate)
    BB_info.validate_format(vcf_info_line=body_str_to_validate)


# negative test
def test_expected_value_length():

    # BB should not have any value assigned here
    with pytest.raises(AssertionError, match=r".*InfoHeader BB was expected to have 0 items assigned to it.*"):
        BB_info.validate_format(vcf_info_line="BB=12;H2")

    # AA should not have 1 value assigned here
    with pytest.raises(AssertionError, match=r".*InfoHeader AA length did not match expectation. Expected 1.*"):
        AA_info.validate_format(vcf_info_line="AA;H2")


def test_missing_key():
    with pytest.raises(ValueError, match=r"Expected InfoHeader ID \(AA\) not found. Found: BB=12;H2.*"):
        AA_info.validate_format(vcf_info_line="BB=12;H2")