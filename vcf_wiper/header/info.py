
from vcf_wiper import log
from vcf_wiper.header.headerfield import HeaderField
from vcf_wiper.utils import remove_commas_from_quoted_strings


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
        # SETTINGS -------------------------------------------------
        self.expected_string = "##INFO="   # expected string in the header field
        self.required_fields = ["ID", "Number", "Type", "Description"]  # this must be included
        self.allowed_types = set(["Integer", "Float", "Flag", "Character", "String"])

        # Start parsing --------------------------------------------
        assert line.startswith(self.expected_string), "line expected to start with %s" % self.expected_string
        # parse info fields
        parsed = self._parse_info_line(line=line)
        # make sure the format is Ok
        for field in parsed.keys():
            assert field in set(self.required_fields), "Expected field missing in INFO header: %s" % field

        self.ID: str = parsed["ID"]
        self.number = parsed["Number"]  # can be either numeric or string
        self.type: str = parsed["Type"]
        self.description: str = parsed["Description"]

        # Assert data type -----------------------------------------
        if self.type not in self.allowed_types:
            e = "INFO header type not allowed: %s." % self.type
            log.error(e)
            raise TypeError(e)
        if self.type == "Flag":
            assert self.number == 0, "Number is expected to be =0 when Type = Flag. Found: %s" % self.number

    def __repr__(self):
        out = "ID=%s\n" % self.ID
        out += "Number=%s\n" % str(self.number)
        out += "Type=%s\n" % self.type
        out += "Description=%s\n" % self.description
        return out

    def _parse_info_line(self, line: str) -> dict:
        """parse the header line into one dictionary"""

        # remove commas found inside quoted parts of the string
        line = remove_commas_from_quoted_strings(string=line, sep=",")

        # remove expected string
        #   ##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
        # and transform into
        #   <ID=AA,Number=1,Type=String,Description="Ancestral Allele">
        line_desc = line.replace(self.expected_string, "")
        self.check_header_line_format(line_desc=line_desc)

        if line_desc.startswith("<"):
            line_desc = line_desc[1:]  # remove < at the beginning
        else:
            raise ValueError("Expected < at the betting of the string. Found: %s" % line_desc)

        if line_desc.endswith(">\n"):
            line_desc = line_desc[:-2]  # remove > at the end
        else:
            raise ValueError("Expected >\\n at the end of the string. Found: %s" % line_desc)

        # split by commas
        fields = line_desc.split(",")

        # parse to dictionary
        out = {}
        for field in fields:
            key, value = field.split("=")

            if value.isnumeric():
                out[key] = int(value)
            else:
                out[key] = value

        return out

    def validate_format(self, vcf_info_line: str):
        """Once the class has been instanciated, we can use this function to asser that
            the vcf fields are according to the standard

            vcf_info_line (str): this is the entire string to that we will find in the vcf row/colum. It contains not
                                only the value we are interested in but also all the other info fields.
                                 Example: "AA=3;DP=14;AF=0.5;BB;H2"
        """
        # parse all the info fields in the string we need to validate
        parse_dict = self.parse_to_dict(query=vcf_info_line, sep=";", assign_symbol="=")

        # find the specific info field we are interested in.
        found = False
        for i_key in parse_dict.keys():
            if i_key == self.ID:
                found = True
                log.debug("found a match: %s:%s" % (i_key, self.ID))

                if self.number == 'A':  # the field has one value per alternate allele
                    # Can have varying lengths
                    # TODO: make sure to check the length matches the ALT column
                    pass
                elif self.number == 'G':
                    # TODO:
                    pass
                elif self.number == 'R':
                    # TODO:
                    pass
                elif self.number == 0:
                    assert parse_dict[self.ID] == "", "InfoHeader %s was expected to have 0 items assigned to it." \
                        "Found: %s" % (self.ID, vcf_info_line)
                elif self.number == 1:

                    if parse_dict[self.ID] == "":
                        e = "Expected InfoHeader (%s) to have 1 value. Found an empty string instead. (%s)" % (self.ID, vcf_info_line)
                        log.error(e)
                        raise ValueError(e)

                    converted_value = self.convert_to_type(value=parse_dict[self.ID], expected=self.type)

                    # NOTE: can not use parse_dict[self.ID] because if it comes as a string like 0.4 than len == 3
                    # we need to convert it first
                    if len([converted_value]) != 1:
                        e = "InfoHeader %s length did not match expectation. Expected 1; Found: %d, (string: %s)" % (
                        self.ID, len(parse_dict[self.ID]), vcf_info_line)
                        log.error(e)
                        raise ValueError(e)


                elif self.number > 1:
                    splits = parse_dict[self.ID].split(",")
                    assert len(splits) == self.number, \
                        "Expected input line (%s) to generate %d splits for ID: %s. Found: %s" % \
                        (vcf_info_line, self.number, self.ID, ", ".join(splits))

        if not found:
            raise ValueError("Expected InfoHeader ID (%s) not found. Found: %s" % (self.ID, vcf_info_line))
