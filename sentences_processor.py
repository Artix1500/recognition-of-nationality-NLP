import re
import raw_text_processor as rtproc
from tika import parser
from ner import properNounsOut

small_letters_unicode = 'abcdefghijklmnopqrstuvwxyzàâäáąßôöóòéèëêęłïîìíçćùûúüÿńñśźżæœ'
big_letters_unicode = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÄÁĄẞÔÖÓÒÉÈËÊĘŁÏÎÌÍÇĆÙÛÚÜŸŃÑŚŹŻÆŒ'
english_big_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
english_small_letters = 'abcdefghijklmnopqrstuvwxyz'
all_letters = small_letters_unicode + big_letters_unicode


def filter_words(words):
    text = []
    for raw_word in words:
        if not raw_word:
            continue
        word = raw_word.lower()
        start_index, end_index = 0, len(word)
        if word[end_index - 1] in [',', '.', ':', ';', '?', '!']:
            if end_index - start_index < 2:
                continue
            end_index -= 1
        if word[start_index] == '(':
            if end_index - start_index < 2:
                continue
            start_index += 1
        if word[end_index - 1] == ')':
            if end_index - start_index < 2:
                continue
            end_index -= 1
        word = word[start_index:end_index]
        if len(word) < 2:
            continue
        if re.match("^[{}]+-?[{}]*$".format(all_letters, all_letters), word):
            text.append(word)
    return text


def create_dictionary(raw_list):
    dictionary = {}
    for element in raw_list:
        dictionary[element] = dictionary.get(element, 0) + 1
    return dictionary


def delete_footers_and_headers(sentences_list):
    return [k for k, v in create_dictionary(sentences_list).items() if v < 2]


def sentence_statistic(sentence):
    length = len(sentence)
    non_ascii_characters = 0
    small_letters = 0
    big_letters = 0
    digits = 0
    other_ascii_characters = 0

    for char in sentence:
        if ord(char) > 127:
            non_ascii_characters += 1
        elif char.islower():
            small_letters += 1
        elif char.isupper():
            big_letters += 1
        elif char.isdigit():
            digits += 1
        else:
            other_ascii_characters += 1

    return [length, 100 * non_ascii_characters / length, 100 * small_letters / length, 100 * big_letters / length,
            100 * digits / length, 100 * other_ascii_characters / length]


def aggressive_sentence_detector(sentence):
    stat = sentence_statistic(sentence)
    if stat[0] < 25:
        return False
    if stat[2] < 50:
        return False
    if stat[3] > 10:
        return False
    if stat[4] > 5:
        return False
    if stat[5] > 30:
        return False
    return True


def references_detector(sentence):
    stat = sentence_statistic(sentence[:30])
    return stat[5] * stat[0] / 100 > 5


def sentence_verifier(sentence):
    return aggressive_sentence_detector(sentence) and not references_detector(sentence)


def select_correct_sentences(sentences_list, is_sentence_verifier):
    return [sentence for sentence in sentences_list if is_sentence_verifier(sentence)]


def print_sentences(sentences_list):
    for sentence in sentences_list:
        print("#" * 80, sentence, sep="\n")


def NER(sentences_list):
    processed_text = " ".join(sentences_list)
    words = properNounsOut(processed_text)
    return words


def print_dictionary(dic):
    for k, v in dic.items():
        print(k, v)


def process_PDF_content(text):
    text = rtproc.join_hyphenated_words(text)
    text = rtproc.delete_square_brackets(text)
    sent = rtproc.split_to_sentences(text)
    sent = select_correct_sentences(sent, sentence_verifier)
    words_without_proper_names = NER(sent)
    words = filter_words(words_without_proper_names)
    final_dict = create_dictionary(words)
    return final_dict
    # print_dictionary(final_dict)
