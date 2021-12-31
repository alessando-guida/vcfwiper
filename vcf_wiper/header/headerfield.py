class HeaderField:
    """ This is the parent class to be inherited by

    * InfoHeader
    * FormatHeader
    """

    def check_header_line_format(self, line_desc: str) -> None:
        """ make sure the format of the line is ok with the standards"""
        # <ID=AA,Number=1,Type=String,Description="Ancestral Allele">
        assert len(line_desc) > 2, "empty string %s" % line_desc
        assert line_desc.startswith("<")
        assert line_desc.endswith(">\n")

    def parse_to_dict(self, query: str, sep: str = ";", assign_symbol: str = "=") -> dict:
        """
        Parser. It expects something like this:
            "NS=3;DP=14;AF=0.5;DB;H2"

        Args
        ------
            query: str = the entire string to be parsed
            sep: str = separator of each element
            assign_symbol: str = the separator between the key and value (e.g. ":", "=")

        """

        query_list = query.split(sep)
        assert len(query_list) > 0, "the vcf field is empty: %s" % query
        out_dict = {}
        for item in query_list:
            if item != '':
                splits = item.split(assign_symbol)
                if len(splits) == 2:
                    key, value = splits
                elif len(splits) == 1:
                    key = splits[0]
                    value = ""
                else:
                    raise ValueError("unexpected value")

                out_dict[key] = value
        return out_dict
