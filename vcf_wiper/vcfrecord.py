import os
import codecs


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
