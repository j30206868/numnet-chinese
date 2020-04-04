from unicodedata import numeric
import re
import string
from word2number.w2n import word_to_num

def isNumber(chinese):
    if chinese is None:
        return False
    try:
        dot_count = 0
        for ch in chinese:
            if ch != '.':
                numeric(ch)
            else:
                if dot_count > 0:
                    return False
                else:
                    dot_count += 1
            
        if [numeric(ch) for ch in chinese if ch != '.']:
            return True
    except:
        return False
def chinese2num(chinese):
    numbers = {'零':0, '一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '壹':1, '贰':2, '叁':3, '仨':3, '肆':4, '伍':5, '陆':6, '柒':7, '捌':8, '玖':9, '两':2, '廿':20, '卅':30, '卌':40, '虚':50, '圆':60, '近':70, '枯':80, '无':90}
    units = {'个':1, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000, '拾':10, '佰':100, '仟':1000}
    ### 壹、貳、參、肆、伍、陸、柒、捌、玖、拾、佰、仟、萬、億、圓、角、分、零、整
    trad_numbers = {'零':0, '一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '壹':1, '貳':2, '參':3, '肆':4, '伍':5, '陸':6, '柒':7, '捌':8, '玖':9, '兩':2, '廿':20, '卅':30, '卌':40, '虛':50, '圓':60, '近':70, '枯':80, '无':90}
    trad_units = {'個':1, '十':10, '百':100, '千':1000, '萬':10000, '億':100000000, '拾':10, '佰':100, '仟':1000}
    
    ###
    numbers.update(trad_numbers)
    units.update(trad_units)
    ###

    number, pureNumber = 0, True
    for i in range(len(chinese)):
        if chinese[i] in units or chinese[i] in ['廿', '卅', '卌', '虚', '圆', '近', '枯', '无']:
            pureNumber = False
            break
        if chinese[i] in numbers:
            number = number * 10 + numbers[chinese[i]]
    if pureNumber:
        return number
    number = 0
    for i in range(len(chinese)):
        if chinese[i] in numbers or chinese[i] == '十' and (i == 0 or  chinese[i - 1] not in numbers or chinese[i - 1] == '零'):
            base, currentUnit = 10 if chinese[i] == '十' and (i == 0 or chinese[i] == '十' and chinese[i - 1] not in numbers or chinese[i - 1] == '零') else numbers[chinese[i]], '個'
            for j in range(i + 1, len(chinese)):
                if chinese[j] in units:
                    if units[chinese[j]] >= units[currentUnit]:
                        base, currentUnit = base * units[chinese[j]], chinese[j]
            number = number + base
    return number
def get_number_from_word_zh(word, improve_number_extraction=True):
    punctuation = string.punctuation.replace('-', '')
    word = word.strip(punctuation)
    word = word.replace(",", "")
    try:
        number = word_to_num(word)
    except ValueError:
        try:
            number = int(word)
        except ValueError:
            try:
                number = float(word)
            except ValueError:
                try:
                    if isNumber(word):
                        # number = pycnnum.cn2num(word)
                        number = chinese2num(word)
                    else:
                        return None
                except ValueError:
                    if improve_number_extraction:
                        if re.match('^\d*1st$', word):  # ending in '1st'
                            number = int(word[:-2])
                        elif re.match('^\d*2nd$', word):  # ending in '2nd'
                            number = int(word[:-2])
                        elif re.match('^\d*3rd$', word):  # ending in '3rd'
                            number = int(word[:-2])
                        elif re.match('^\d+th$', word):  # ending in <digits>th
                            # Many occurrences are when referring to centuries (e.g "the *19th* century")
                            number = int(word[:-2])
                        elif len(word) > 1 and word[-2] == '0' and re.match('^\d+s$', word):
                            # Decades, e.g. "1960s".
                            # Other sequences of digits ending with s (there are 39 of these in the training
                            # set), do not seem to be arithmetically related, as they are usually proper
                            # names, like model numbers.
                            number = int(word[:-1])
                        elif len(word) > 4 and re.match('^\d+(\.?\d+)?/km[²2]$', word):
                            # per square kilometer, e.g "73/km²" or "3057.4/km2"
                            if '.' in word:
                                number = float(word[:-4])
                            else:
                                number = int(word[:-4])
                        elif len(word) > 6 and re.match('^\d+(\.?\d+)?/month$', word):
                            # per month, e.g "1050.95/month"
                            if '.' in word:
                                number = float(word[:-6])
                            else:
                                number = int(word[:-6])
                        else:
                            return None
                    else:
                        return None
    return number