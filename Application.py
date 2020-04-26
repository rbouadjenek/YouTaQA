import os
import glob
from Indexer import Indexer
import hashlib
from tqdm import tqdm

def main():
    # Root
    basepath = "/Users/younesagabi/Desktop/00/13"

    # Browse all the files from root and store the paths
    files = glob.glob(basepath+'/**/*.xml', recursive=True)
    num_lines = len(files)

    # Create the indexes directory
    indexDir = os.path.join(os.getcwd(),"IndexFolder")
    indexer = Indexer(indexDir)
    
    j = 0
    print('Start processing....')
    # Iterate in the files paths list
    with tqdm(total=num_lines) as pbar:
        for f in files: #saint-austin / Brazilian
            pbar.update(1)
            j += 1
            file = f
            
            # Extract file name
            file_name = os.path.basename((os.path.splitext(file))[0])
            
            # Parse the article with the path stored in the variable file
            os.system("python WikiExtractor.py --lists "+ file)
            
            # Read the temporary text file that contains the parsed article
            wiki = open(os.getcwd()+"/tmp.txt", 'w+', encoding = 'utf-8')
            
            # The content of the article should be initialized to an empty string
            # everytime we read a new file
            content = ""
            for i, line in enumerate(wiki):
                # The first line contains the title of the article
                if i == 0:
                    article_name = line
                    section_name = line
                
                # If the line starts with #, that means it's a new section
                elif line[0] == "=":
                    hash_content = hashlib.sha512(content.encode('utf-8')).hexdigest()
                    
                    # Indexing the file
                    indexer.indexDocument(file_name, article_name , hash_content, section_name, content)

                    # Extract new section name from the line that contains it
                    section_name = (line.split("="))[1]
                    content = ""
                
                else:
                    # Every new line that doesn't start with # is part of the content
                    content += line
        
        indexer.close
    

    # Test the search method 
    query="America"
    result=indexer.search(query)
    if result.is_empty():
        print("No result found")
    else:
        # Print the first result
        print(result[0])

if __name__ == "__main__":
    main()