from tqdm import tqdm
from pathlib import Path
import os.path
import sys, getopt


def get_name(page_id):
    name = str(page_id)
    while len(name) < 8:
        name = "0" + name
    return name[0:2] + "/" + name[2:4] + "/" + name[4:6] + "/", name + ".xml"


def process(file, dest):
    print('Reading file in progress...')
    if not dest.endswith('/'):
        dest += '/'
    dest += 'wikipedia/'
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
                    repo = dest + repo
                    absolute_file = repo + file_name
                    Path(repo).mkdir(parents=True, exist_ok=True)
                    f = open(absolute_file, "w+")
                    f.write(content)
                    f.close()
                    # print(dest + get_name(page_id))
                    content = ""
                    page_id = -1
                elif read:
                    content += line


def main(argv):
    input_file = ''
    destination = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
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
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
    #process("/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/enwiki-20200401-pages-articles-multistream.xml",
    #        "/home/reda/NetBeansProjects/DeepQA/enwiki-20200401/")
