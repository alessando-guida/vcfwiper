from vcf_wiper.utils import remove_commas_from_quoted_strings
from vcf_wiper.utils import can_be_float
from vcf_wiper.utils import can_be_bool
from vcf_wiper.utils import can_be_int
from vcf_wiper.utils import can_be_chr
from vcf_wiper.utils import can_be_str
import pytest


def test_remove_commas():
    out = remove_commas_from_quoted_strings('asdasdas , dasd ", asdasdasd" ,,', ",")
    assert out == 'asdasdas , dasd " asdasdasd" ,,'


def test_can_be_float():
    assert can_be_float("123") == True
    assert can_be_float("0.4") == True
    assert can_be_float("banana") == False


def test_can_be_int():
    assert can_be_int("123") == True
    assert can_be_int(123) == True
    assert can_be_int(0.4) == True


def test_can_be_chr():
    assert can_be_chr("123") == False
    assert can_be_chr(123) == False
    assert can_be_chr(1) == True
    assert can_be_chr("1") == True


def test_can_be_str():
    assert can_be_str("123") == True
    assert can_be_str(123) == True


def test_can_be_bool():
    assert can_be_bool(1) == True
    assert can_be_bool(0) == True
    assert can_be_bool(True) == True
    assert can_be_bool(False) == True
    assert can_be_bool("False") == True
    assert can_be_bool("1") == True
    assert can_be_bool("123") == False
    assert can_be_bool(123) == False