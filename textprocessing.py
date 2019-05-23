import re
from tika import parser
from ner import properNounsOut

french_regex = '[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ]'
german_regex = '[a-zA-ZäöüßÄÖÜẞ]'
polish_regex = '[a-pr-uwy-zA-PR-UWY-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'
italian_regex = '[a-zA-ZàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]'
spanish_regex = '[a-zA-ZáéíñóúüÁÉÍÑÓÚÜ]'
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
        if len(raw_word) < 2:
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
        if re.match("^[{}]+-?[{}]*$".format(all_letters, all_letters), word):
            text.append(word)
    return text


def join_hyphenated_words(raw_text):
    result = []
    previous_word = ''
    for raw_word in raw_text.split():
        word = previous_word + raw_word
        previous_word = ''
        if word[-1] == '-':
            previous_word = word[:-1]
            continue
        result.append(word)
    return ' '.join(result)


def split_by(raw_text, delimiter):
    splitted_text = raw_text.split(delimiter)
    splitted_text_with_delimiter = [text + delimiter for text in splitted_text[:-1]]
    if len(splitted_text[-1]) > 0:
        splitted_text_with_delimiter.append(splitted_text[-1])
    return splitted_text_with_delimiter


def split_to_sentences(raw_text):
    exclamatory_sentences_split = split_by(raw_text, '!')

    interrogative_sentences_split = []
    for sentence in exclamatory_sentences_split:
        interrogative_sentences_split.extend(split_by(sentence, '?'))

    declarative_sentences_split = []
    for sentence in interrogative_sentences_split:
        declarative_sentences_split.extend(split_by(sentence, '.'))

    sentences_list = []
    for sentence in declarative_sentences_split:
        if sentence[0] is ' ' and sentence[1] in english_big_letters:
            sentences_list.append(sentence)
        elif len(sentences_list) > 0:
            sentences_list[-1] += sentence
    return sentences_list


def isAscii(char):
    return 32 <= ord(char) <= 128


def isSentenceAcceptable(sentence):
    if len(sentence) < 25:
        return False
    percent = 10
    maximal_accepted = 5
    numbers = 0
    for char in sentence:
        if not isAscii(char):
            return False
        if char.isdigit():
            numbers += 1

    accepted = numbers * 100 / len(sentence) < percent and numbers <= maximal_accepted
    # if not accepted:
    #     print("USUWAM ZDANIE: + " + sentence)
    return accepted


def delete_sentences_with_many_numbers(sentences_list):
    return [x for x in sentences_list if isSentenceAcceptable(x)]


def create_dictionary(words_list):
    dictionary = {}
    for word in words_list:
        dictionary[word] = dictionary.get(word, 0) + 1
    return dictionary


def print_sentences(sentences_list, old_number_of_sentences):
    for sentence in sentences_list:
        print("#" * 80, '\n', sentence, sep="")
    print("\nNo. sentences before: " + str(old_number_of_sentences) + ", after: " + str(len(sentences_list)))


def deleteWhitespacesOnEdges(sentences_list):
    return list(map(str.strip, sentences_list))


def NER(sentences_list):
    # for sentence in sentences_list:
    #     print(properNounsOut(sentence))
    processed_text = " ".join(sentences_list)
    words = properNounsOut(processed_text)
    return words


def delete_footers_and_headers(sentences_list):
    dic = create_dictionary(sentences_list)
    return [k for k, v in dic.items() if v < 2]


def delete_square_brackets(sentence):
    return "".join(re.split("\[[0-9]*\]", sentence))


if __name__ == '__main__':
    pdf_path = 'Polish/BlochoNalepa.pdf'
    pdf_text = parser.from_file(pdf_path)
    sentences_list = split_to_sentences(join_hyphenated_words(pdf_text['content']))
    old_number_of_sentences = len(sentences_list)
    sentences_list = delete_sentences_with_many_numbers(sentences_list)
    sentences_list = deleteWhitespacesOnEdges(sentences_list)
    sentences_list = delete_footers_and_headers(sentences_list)
    map(delete_square_brackets, sentences_list)
    words = NER(sentences_list)
    words = filter_words(words)
    print(words)
