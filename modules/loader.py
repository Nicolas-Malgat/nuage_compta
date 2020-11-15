from random import sample
from os import path, makedirs, sep
import os
from PIL import Image
import numpy as np

import csv
from numpy.core.fromnumeric import std
import requests
import sys
import zipfile


RAW_LOCAL_PATH = os.sep.join([ '..', 'datas', 'RAW', 'alphabet-dataset' ])
if __name__ == "__main__":
    RAW_LOCAL_PATH = os.sep.join([ '..', '..', 'datas', 'RAW', 'alphabet-dataset' ])

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

    # NOTE: PAS SUR QUE CE SOIT UTILE
    ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def letter_to_int(self, letter:str):
        return self.ALPHABET.index(letter)

    def int_to_letter(self, index:int):
        return self.ALPHABET[index]
    # FIN DE NOTE

    # RECUPERATION ALEATOIRE DES LETTRES
    def create_csv(self, nb_lettre):
        # nb_lettre = int(input("Indiquer le nombre d'images à saisir pour chaque lettre"))
        
        print('Chargement des dossiers: ...', end='')
        alphabet_folders = self.__load_folders()
        print('OK')
        print('Sélection des fichiers: ... ', end='')
        list_letters = self.__list_letters(alphabet_folders, nb_lettre)
        print('OK')
        print('Chargement des images: ... ', end='')
        alphabet_data = self.__load_data_from_img(list_letters)
        print('OK')
        print('Mise en forme des données: ... ', end='')
        data, labels = self.__reconditionnement(alphabet_data)
        print('OK')
        print('Sauvegarde: ... ', end='')
        self.__sauvegarde_csv(data, labels, nb_lettre)
        print('OK')

    def __sauvegarde_csv(self, data, labels, nb_lettre):

        data = data.reshape(data.shape[0], -1)

        path = r"../datas/CURATED/"
        np.savetxt(path + str(nb_lettre) + "_data.csv", data, delimiter=",")
        np.savetxt(path + str(nb_lettre) + "_labels.csv", labels, delimiter=",")

        # print(
        #     'CSV créés:', str(nb_lettre) + "_data.csv et", str(nb_lettre)+"_labels.csv"
        # )    

    def __reconditionnement(self, alphabet):
        """ Cette fonction reçoit les images de l'alphabet sous ce format:
            [
                [ numpyArray, numpyArray, numpyArray ... ], #les A
                [ numpyArray, numpyArray, numpyArray ... ], #les B
                etc ...
            ]

            Elle renvoit deux ndArray contenant les images et les labels séparément
        """
        data = np.empty( (0, 28, 28), np.intc)
        labels = np.zeros( (0), np.intc)

        for i in range(len(alphabet)):
            for j in range(len(alphabet[i])):
                data = np.append(data, np.expand_dims(alphabet[i][j], axis=0), axis=0)
                labels = np.append(labels, i)

        return data, labels


    def __load_folders(self):
        return [
                    RAW_LOCAL_PATH+os.sep+dir 
                for dir in os.listdir(RAW_LOCAL_PATH) 
            if os.path.isdir(RAW_LOCAL_PATH+os.sep+dir)
        ]
    
    def __list_letters(self, folders, nb_letter):
        """
        Renvoie un sample d'une longueur nb_letter dans chaque dossier de folders
        """

        liste = list()

        for f in folders:
            
            if len(os.listdir(f)) < nb_letter:
                nb_sample = len(os.listdir(f))
            else:
                nb_sample = nb_letter

            # print(f,len(os.listdir(f)),nb_sample)

            liste_lettre = list()

            for letter in sample(os.listdir(f), nb_sample):
                liste_lettre.append(f + os.sep + letter)
            
            liste.append(liste_lettre)

        return liste

        # return [ 
        #         [ 
        #             f+os.sep+letter 
        #         for letter in sample(os.listdir(f), len(os.listdir(f)) if len(os.listdir(f)) >= nb_letter else nb_letter)
        #         ] 
        #     for f in folders
        # ]

    def __load_data_from_img(self, list_letters):
        """
            [
                [ str (fichier), str (fichier), str (fichier) ... ], #les A
                [ str (fichier), str (fichier), str (fichier) ... ], #les B
                etc ...
            ]
        """
        return [
            [ 
                    np.asarray(Image.open(img))
                for img in letters
            ]
            for letters in list_letters
        ]

if __name__ == "__main__":
    loader = ComptaDataLoader()
    data, labels = loader.get_alphabet_data(2)

    print(
        'data', data.shape, '\n',
        data, '\n',
        '\n',
        'labels', labels.shape, '\n',
        labels, '\n'
    )
