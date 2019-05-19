import re

french_regex = '[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ]'
german_regex = '[a-zA-ZäöüßÄÖÜẞ]'
polish_regex = '[a-pr-uwy-zA-PR-UWY-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'
italian_regex = '[a-zA-ZàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]'
spanish_regex = '[a-zA-ZáéíñóúüÁÉÍÑÓÚÜ]'
small_letters_unicode = 'abcdefghijklmnopqrstuvwxyzàâäáąßôöóòéèëêęłïîìíçćùûúüÿńñśźżæœ'
big_letters_unicode = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÄÁĄẞÔÖÓÒÉÈËÊĘŁÏÎÌÍÇĆÙÛÚÜŸŃÑŚŹŻÆŒ'
all_letters = small_letters_unicode + big_letters_unicode


def split_to_words(raw_text):
    text = []
    buffer = ""
    for raw_word in raw_text.split():
        if not raw_word:
            continue
        word = buffer + raw_word.lower()
        start_index, end_index = 0, len(word)
        buffer = ''
        if word[end_index-1] in [',', '.', ':', ';', '?', '!']:
            if end_index - start_index < 2:
                continue
            end_index -= 1
        if word[start_index] == '(':
            if end_index - start_index < 2:
                continue
            start_index += 1
        if word[end_index-1] == ')':
            if end_index - start_index < 2:
                continue
            end_index -= 1
        if word[end_index-1] == '-':
            if end_index - start_index < 2:
                continue
            buffer = word[:end_index-1]
            continue
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

    return declarative_sentences_split


def create_dictionary(words_list):
    dictionary = {}
    for word in words_list:
        dictionary[word] = dictionary.get(word, 0) + 1
    return dictionary





if __name__ == '__main__':
    from tika import parser
    pdf_path = 'data/Polish/BlochoNalepa.pdf'
    pdf_text = parser.from_file(pdf_path)
    raw_text = "Eryk się spina! Czy on taki jest? Czy to tylko ja? Ala kota ma. I ja mam Alę. Cholera! Dziś juwe?"
    sentences_list = split_to_sentences(join_hyphenated_words(pdf_text['content']))
    # sentences_list = join_hyphenated_words(pdf_text['content'])
    print(sentences_list)
    # print(sentences_list)
    for sentence in sentences_list:
        print("#"*80, '\n', sentence)

