import getopt
import sys
from random import randint
from time import sleep
from datetime import datetime

from accent.accent_checker import AccentChecker
from nlp.tagger import PosTagger
from util.msword import DocWriter


class JapanTextAnalyzer:

    def __init__(self):
        self.japan_pos = ['連体詞', '接続詞', '助詞', '形容詞', '記号', '名詞', '接頭詞', '副詞', 'BOS/EOS', '助動詞', 'フィラー', '感動詞', '動詞']
        self.punc_post = ['記号']
        self.target_post = ['形容詞', '名詞']
        self.project_data = '/home/raylam/Dropbox/Code/JAccent/data/'
        self.default_input_filename = 'japanese_text.txt'
        self.default_output_filename = 'processed_japan_text.doc'
        self.accent_checker = AccentChecker()
        self.doc_writer = DocWriter(self.project_data, self.default_output_filename)
        self.pos_tagger = PosTagger()

    def main(self, argv):
        startTime = datetime.now()
        
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

        #===============================================================================================

        self.doc_writer.open_new_document(outputfile)

        f = open(self.project_data + inputfile, encoding='utf-8')
        text = f.read()
        f.close()

        tagged_text_tp = self.pos_tagger.parse_text(text)

        # Extract Accent - Start
        output_line = ''
        accent_note = []
        debug_note = []
        no_result_note = []

        for tagged_word in tagged_text_tp:
            # self.randomDelay()
            word = tagged_word[0]
            pos = tagged_word[1]

            if pos in self.target_post:  # Lookup dictionary
                result = self.cache_lookup(word)
                if result is None:
                    if pos == '形容詞' and (word.endswith('かっ') or word.endswith('く')):
                        result = self.accent_checker.weblio_special_search(word, pos)
                    else:
                        result = self.accent_checker.weblio_original_search(word, pos)

                if result:  # Dictionary returned something
                    accent = result[0]
                    debug_info = result[2]

                    if 'イ形容詞變化型' in debug_info:
                        accent_note.append(result[2])
                    elif debug_info != '':
                        debug_note.append(result[2])

                    output_line += self.accent_checker.get_greek_letter_as_accent(accent) + word
                else:  # Dictionary no result
                    no_result_note.append(word + " : " + pos + ", 字典查無此字。")
                    output_line += word
            else:  # Does not Lookup Dictionary
                output_line += word

            if pos in self.punc_post and (word == '。' or word == '？' or word == '?'):
                output_line += 'Ω'

        # Extract Accent - End
        return output_line, accent_note, debug_note, no_result_note

    def cache_lookup(self, word):
        if word in self.accent_checker.cache_dict:
            result = self.accent_checker.cache_dict[word]
            return result[0], result[1], result[2]
        return None

    def random_delay(self):
        sleep(randint(3, 6))


if __name__ == "__main__":
    startTime = datetime.now()

    Jp = JapanTextAnalyzer()
    Jp.accent_checker.load_cache_dict()
    Jp_result = Jp.main(sys.argv[1:])
    Jp.doc_writer.write_to_doc(Jp_result[0], Jp_result[1], Jp_result[2], Jp_result[3])
    Jp.accent_checker.save_cache_dict()

    print("Grand Finished", datetime.now() - startTime)