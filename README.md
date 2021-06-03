# vcfwiper
[![Build status](https://ci.appveyor.com/api/projects/status/y09medho67x2nrgn?svg=true)](https://ci.appveyor.com/project/mazzalab/fastqwiper)
[![GitHub issues](https://img.shields.io/github/issues-raw/mazzalab/vcfwiper)](https://github.com/mazzalab/fastqwiper/issues)

`VcfWiper` is a Python application that fixes VCF sequencing files
d reads from readable FASTQ files. 

* Compatibility: Python <=3.9
* OS: Windows, Linux, Mac OS
* Contributions: [bioinformatics@css-mendel.it](bioinformatics@css-mendel.it)
* Pypi: https://pypi.org/project/vcfwiper
* Conda: https://anaconda.org/bfxcss/vcfwiper
* Docker Hub: available soon
* Bug report: [https://github.com/mazzalab/vcfwiper/issues](https://github.com/mazzalab/vcfwiper/issues)


## Installation
`VcfWiper` can be installed using both Conda and PyPi and runs smoothly on all OS specified above.

### Anaconda or Miniconda
[![Anaconda-Server Badge](https://anaconda.org/bfxcss/fastqwiper/badges/version.svg)](https://anaconda.org/bfxcss/fastqwiper) [![Anaconda-Server Badge](https://anaconda.org/bfxcss/fastqwiper/badges/latest_release_date.svg)](https://anaconda.org/bfxcss/fastqwiper) [![Anaconda-Server Badge](https://anaconda.org/bfxcss/fastqwiper/badges/platforms.svg)](https://anaconda.org/bfxcss/fastqwiper) [![Anaconda-Server Badge](https://anaconda.org/bfxcss/vcfwiper/badges/downloads.svg)](https://anaconda.org/bfxcss/vcfwiper)

Create and activate an empty Conda environment, if not already available.<br/>
```
$ conda create -n VcfWiper python=3.9
$ conda activate VcfWiper
```

then<br/>
`$ conda install -y -c bfxcss -c conda-forge vcfwiper`

### Pypi
[![PyPI version](https://badge.fury.io/py/vcfwiper.svg)](https://pypi.org/project/vcfwiper/)

`pip install vcfwiper`

### Usage
`vcfwiper` `<options>`
```
options:
  --vcf_in TEXT          The input VCF file to be fixed    [required]
  --vcf_out TEXT         The wiped VCF file                [required]
```
It accepts in input `*.vcf` files.

# Author
**Tommaso Mazza**  
[![Tweeting](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/irongraft)

Laboratory of Bioinformatics<br/>
Fondazione IRCCS Casa Sollievo della Sofferenza<br/>
Viale Regina Margherita 261 - 00198 Roma IT<br/>
Tel: +39 06 44160526 - Fax: +39 06 44160548<br/>
E-mail: t.mazza@css-mendel.it <br/>
Web page: http://www.css-mendel.it <br/>
Web page: http://bioinformatics.css-mendel.it <br/>