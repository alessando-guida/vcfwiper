from vcf_wiper import log
from vcf_wiper.header.info import InfoHeader


class Header:

    def __init__(self):
        self.infolines = []
        #self.metalines = []
        #self.formatlines = []
        #self.filterlines = []  # kind of useless
        #self.altlines = []  # needed?

    def read_header(self, lines):
        for line in lines:
            if line.startswith("##INFO"):
                self.infolines.append(InfoHeader(line=line))

        #     if line is format:
        #         self.formatlines.append(FormatHeader())
        #
        #     if line is meta:
        #         self.metalines.append(MetaHeader()

    def _validate_info(self, query):
        # for info in self.infolines:
        #     info.validate_format(query)
        #
        # assert no
        # missing
        # assert no
        # extra
        pass

    def _validate_format(self, query):
        pass

    #def validate(self, bodyrecord: BodyRecord)
        #self._validate_info(bodyrecord.get_info())
        #self._validate_format(bodyrecord.get_format())



