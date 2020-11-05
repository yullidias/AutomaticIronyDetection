import src.utils.constants as cns
from src.error_map import error_map

import re
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import RegexpTokenizer
from nltk import tokenize
from unicodedata import normalize
from enum import Enum

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('rslp')


URL_REGEX = r'https?:\/\/(www\.)?[0-9A-Za-z:%_\+.~#?&//=]+[^\s]{2,4}(\/[0-9A-Za-z:%_\+.~#?&//=]+)?'
WWW_REGEX = r'www\.[0-9A-Za-z:%_\+.~#?&//=]+[^\s]{2,4}(\/[0-9A-Za-z:%_\+.~#?&//=]+)?'


class Tag(Enum):
    NUMBER = ' numero '
    MONEY = ' dinheiro '
    EMAIL = ' email '
    URL = ' url '
    LAUGHS = ' risos '
    DATE = ' data '
    MARK = ' marcacao '
    HEART = ' amor '
    DEATH = ' morte '
    SAD = ' triste '
    HAPPY = ' feliz '
    HASHTAG = ' hashtag '
    RAGE = ' raiva '
    ELLIPSIS = ' reticencias '
    PLUS = ' mais '
    DIFFERENT = ' diferente '


def tag_emoticon_heart(text):
    # ref: https://unicode-table.com/pt/sets/hearts-symbols/
    return re.sub(r'\u2766|\u2767|\u2619|\u2765|\u2763|\u2661|\u2665|\u2764'
                  r'|\u27B3|\u10E6|\uD83D\uDC8C|\uD83C\uDFE9|\uD83D\uDC93'
                  r'|\uD83D\uDC94|\uD83D\uDC95|\uD83D\uDC96|\uD83D\uDC97'
                  r'|\uD83D\uDC98|\uD83D\uDC99|\uD83D\uDC9A|\uD83D\uDC9B'
                  r'|\uD83D\uDC9C|\uD83D\uDDA4|\uD83D\uDC9D|\uD83D\uDC9E'
                  r'|\u2764\uFE0F|\ud83d\uDC9B|\ud83d\uDE0D|\ud83d\udc97',
                  Tag.HEART.value, text)


def tag_emoticon_death(text):
    return re.sub(r'\u2620', Tag.DEATH.value, text)


def tag_emoticon_rage(text):
    text = re.sub(r'\uD83D\uDE21', Tag.RAGE.value, text)
    text = re.sub(r'[:=]@+', Tag.RAGE.value, text)
    text = re.sub(r'@+[:=]', Tag.RAGE.value, text)
    return text


def tag_emoticon_sad(text):
    text = re.sub(r'\u2639|\uD83D\uDE1F|\uD83D\uDE1E|\ud83d\ude2d'
                  r'|\ud83d\ude14',
                  Tag.SAD.value, text)
    text = re.sub(r'[:=]\'?[/\\]+', Tag.SAD.value, text)
    return text


def tag_emoticon_happy(text):
    text = re.sub(r'\u263A|\u263B|\uD83D\uDE00|\uD83D\uDE01|\uD83D\uDE03'
                  r'|\uD83D\uDE04|\uD83D\uDE06|\u30c4', Tag.HAPPY.value, text)
    text = re.sub(r'[:|=][\)3]+', Tag.HAPPY.value, text)
    return text


def tag_emoticon_laughs(text):
    return re.sub(r'\uD83D\uDE02', Tag.LAUGHS.value, text)


def remove_accents(words):
    return [normalize('NFKD', word)
            .encode('ASCII', 'ignore')
            .decode('ASCII') for word in words]


def tokenize_text(text):
    return tokenize.word_tokenize(text, language='portuguese')


def remove_irrelevant_punctuation(text):
    tokenize_words = RegexpTokenizer(r'\w+|\?|!|-|')
    return tokenize_words.tokenize(text)


def remover_stop_words(words):
    stop_words = remove_accents(set(stopwords.words('portuguese')))
    return [word for word in words if word not in stop_words]


def word_stemmer(words):
    stemmer = RSLPStemmer()
    return [stemmer.stem(word) for word in words]


def tag_numbers(text):
    # Date
    text = re.sub(r'\d\d, (1|2)\d\d\d( at \d\d:\d\d[a|p]m)?',
                  Tag.DATE.value, text)
    date = r'(\d\d/\d\d?(/(1|2)\d(\d\d)?)?)'
    hour = r'(\d\d?:\d\d?(:\d\d?)?)'
    text = re.sub(date + ' ' + hour, Tag.DATE.value, text)
    text = re.sub(date, Tag.DATE.value, text)
    text = re.sub(r'\d\d:\d\d', Tag.DATE.value, text)
    text = re.sub(r'((1|2)\d\d\d[-.])\d\d[-.]\d\d?', Tag.DATE.value,
                  text)  # ano mes dia
    text = re.sub(r'\d\d[-.]\d\d?([-.](1|2)\d(\d\d)?)', Tag.DATE.value,
                  text)  # dia mes ano

    # Cardinal numbers
    text = re.sub(r'[0-9]+[oa]', Tag.NUMBER.value, text)

    # Telephone
    text = re.sub(
            r'((\+)?\d{2}[- ])?(\d{2}[- ])?\d{4}[- ]\d{4}',
            Tag.NUMBER.value, text)

    # Float
    text = re.sub(r'(\+)?\d+([.,]?[0-9]+)?\s?[%]?', Tag.NUMBER.value, text)



    # Money
    text = re.sub(r'r?\$[\s]*'+Tag.NUMBER.value, Tag.NUMBER.value, text)

    return text


