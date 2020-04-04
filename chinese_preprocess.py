import re
from typing import Any, Dict, List, Set, Tuple, Union, Optional
from tag_mspan_robert_gcn.chinese_number import *

def _remove_articles(text: str) -> str:
    regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
    return re.sub(regex, ' ', text)

def _white_space_fix(text: str) -> str:
    return ' '.join(text.split())

EXCLUDE = set(string.punctuation)
def _remove_punc(text: str) -> str:
    if not _is_number(text):
        return ''.join(ch for ch in text if ch not in EXCLUDE)
    else:
        return text

def _lower(text: str) -> str:
    return text.lower()

def _tokenize(text: str) -> List[str]:
    return re.split(" |-", text)

def _normalize_answer(text: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""

    parts = [_white_space_fix(_remove_articles(_normalize_number(_remove_punc(_lower(token)))))
             for token in _tokenize(text)]
    parts = [part for part in parts if part.strip()]
    normalized = ' '.join(parts).strip()
    return normalized

def _is_number(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False

def _normalize_number(text: str) -> str:
    if _is_number(text):
        return str(float(text))
    else:
        return text

class CHPreproc:
    ###
    @staticmethod
    def _remove_articles(text: str) -> str:
        ### articel (冠詞)
        ### 主要目的: 英文是把 a | an | the 換成空白
        return text
    @staticmethod
    def _white_space_fix(text: str) -> str:
        ### 主要目的: 處理連續的空白 換成一個空白
        return ' '.join(text.split())
    @staticmethod
    def _remove_punc(text: str) -> str:
        eng_punc = '!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~' ### string.punctuation.replace('.' , '').replace('-' , '')
        ch_punc = "！？．｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏"
        punc = eng_punc + ch_punc + '\n'
        ### 如果 '-' 用 re.sub 刪會刪到小數點; 因此分開做
        text = re.sub(r"[%s]+" %punc, "", text)
        return text.replace('-','')
    @staticmethod
    def _lower_and_white_spacing(text: str) -> str:
        def gettype(ch):
            if isNumber(ch) or ch == '.':
                return 'n' ### number whether english or chinese
            if (ord(ch) >= 97 and ord(ch) <= 122):
                return 'e' ### lower case english (assuming all english alphbat in lower cases)
            return 'c' ### chinese and words in other language

        ### englich must be lower case
        text = _lower(text)
        prev_type = ''
        tokens = [""]
        for ch in text:
            if ch == ' ':
                if prev_type != '':
                    tokens.append('')
                    prev_type = ''
                continue

            if prev_type == '':
                tokens[-1] += ch
            elif prev_type == 'c':
                tokens.append(ch)
            elif gettype(ch) == prev_type:
                tokens[-1] += ch
            else:
                tokens.append(ch)
            prev_type = gettype(ch)

        # res = ''.join([ch if isNumber(ch) or ch == '.' or ch ==' ' or   else ' '+ch+' ' for ch in text])
        # print(tokens)
        return " ".join(tokens)

def normalize_answer_zh(text: str) -> str:
    '''
        English Steps
        1. split tokens from text by (' ' | '-')
        2. for token in tokens
            _white_space_fix(_remove_articles(_normalize_number(_remove_punc(_lower(token)))))
        3. for token in tokens
                token.strip()
        4. return ' '.join(parts).strip()
        
        Chinese Steps
        remove _white_space_fix and _remove_articles currently
    '''
    # parts = [_normalize_number(CHPreproc._remove_punc(_lower(token))) for token in _tokenize(text)]
    normalized = CHPreproc._lower_and_white_spacing(text)

    #parts = [CHPreproc._remove_punc(_lower(token)) for token in _tokenize(text)]
    #parts = [part for part in parts if part.strip()]
    #normalized = ' '.join(parts).strip()
    return normalized.strip()
    # return text

if __name__ == "__main__":
    print(CHPreproc._lower_and_white_spacing(CHPreproc._remove_punc("波音747，又稱為「巨無霸客機」（Jumbo Jet）；一台要價一百億元 ($10,000,000,000)，平均每年全球產量僅11.4台．")))