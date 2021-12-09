""""
File description
"""

import os.path
import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from colorama import init

init(convert=True)
import re
import click
import codecs
from vcf_wiper import log

__author__ = "Tommaso Mazza"
__copyright__ = "Copyright 2021, The VcfWiper Project"
__version__ = "0.0.1"
__maintainer__ = "Tommaso Mazza"
__email__ = "bioinformatics@css-mendel.it"
__status__ = "Development"
__date__ = "03/06/2021"
__creator__ = "t.mazza"
__license__ = u"""
  Copyright (C) 2021 Tommaso Mazza <t.mazza@css-mendel.it>
  Viale Regina Margherita 261, 00198 Rome, Italy

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc.,  51 Franklin Street, Fifth Floor, Boston, MA
  02110-1301 USA
  """


def open_vcf_file(file_path: str):
    vcf_file_handler = None

    if '/' not in file_path and '\\' not in file_path:
        file_path = os.path.join(os.getcwd(), file_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        vcf_file_handler = codecs.open(file_path, encoding='utf-8', errors='ignore')
        # vcf_file_handler = open(file_path, 'rt', encoding="utf8", errors='strict')

    return vcf_file_handler


def write_vcf_file(file_path: str):
    vcf_file_handler = None

    if '/' not in file_path and '\\' not in file_path:
        parent_folder = os.getcwd()
    else:
        parent_folder = os.path.abspath(os.path.join(file_path, os.pardir))

    if os.path.isdir(parent_folder):
        vcf_file_handler = open(file_path, 'wt', encoding="utf-8")

    return vcf_file_handler


def is_float(text: str) -> bool:
    return re.search("^[0-9]+(\\.[0-9]+)?$", text)


def contains_nucleotides_ref(text: str) -> bool:
    return re.search("^([ACGTN]+$)|(^[acgtn]+$)", text)


def contains_nucleotides_alt(text: str) -> bool:
    return re.search("^([ACGTN]+|\\*|<CNV>)(,([ACGTN]+|\\*|<CNV>))*$", text)


def is_info(text: str) -> bool:
    return re.search("^.+(=.+(,.+)*)?(;.+(=.+(,.+)*)?)*$", text)


def is_genotype(text: str) -> bool:
    return re.search("^([\\d|\\.]\\|[\\d|\\.])|([\\d|\\.]/[\\d|\\.])$", text)


def parse_info(text: str) -> list:
    keys: list = []
    tokens = text.split(";")
    for i in tokens:
        keys.append(i.split('=')[1])

    return keys


def wipe_vcf(vcf_in: str, vcf_out: str):
    fin = open_vcf_file(vcf_in)
    if not fin:
        m = 'The input VCF file does not exist or bad extension'
        log.error(m)
        click.echo(click.style(m, fg='red'))
        raise FileNotFoundError(m)

    m = f"Start wiping {vcf_in}"
    log.info(m)
    click.echo(click.style(m, fg='blue'))

    # Open file out stream
    fout = write_vcf_file(vcf_out)

    # region VARIABLES
    info_id: list = []
    af_in_info: bool = False
    # endregion

    line_num = 1
    for line in fin:
        line: str = line.rstrip()

        if line_num == 1 and not line.startswith("##fileformat"):
            fout.write("##fileformat=VCFv4.2\n")
        elif line.startswith("##INFO"):
            # INFO fields should be described as: first four keys are required, source and version are recommended
            temp_line = line[8:-1]  # remove "##INFO=<" suffix

            token = re.findall(r'([^=]+)=([^=]+)(?:,|$)', temp_line)
            if len(token) < 4 or not all(x[0] in ['ID', 'Number', 'Type', 'Description'] for x in token):
                click.echo(click.style(f"The INFO field must contain at least the 'ID', 'Number', 'Type', and "
                                       f"'Description' keys in the INFO header line: {line_num}", fg='red'))
            else:
                for t in token:
                    if t[0] == "ID":
                        info_id.append(t[1])
                        break

            fout.write(line+'\n')

        # Loop lines
        line_num += 1

    # Print read variables
    if 'AF' in info_id:
        af_in_info = True

    click.echo(click.style(f"INFO keys: {','.join([x for x in info_id])}", fg='blue'))

    # Close streams
    fout.close()
    fin.close()

    click.echo(click.style("Successfully terminated\n", fg='blue'))


@click.command()
@click.option("--vcf_in", required=True, help="The input VCF file")
@click.option("--vcf_out", required=True, help="The wiped VCF file")
def wipe_vcf_command(vcf_in, vcf_out):
    return wipe_vcf(vcf_in, vcf_out)


if __name__ == '__main__':
    wipe_vcf_command()
