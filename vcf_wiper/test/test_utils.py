from vcf_wiper.utils import remove_commas_from_quoted_strings
import pytest


def test_remove_commas():
    out = remove_commas_from_quoted_strings('asdasdas , dasd ", asdasdasd" ,,', ",")
    assert out == 'asdasdas , dasd " asdasdasd" ,,'