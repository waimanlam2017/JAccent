from bs4 import BeautifulSoup
import re


class Soup:
    def __init__(self):
        pass

    def parse_html(self, html_doc, word, pos):
        """ Description: Parse html tree to get accent in integer and pronunciation, take the first result found.
            Return: A Tuple with - Integer Accent, String Pronunciation, String Debug Note, String Word"""

        soup = BeautifulSoup(html_doc, 'html.parser')

        # Checking the pronunciation - Start
        pronunciation_found = False
        pronunciation = ''
        div_results = soup.find_all("div", "NetDicHead")
        for result in div_results:
            if pronunciation_found:
                break
            b_results = result.find_all("b")
            for result in b_results:
                search_result = re.findall(r'\D+', result.string)
                if len(search_result) > 0:
                    pronunciation_found = True
                    pronunciation = ''.join(search_result)
                    break
        # Checking the pronunciation - End

        # Checking the accent - First Pass Start
        accent_found = False
        accent = ''
        debug_line = ''
        accent_result_count = 0
        div_results = soup.find_all("div", "NetDicHead")
        for result in div_results:
            if accent_found:
                break
            span_results = result.find_all("span")
            for result in span_results:
                search_result = re.findall(r'\d+', result.string)
                if len(search_result) > 0:
                    accent_found = True
                    accent_result_count += 1
                    accent = int(''.join(search_result))
                    debug_line = word + ": " + pos + ", 發音 : " + pronunciation + ", 聲調: " + str(accent)
                    break

        if accent_result_count > 1:
            debug_line += ". 請覆查字典。檢索結果多於1。共有" + str(accent_result_count) + "個檢索結果。"

        if accent_found:
            return (accent, pronunciation, debug_line, word)
        else:
            return None
