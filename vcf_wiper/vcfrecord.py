import os
import codecs
from vcf_wiper.header.header import Header
from vcf_wiper.body import BodyLineRecord
from vcf_wiper import log

class VcfRecord:

    def __init__(self):
        self.file_path = None

        self.header_lines = []
        self.body_header_line = []
        self.body_lines = []

    def read_vcf(self, file_path) -> None:
        """find, from the vcf file the three tuypes of lines:

        * Lines starting with ## are the Header lines
        * The Line starting with # is the Body Header line (there should be only one)
        * The line with no # is the main body record line
        """
        # open the vcf file ---------------------------------------------
        if os.path.exists(file_path) and os.path.isfile(file_path):
            vcf_file_handler = codecs.open(file_path, encoding='utf-8', errors='ignore')
        else:
            raise FileNotFoundError("file_path: %s" % file_path)
        self.file_path = file_path

        # parse the lines ---------
        for line in vcf_file_handler:
            if line.startswith("##"):
                self.header_lines.append(line)
            elif line.startswith("#"):
                self.body_header_line.append(line)
            else:
                self.body_lines.append(line)

        assert len(self.body_header_line) == 1, "We expected to find only line starting with only a # to define " \
                                                "the column headers"

    def __repr__(self):
        out = "--- Stats ---\n"
        out += "\tHeader lines: %d \n" % len(self.header_lines)
        out += "\tBody lines: %d \n" % len(self.body_lines)

        return out

    def validate(self, verbose=False):
        log.info("validating file: %s" % self.file_path)
        header = Header()
        header.read_header(lines=self.header_lines)

        # NOTE: this might not actually be correct in case there are empty lines.
        first_body_line_number = len(self.body_header_line) + len(self.header_lines) + 1

        for index, line in enumerate(self.body_lines):
            line_number = index + first_body_line_number
            log.info("body line: %d (with header: %d)" % (index, line_number))

            if self.body_lines == "" or self.body_lines == "\n":
                raise ValueError("Line is empty: %d" % line_number)

            # define body reading the body header line
            bodyrecord = BodyLineRecord(self.body_header_line[0])
            # read in the body line
            bodyrecord.read_body_line(line, line_number=line_number)

            # Verify that the body is written according to the header specifications
            try:
                header.validate(bodyrecord)
            except Exception as e:
                log.error(e)
                if verbose:
                    print("Line Numeber: %d" % line_number)
                    print(bodyrecord)