def tag_URL(text):
    text = re.sub(URL_REGEX, Tag.URL.value, text)
    text = re.sub(WWW_REGEX, Tag.URL.value, text)
    return text


def remove_URL(text):
    text = re.sub(URL_REGEX, ' ', text)
    text = re.sub(WWW_REGEX, ' ', text)
    return text


def tag_email(text):
    return re.sub(r'[A-za-z0-9-._]+@[A-za-z]+\.[^\s]+', Tag.EMAIL.value, text)


def tag_at(text):
    return re.sub(r'@/?\w+', Tag.MARK.value, text)


def tag_hashtag(text):
    return re.sub(r'#/?[\w\.]+', Tag.HASHTAG.value, text)


def tag_ellipsis(text):
    text = re.sub(r'(\.){2,}', Tag.ELLIPSIS.value, text)
    text = re.sub(r'\u2026', Tag.ELLIPSIS.value, text)
    return text


def tag_plus(text):
    return re.sub(r'\+', Tag.PLUS.value, text)


def add_tags_from_text(text):
    text = tag_URL(text)
    text = tag_email(text)
    text = tag_at(text)
    text = tag_hashtag(text)
    text = tag_emoticon_happy(text)
    text = tag_emoticon_sad(text)
    text = tag_emoticon_death(text)
    text = tag_emoticon_heart(text)
    text = tag_emoticon_laughs(text)
    text = tag_emoticon_rage(text)
    text = tag_numbers(text)
    text = tag_ellipsis(text)
    text = tag_plus(text)
    return text


def add_tags_from_token_text(words):
    for index in range(len(words)):
        if words[index] in ['kk', 'haha', 'rsrs', 'kaka', 'hehe']:
            words[index] = Tag.LAUGHS.value.strip()
    return words


def remove_repeat_char(text):
    """
    Ref:https://stackoverflow.com/questions/10072744/remove-repeating-characters-from-words
    """
    return re.sub(r'(.)\1+', r'\1\1', text)


def remove_feature_hashtags(text):
    return re.sub(r'#sqn|#ironia|#soquenao', ' ', text)


def remove_especial_chars(text):
    text = re.sub(r"&.*;", ' ', text)
    text = re.sub(r"[\*=\.,:;'\$_\"\(\)~\[\]&\|/\\`´\^\{\}]+", ' ', text)
    return text


def remove_repeat_two_char(text):
    return re.sub(r'(..)\1+', r'\1\1', text)


def emoticon_to_chars(text):
    text = re.sub(r'\u203c|\u203c\ufe0f', '!!', text)
    text = re.sub(r'\u2049|\u2049\ufe0f', '!?', text)
    text = re.sub(r'\u2753|\uff1f|\uff1f\u3000', '?', text)
    text = re.sub(r'\uff08', '(', text)
    text = re.sub(r'\ufe36|\uff09', ')', text)
    text = re.sub(r'\u2260', Tag.DIFFERENT.value, text)
    text = re.sub(r'\u00a8', ' ', text)  # DIAERESIS
    text = re.sub(r'\u208a', ' ', text)  # + mini emoji
    text = re.sub(r'\ufe4f', ' ', text)  # ﹏
    text = re.sub(r'\u203e', ' ', text)  # ‾
    text = re.sub(r'\u0296\u032b', ' ', text)  # ʖ̫
    text = re.sub(r'\ufe34\u27a4', ' ', text)  # ︴➤
    text = re.sub(r'\u0137', ' ', text)  # ķ
    return text


def correcting_mistakes(words):
    return [error_map[word] if word in error_map else word for word in words]


def remove_empty_srt(words):
    return [word for word in words if word not in ["", " ", "-"]]


def remove_char_beginning(words):
    return [word[1:] if word.startswith('-') else word for word in words]


def remove_char_end(words):
    return [word[:-1] if word.endswith('-') else word for word in words]


def preprocess(text, out_tokens=False):
    text = text.lower()
    text = remove_feature_hashtags(text)
    text = add_tags_from_text(text)
    text = emoticon_to_chars(text)
    text = remove_repeat_char(text)
    text = remove_repeat_two_char(text)
    text = remove_especial_chars(text)
    words = tokenize_text(text)
    words = remove_accents(words)
    words = remove_char_beginning(words)
    words = remove_char_end(words)
    words = add_tags_from_token_text(words)
    words = correcting_mistakes(words)
    words = remove_empty_srt(words)
    if cns.REMOVE_STOP_WORDS:
        words = remover_stop_words(words)
    if cns.USE_STEMMING:
        words = word_stemmer(words)

    return words if out_tokens else ' '.join(words)