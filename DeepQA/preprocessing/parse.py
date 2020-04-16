# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2020. Reda Bouadjenek, Deakin University                      +
#     Email:  reda.bouadjenek@deakin.edu.au                                    +
#                                                                              +
#  Licensed under the Apache License, Version 2.0 (the "License");             +
#   you may not use this file except in compliance with the License.           +
#    You may obtain a copy of the License at:                                  +
#                                                                              +
#                 http://www.apache.org/licenses/LICENSE-2.0                   +
#                                                                              +
#    Unless required by applicable law or agreed to in writing, software       +
#    distributed under the License is distributed on an "AS IS" BASIS,         +
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  +
#    See the License for the specific language governing permissions and       +
#    limitations under the License.                                            +
#                                                                              +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import getopt
import os.path
import sys
from pathlib import Path
from tqdm import tqdm

"""
This python script aims at preprocessing the Wikipedia dump file into 
files for each wikipedia page organized hierarchically based on page ids.
"""


def get_name(page_id):
    """
    This function generates the filename and the repository where to store the filename.
    :param page_id: the wikipedia page id.
    :return: the repository where to store the file and the filename.
    """
    name = str(page_id)
    while len(name) < 9:
        name = "0" + name
    return name[0:2] + "/" + name[2:4] + "/" + name[4:7] + "/", name + ".xml"


def process(file, destination_folder):
    """
    This is the main function that processes the big wikipedia file.
    :param file: the file to process.
    :param destination_folder: the repository where to store the data.
    :return:
    """
    print('Reading file in progress...')
    if not destination_folder.endswith('/'):
        destination_folder += '/'
    destination_folder += 'wikipedia/'
    num_lines = sum(1 for line in open(file))
    print('Start processing....')
    read = False
    content = ""
    page_id = -1
    with tqdm(total=num_lines) as pbar:
        with open(file) as f:
            for line in f:
                pbar.update(1)
                if line.strip().lower().startswith('<page>'):
                    read = True
                    content += line
                    page_id = -1
                elif line.strip().lower().startswith('<id>') and line.strip().lower().endswith(
                        '</id>') and page_id == -1 and read:
                    page_id = int(line.replace('<id>', '').replace('</id>', ''))
                    content += line
                elif line.strip().lower().startswith('<redirect title='):
                    read = False
                    content = ""
                    page_id = -1
                elif line.strip().lower().startswith('</page>') and read == True:
                    content += line
                    read = False
                    # Write to file.
                    repo, file_name = get_name(page_id)
                    repo = destination_folder + repo
                    absolute_file = repo + file_name
                    Path(repo).mkdir(parents=True, exist_ok=True)
                    f = open(absolute_file, "w+")
                    f.write(content)
                    f.close()
                    content = ""
                    page_id = -1
                elif read:
                    content += line


def main(argv):
    """
    Main function that read input arguments to lunch the script. 
    :param argv: 
    :return: 
    """

    input_file = ''
    destination = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('parse.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            if not os.path.isfile(input_file):
                print(input_file + ' does not exist.')
                sys.exit(2)
        elif opt in ("-o", "--ofile"):
            destination = arg
            if not os.path.isdir(destination):
                print(destination + ' does not exist.')
                sys.exit(2)
    if input_file != '' and destination != '':
        process(input_file, destination)
    else:
        print('parse.py -i <input_file> -o <output_file>')
        sys.exit(2)


if __name__ == "__main__":
    """
    The main function.
    """
    main(sys.argv[1:])
