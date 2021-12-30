from vcf_wiper import log

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
        assert line_desc.endswith(">")

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
        assert len(query_list) > 0, "query string is empty: %s" % query
        out_dict = {}
        for item in query_list:
            if item != '':
                splitted = item.split(assign_symbol)
                if len(splitted) == 2:
                    key, value = splitted
                elif len(splitted) == 1:
                    key = splitted[0]
                    value = ""
                else:
                    raise ValueError("unexpected value")

                out_dict[key] = value
        return out_dict