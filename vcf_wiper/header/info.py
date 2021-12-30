
from vcf_wiper import log
from vcf_wiper.header.headerfield import HeaderField


class InfoHeader(HeaderField):
    """
    Define a class for the info header lines.

    There can be multiple header lines in a vcf file. This class models and records one of these lines.

    Description
    ------------

    INFO fields should be described as follows (first four keys are required, source and version are recommended):

    ##INFO=<ID=ID,Number=number,Type=type,Description="description",Source="source",Version="version">

    Type:
    Possible Types for INFO fields are: Integer, Float, Flag, Character, and String.

    Number
        The Number entry is an Integer that describes the number of values that can be included with the INFO field.
        For example, if the INFO field contains a single number, then this value should be 1; if the INFO field
        describes a pair of numbers, then this value should be 2 and so on. There are also certain special characters
        used to define special cases:
        • If the field has one value per alternate allele then this value should be ‘A’.
        • If the field has one value for each possible allele (including the reference), then this value should be ‘R’.
        • If the field has one value for each possible genotype (more relevant to the FORMAT tags) then this value
        should be ‘G’.
        • If the number of possible values varies, is unknown, or is unbounded, then this value should be ‘.’.
        The ‘Flag’ type indicates that the INFO field does not contain a Value entry, and hence the Number should be
        0 in this case. The Description value must be surrounded by double-quotes. Double-quote character can be escaped
        with backslash and backslash \\. Source and Version values likewise should be surrounded by double-quotes
        and specify the annotation source (case-insensitive, e.g. “dbsnp”) and exact version (e.g. “138”), respectively
        for computational use.

    Reference
    -----------
    https://samtools.github.io/hts-specs/VCFv4.2.pdf


    """
    def __init__(self, line: str):
        """
        Define here the INFO Header Field. When we instanciate this class it verifies that
        we have the expected string to be found in the header (e.g. ##INFO) and all the
        required fields are included
        """
        self.expected_string = "##INFO="
        assert line.startswith(self.expected_string), "line expected to start with %s" % self.expected_string

        # REQUIRED FIELDS ------------------------------------------
        self.required_fields = ["ID", "Number", "Type", "Description"]

        # parse required fields
        parsed = self._build(line=line)
        self.ID: str = parsed["ID"]
        self.number: int = int(parsed["Number"])
        self.type: str = parsed["Type"]
        self.description: str = parsed["Description"]

        # TODO : assert data type
        #allowed_types = set([int, float, str, chr])
        #assert type(self.number) in allowed_types, ""


    def _build(self, line: str) -> dict:
        """parse the header line"""
        # remove expected string
        #   ##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
        # and transform into
        #   <ID=AA,Number=1,Type=String,Description="Ancestral Allele">
        line_desc = line.replace(self.expected_string, "")
        self.check_header_line_format(line_desc=line_desc)

        line_desc = line_desc[1:]  # remove < at the beginning
        line_desc = line_desc[:-1]  # remove > at the end
        fields = line_desc.split(",")  # split by ,

        out = {}
        for field in fields:
            key, value = field.split("=")
            out[key] = value

        for field in out.keys():
            assert field in set(self.required_fields), \
                "Expected field missing in INFO header: %s" % field

        return out

    def __repr__(self):
        out = "ID=%s\n" % self.ID
        out += "Number=%s\n" % str(self.number)
        out += "Type=%s\n" % self.type
        out += "Description=%s\n" % self.description
        return out

    def validate_format(self, vcf_info_line: str):
        """Once the class has been instanciated, we can use this function to asser that
            the vcf fields are according to the standard

            vcf_info_line (str): this is the entire string to that we will find in the vcf row/colum. It contains not only
                                 the value we are interested in but also all the other info fields.
        """
        # parse all the info fields in the string we need to validate
        parse_dict = self.parse_to_dict(query=vcf_info_line, sep=";", assign_symbol="=")

        # find the specific info field we are interested in.
        found = False
        for i_key in parse_dict.keys():
            if i_key == self.ID:
                found = True
                log.debug("found a match: %s:%s" % (i_key, self.ID))

                if self.number == 0:
                    assert parse_dict[self.ID] == "", "InfoHeader %s was expected to have 0 items assigned to it." \
                        "Found: %s" % (self.ID, vcf_info_line)
                elif self.number == 1:
                    assert len(parse_dict[self.ID]) == 1, "InfoHeader %s length did not match expectation. Expected 1" \
                        "; Found: %s" % (self.ID, vcf_info_line)
                elif self.number > 1:
                    raise ValueError("not ready to deal with n >1 ")

        if not found:
            raise ValueError("Expected InfoHeader ID (%s) not found. Found: %s" % (self.ID, vcf_info_line))