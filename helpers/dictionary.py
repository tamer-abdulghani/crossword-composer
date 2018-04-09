from string import ascii_lowercase
import pandas as pd

class DictionaryCollection:
    def __init__(self,file):
        self.file = file
        self.all_words = []
        self.dic_len_list = dict()
        self.dic_char_list = dict()
        self.dic_index_char_length = dict()

    def load(self, grid_words):

        self.all_words = [w.strip() for w in open(self.file, "r").readlines()]
        #Load the dictionary by word's length!
        for word in grid_words:
            if word.length not in self.dic_len_list:
                newlist = list(filter(lambda x: len(x) == word.length, self.all_words))
                self.dic_len_list[word.length] = newlist
        print('Dictionary Length->WordsList Loaded!!!')

        #Load the dictionary by character!
        for letter in ascii_lowercase:
            if letter not in self.dic_char_list:
                newlist = filter(lambda x: x[0].lower() == letter, self.all_words)
                self.dic_char_list[letter] = list(newlist)
        print('Dictionary Char->WordsList Loaded!!!')

        #Load master dictionary by index, letter, and length!

        for index in range(0,12):
            for letter in ascii_lowercase:
                for word in grid_words:
                    list1 = self.dic_len_list[word.length]
                    if word.length > index:
                        newlist = list(filter(lambda x: x[index].lower() == letter ,list1 ))
                        key = str(index)+'_'+str(letter.upper()) + '_' +str(word.length)
                        self.dic_index_char_length[key] = newlist
        #for key,value in self.dic_index_char_length.items():
            #print(key,value)
        print('Dictionary Index_Char_Length Loaded!!!')

    def get_count_index_char_length(self, index,letter, length):
        return len(self.get_list_index_char_length(index,letter, length))

    def get_list_index_char_length(self,index,letter,length):
        if letter == '':
            return self.dic_len_list[length]
        else:
            key = str(index) + '_' + str(letter.upper()) + '_' + str(length)
            return self.dic_index_char_length[key]




