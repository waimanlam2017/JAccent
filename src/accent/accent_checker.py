from net.dictionary_weblio import WeblioCaller
from nlp.bs import Soup
import pickle


class AccentChecker():
    def __init__(self):
        self.cache_dict = {}
        self.weblio_caller = WeblioCaller()
        self.soup = Soup()
        self.aiueo = ['あ', 'い', 'う', 'え', 'お']
        self.pickle_name = 'pickle_dict.dict'
        self.load_cache_dict()

    def special_word_checking(self, word, pos):
        # if ( 'よく' in word and '形容詞' in pos ):
        #	return ( '1', 'よく', word + ": " + pos + ', 修正的特例 - よい的過去型', 'よく' )
        # else:
        #	return None
        pass

    def weblio_special_search(self, word, pos):
        print("Special checking with " + word)
        # Checking variation with く - Second Pass - Start
        if pos == "形容詞" and word.endswith("く"):
            '''原形形容詞的重音如果是
            ◎、則重音依然是◎、若不
            是◎、則在「く」的前面兩
            個字。'''
            transformed_word = word
            none_changing_part = transformed_word[:-1]
            original_word = none_changing_part + "い"

            # Query Weblio with original Adjective
            http_result = self.weblio_caller.simple_weblio(original_word, pos)
            status = http_result[0]
            text = http_result[1]
            result = self.soup.parse_html(text, word, pos)
            # Query Weblio with original Adjective

            if result:
                original_accent = int(result[0])
                pronunciation = result[1]
                pronunciation_non_changing_part = pronunciation[:-1]

                if original_accent == 0:  # Special rule
                    vary_accent = 0
                else:  # Special rule
                    vary_accent = original_accent - 1 if original_accent > 1 else 1

                debug_line = "イ形容詞變化型-く: " + transformed_word + ", 發音: " + pronunciation_non_changing_part + "く, 聲調(按規則推斷): " + str(
                    vary_accent) + ", 原來聲調: " + str(original_accent)

                self.cache_dict[word] = [vary_accent, pronunciation, debug_line, word]
                return (vary_accent, pronunciation, debug_line, word)
            else:
                return None
        elif pos == "形容詞" and word.endswith("かっ"):  # Checking variation with かっ
            '''原形形容詞的重音如果是
            ◎、則重音在「かった」的
            前面一個字、若不是◎、則
            在「かった」的前面兩個字。'''
            transformed_word = word
            none_changing_part = transformed_word[:-2]
            original_word = none_changing_part + "い"

            # Query Weblio with original Adjective
            http_result = self.weblio_caller.simple_weblio(original_word, pos)
            status = http_result[0]
            text = http_result[1]
            result = self.soup.parse_html(text, word, pos)
            # Query Weblio with original Adjective

            if result:
                original_accent = result[0]
                pronunciation = result[1]
                pronunciation_non_changing_part = pronunciation[:-1]

                if original_accent == 0:  # Special rule
                    if pronunciation_non_changing_part[-1] in self.aiueo:  # Accent is あいうえお Special rule
                        vary_accent = str(len(pronunciation_non_changing_part) - 2)
                    else:  # Special rule
                        vary_accent = str(len(pronunciation_non_changing_part) - 1)
                else:  # Special rule
                    vary_accent = original_accent - 1 if original_accent > 1 else 1

                debug_line = "イ形容詞變化型-かった: " + transformed_word + ", 發音: " + pronunciation_non_changing_part + "かった, 聲調(估計): " + str(
                    vary_accent) + ", 原來聲調: " + str(original_accent)

                self.cache_dict[word] = [vary_accent, pronunciation, debug_line, word]
                return (vary_accent, pronunciation, debug_line, word)
            else:
                return None
        else:  # Other transformed adjective, not supported now
            return None

    def weblio_original_search(self, word, pos):
        http_result = self.weblio_caller.simple_weblio(word, pos)
        status = http_result[0]
        text = http_result[1]
        result = self.soup.parse_html(text, word, pos)
        if result:
            self.cache_dict[word] = [int(result[0]), result[1], result[2], result[3]]
            return (int(result[0]), result[1], result[2], result[3])
        else:
            return None

    def save_cache_dict(self):
        with open(self.pickle_name, 'wb') as handle:
            pickle.dump(self.cache_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_cache_dict(self):
        with open(self.pickle_name, 'rb') as handle:
            self.cache_dict = pickle.load(handle)
