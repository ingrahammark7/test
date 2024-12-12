import codecs
from  urllib.parse import unquote

def convert_to_ascii(input_file, output_file):
    with codecs.open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='ascii', errors='ignore') as f_out:
        for line in f_in:
            f_out.write(unquote(line))

input_file = 'in.txt'
output_file = 'out.txt'	

convert_to_ascii(input_file, output_file)
