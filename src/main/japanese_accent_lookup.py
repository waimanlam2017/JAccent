from random import randint
from time import sleep

from accent.accent_checker import AccentChecker
from nlp.tagger import PosTagger
from util.msword import DocWriter

import sys
import getopt

class JapanTextAnalyzer():

    def __init__(self):
        self.japan_pos = ['連体詞', '接続詞', '助詞', '形容詞', '記号', '名詞', '接頭詞', '副詞', 'BOS/EOS', '助動詞', 'フィラー', '感動詞', '動詞']
        self.punc_post = ['記号']
        self.target_post = ['形容詞', '名詞']
        self.project_data = 'C:\\Users\\01556729\\Dropbox\\Code\\JAccent\\data\\'
        self.default_input_filename = 'japanese_text.txt'
        self.default_output_filename = 'processed_japan_text.doc'
        self.accent_checker = AccentChecker()
        self.doc_writer = DocWriter(self.project_data, self.default_output_filename)
        self.pos_tagger = PosTagger()

    def main(self, argv):
        inputfile = ''
        outputfile = ''
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print ('japanese_accent_lookup.py -i <inputfile> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            print (opt, arg)
            if opt == '-h':
                print
                'test.py -i <inputfile> -o <outputfile>'
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
                
        if inputfile == '':
            print('Input file is null, setting default value"', inputfile)
            inputfile = self.default_input_filename
        if outputfile == '':
            print('Output file is null, setting default value"', outputfile)
            outputfile = self.default_output_filename
        print('Input file is "', inputfile)
        print('Output file is "', outputfile)

        self.doc_writer.doc_filename = outputfile

        # Source text file - Start
        f = open(self.project_data + inputfile, encoding='utf-8')
        text = f.read()
        f.close()
        # Source text file - End

        # MeCab Tagging Process - Start
        tagged_text_tp = self.pos_tagger.parse_text(text)
        # MeCab Tagging Process - End

        # Extract Accent - Start
        output_line = ''
        debug_note = []
        no_result_note = []
        accent_note = []
        for word in tagged_text_tp:
            # self.randomDelay()
            original_word = word[0]
            pos = word[1]

            if pos in self.target_post:  # Lookup dictionary
                if pos == "形容詞" and (original_word.endswith('かっ') or original_word.endswith('く')):
                    result = self.accent_checker.weblio_special_search(original_word, pos)
                else:
                    result = self.accent_checker.weblio_original_search(original_word, pos)

                if result:  # Dictionary returned something
                    accent = result[0]
                    debug_info = result[2]

                    if "イ形容詞變化型" in debug_info:
                        accent_note.append(result[2])
                    elif debug_info != '':
                        debug_note.append(result[2])

                    symbol_accent = self.accent_checker.getGreekLetterAsAccent(accent)

                    output_line += str(symbol_accent) + original_word
                else:  # Dictionary no result
                    no_result_note.append(original_word + " : " + pos + ", 字典查無此字。")
                    output_line += original_word
            else:  # Does not Lookup Dictionary
                output_line += original_word

            if pos in self.punc_post and (original_word == '。' or original_word == '？' or original_word == '?'):
                output_line += "Ω"

        # Extract Accent - End
        return (output_line, accent_note, debug_note, no_result_note)



    def fixed_lookup(self, word, pos):
        result = self.special_word_checking(word, pos)
        if (result is not None):
            return (result[0], result[1], result[2], result[3])

        if (word in self.cache_dict):
            result = self.cache_dict[word]
            return (result[0], result[1], result[2], result[3])

    def save_accent_cache_dict(self):
        self.accent_checker.save_cache_dict()

    def randomDelay(self):
        sleep(randint(3, 6))


if __name__ == "__main__":
    Jp = JapanTextAnalyzer()
    print(sys.argv[1:])
    result = Jp.main(sys.argv[1:])
    Jp.doc_writer.write_to_doc(result[0], result[1], result[2], result[3])
    Jp.save_accent_cache_dict()
