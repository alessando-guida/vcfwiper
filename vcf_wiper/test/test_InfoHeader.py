from vcf_wiper.header.info import InfoHeader
import pytest

# define header field by providing the matching string
testline1 = '##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">\n'
testline2 = '##INFO=<ID=BB,Number=0,Type=String,Description="Something else">\n'
testline3 = '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">\n'
testline4 = '##INFO=<ID=GG,Number=2,Type=Float,Description="Allele Frequency">\n'
testline5 = '##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">\n'
testline6 = '##INFO=<ID=AF,Number=1,Type=Float,Description="Allele Frequency">\n'

# Parse the string
AA_info = InfoHeader(line=testline1)
BB_info = InfoHeader(line=testline2)
AF_info = InfoHeader(line=testline3)
GG_info = InfoHeader(line=testline4)
H2_info = InfoHeader(line=testline5)
AF_info_float = InfoHeader(line=testline6)

# Positive tests
def test_parsing():
    assert AA_info.ID == "AA"
    assert AA_info.number == 1
    assert AA_info.type == "String"
    assert AA_info.description == '"Ancestral Allele"'


def test_flag():
    wrong_headerline = '##INFO=<ID=H2,Number=1,Type=Flag,Description="HapMap2 membership">\n'
    with pytest.raises(AssertionError, match=r".*Number is expected to be =0 when Type = Flag.*"):
        InfoHeader(line=wrong_headerline)

def test_wrong_type():
    wrong_headerline = '##INFO=<ID=H2,Number=1,Type=Wrong,Description="HapMap2 membership">\n'
    with pytest.raises(TypeError, match=r".*INFO header type not allowed: Wrong."):
        InfoHeader(line=wrong_headerline)


########################################################
# TEST VALIDATION
########################################################

# TEST NUMBER FIELD ----------------------------------------
def test_value_checking_zeros():
    BB_info.validate_format(vcf_info_line="BB;H2")


def test_value_checking_ones():
    # validate the info column in one of the vcf lines
    AA_info.validate_format(vcf_info_line="AA=3;DP=14;AF=0.5;")
    AF_info.validate_format(vcf_info_line="AA=3;DP=14;AF=0.5")
    AF_info_float.validate_format(vcf_info_line="AF=0.4")


def test_value_checking_multiple():
    # validate the info column in one of the vcf lines
    GG_info.validate_format(vcf_info_line="GG=3,2;DP=14;AF=0.5;")

    with pytest.raises(AssertionError, match=r".*Expected input line \(GG=3,2,3;DP=14;AF=0.5;\) to generate 2 splits "
                                             r"for ID: GG. Found: 3, 2, 3.*"):
        GG_info.validate_format(vcf_info_line="GG=3,2,3;DP=14;AF=0.5;")


def test_value_A():
    AF_info.validate_format(vcf_info_line="AF;H2")
    AF_info.validate_format(vcf_info_line="AF=1")
    AF_info.validate_format(vcf_info_line="AF=1,2;BB")

def test_value_R():
    pass

def test_value_G():
    pass

def test_value_checking_mixed():
    # add mix string, with assigned value and not
    body_str_to_validate = "AA=3;DP=14;AF=0.5;BB;H2"
    AA_info.validate_format(vcf_info_line=body_str_to_validate)
    BB_info.validate_format(vcf_info_line=body_str_to_validate)


def test_expected_value_length():

    # BB should not have any value assigned here
    with pytest.raises(AssertionError, match=r".*InfoHeader BB was expected to have 0 items assigned to it.*"):
        BB_info.validate_format(vcf_info_line="BB=12;H2")

    # AA should not have 1 value assigned here
    with pytest.raises(ValueError,
                       match=r".*Expected InfoHeader \(AA\) to have 1 value. Found an empty string .*"):
        AA_info.validate_format(vcf_info_line="AA;H2")


def test_missing_key():
    with pytest.raises(ValueError, match=r"Expected InfoHeader ID \(AA\) not found. Found: BB=12;H2.*"):
        AA_info.validate_format(vcf_info_line="BB=12;H2")


def test_convert_to_type():
    assert AA_info.convert_to_type(value="0.4", expected="String") == "0.4"
    assert AA_info.convert_to_type(value="0.4", expected="Float") == 0.4
    assert AA_info.convert_to_type(value="4", expected="Integer") == 4

    with pytest.raises(ValueError, match=r"Incorrect Expected type, cannot convert value \(4\).*"):
        AA_info.convert_to_type(value="4", expected="Int")
