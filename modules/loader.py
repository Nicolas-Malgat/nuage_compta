from os import path, makedirs

import csv
import requests
import sys
import zipfile



class ComptaDataLoader:

    # def split_data(self):
    #     '''
    #     Break raw data into many files
    #     '''
        
    #     with open(RAW_LOCAL_PATH + TITLE_FILE_NAME, encoding='utf-8') as file_stream:    
    #         file_stream_reader = csv.DictReader(file_stream, delimiter='\t')
            
    #         open_files_references = {}

    #         for row in file_stream_reader:
    #             title_type = row['titleType']

    #             # Open a new file and write the header
    #             if title_type not in open_files_references:
    #                 output_file = open(CURATED_LOCAL_PATH + '{}.csv'.format(title_type), 'w', encoding='utf-8', newline='')
    #                 dictionary_writer = csv.DictWriter(output_file, fieldnames=file_stream_reader.fieldnames)
    #                 # dw.writeheader()
    #                 open_files_references[title_type] = output_file, dictionary_writer
    #             # Always write the row
    #             open_files_references[title_type][1].writerow(row)
    #         # Close all the files
    #         for output_file, _ in open_files_references.values():
    #             output_file.close()

    def ensure_data_loaded(self):
        '''
        Ensure if data are already loaded. Download if missing
        '''

        if path.exists(TXT_LOCAL_PATH) == False:
            try:
                makedirs(TXT_LOCAL_PATH)
            except OSError:
                print ("Creation of the directory %s failed" % TXT_LOCAL_PATH)
                exit(1)
            else:
                print ("Successfully created the directory %s " % TXT_LOCAL_PATH)

        if path.exists(RAW_LOCAL_PATH) == False:
            self._download_data()

        # if len(listdir(RAW_LOCAL_PATH)) == 0:
        #     self._extract_data()

        print('Les fichiers sont correctement téléchargés')


    def _download_data(self):
        '''
        Download the data from internet
        '''
        
        print('Downloading data')
        with open(RAW_LOCAL_PATH, "wb") as f:
            response = requests.get(TXT_REMOTE_PATH, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
            
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()

        print('Téléchargement terminé !')

        self._extract_data()

    def _extract_data(self):
        '''
        Extract the zip file to the hard disk
        '''

        print('Begin extracting data')
        with zipfile.ZipFile(TXT_REMOTE_PATH, 'r') as zip_ref:
            zip_ref.extractall(RAW_LOCAL_PATH)
        print('Data extract successfully')
