import re

from bs4 import BeautifulSoup


class Soup:
    def __init__(self):
        pass

    def lookup_pronunciation(self, soup):
        div_results = soup.find_all("div", "NetDicHead")
        for div_result in div_results:
            b_results = div_result.find_all("b")
            for b_result in b_results:
                search_result = re.findall(r'\D+', b_result.string)
                if len(search_result) > 0:
                    return ''.join(search_result)
            else:
                continue
            break
        return None

    def lookup_accent(self, soup):
        accent_result_count = 0

        div_results = soup.find_all("div", "NetDicHead")
        for div_result in div_results:
            span_results = div_result.find_all("span")
            for span_result in span_results:
                search_result = re.findall(r'\d+', span_result.string)
                if len(search_result) > 0:
                    accent_result_count += 1
                    if accent_result_count == 1:
                        accent = int(''.join(search_result))

        if accent_result_count > 0 :
            return accent, accent_result_count
        else:
            return None

    def parse_html(self, html_doc, word, pos):
        """ Description: Parse html tree to get accent in integer and pronunciation, take the first result found.
            Return: A Tuple with - Integer Accent, String Pronunciation, String Debug Note, String Word"""

        soup = BeautifulSoup(html_doc, 'html.parser')

        pronunciation = self.lookup_pronunciation(soup)

        accent_search_result = self.lookup_accent(soup)
        if accent_search_result:
            debug_line = self.check_accent_result(word, accent_search_result[1])
            if pronunciation:
                return accent_search_result[0], pronunciation, debug_line
            else:
                return accent_search_result[0], '', debug_line
        else:
            return None

    def check_accent_result(self, word, accent_result_count):
        if accent_result_count > 1:
            return word + ': 請覆查字典。檢索結果多於1。共有' + str(accent_result_count) + '個檢索結果。'
        else:
            return ''
