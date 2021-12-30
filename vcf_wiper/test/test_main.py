import vcf_wiper
from vcf_wiper import wiper
import os


print("ROOT_DIR: %s" % vcf_wiper.ROOT_DIR)

# define test vcf file
test_input = os.path.join(vcf_wiper.ROOT_DIR, "../data/VCFv4.2.vcf")
assert os.path.isfile(test_input), "File not found: %s" % test_input


wiper.wipe_vcf(vcf_in=test_input, vcf_out="deleteme.vcf")
#wiper.wipe_vcf(test_input)
