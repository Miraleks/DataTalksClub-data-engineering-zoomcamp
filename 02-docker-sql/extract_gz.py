import gzip
import shutil
from pathlib import Path

def unzip_gz_file(input_file):
    output_file = input_file.with_suffix('')
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_file
