class BodyLineRecord:

    def __init__(self, body_header_line: str):
        """

        Parameters
        ----------
        body_header_line: this is expected to start match the following format
        "#CHROM  POS ID  REF ALT QUAL FILTER INFO"

        """
        # FORMAT ----------------------------
        self.col_sep = "\t"  # column separator
        self.required_fields = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "INFO", "FILTER"]

        self.line_number = None  # this is the number of the line in the vcf file. Helps debugging

        # Init emtpy body fields
        self.chrom = None
        self.pos = None
        self.id = None
        self.ref = None
        self.alt = None
        self.qual = None
        self.info = None
        self.filter = None
        self.format = None  # optional
        self.extra_fields: dict = {}  # optional

        # Read in the body header format
        self.columns = self._read_body_header(body_header_line=body_header_line)

    def _read_body_header(self, body_header_line):
        if body_header_line.startswith("#"):
            body_header_line = body_header_line[1:]
        else:
            raise ValueError("body header is supposed to start with a #. Found: %s" % body_header_line)

        # split by spacer
        body_header_splits = body_header_line.split(sep=self.col_sep)
        assert len(body_header_splits) >= 8, "Body Header is expected to have 8 or more columns"

        # assert that all required columns are there
        for field in self.required_fields:
            if field not in set(body_header_splits):
                raise ValueError("Expected column not found: %s" % field)

        return body_header_splits

    def read_body_record(self, line: str, line_number):

        self.line_number = line_number

        # split line by separator
        splits = line.split(self.col_sep)
        assert len(self.columns) == len(splits), "Error in body record line: %d. Number of Columns not matching Body " \
                                                 "Header. Found: %d, Expected: %d" \
                                                 % (self.line_number, len(splits), len(self.columns))
        extra_fields = {}
        for index, col in enumerate(self.columns):

            if col == "CHROM":
                self.chrom = splits[index]
            elif col == "POS":
                self.pos = splits[index]
            elif col == "ID":
                self.id = splits[index]
            elif col == "REF":
                self.ref = splits[index]
            elif col == "ALT":
                self.alt = splits[index]
            elif col == "QUAL":
                self.qual = splits[index]
            elif col == "INFO":
                self.info = splits[index]
            elif col == "FILTER":
                self.filter = splits[index]
            elif col == "FORMAT":
                self.format = splits[index]
            else:
                self.extra_fields[col] = splits[index]

    def __repr__(self):
        out = "### BodyLineRecord ###\n"
        out += "\tCHROM: " + self.chrom + "\n"
        out += "\tPOS: " + self.pos + "\n"
        out += "\tID: " + self.id + "\n"
        out += "\tREF: " + self.ref + "\n"
        out += "\tALT: " + self.alt + "\n"
        out += "\tQUAL: " + self.qual + "\n"
        out += "\tINFO: " + self.info + "\n"
        out += "\tFILTER: " + self.filter + "\n"
        if self.format:
            out += "\tFORMAT: " + self.format + "\n"
        for key, value in self.extra_fields.items():
            out += "\t" + key + ": " + value + "\n"
        out += "\n"

        return out

    #
    # def read_line(line):
    #     read_col_definition
    #
    #     assert number
    #     of
    #     cols
    #     assert col
    #     names
    #     assert col
    #     name
    #     order
    #
    # def get_INFO()
    #     return info_field
    #
    # def get_FORMAT()
    #     return format_field