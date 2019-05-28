import re


def join_hyphenated_words(raw_text):
    result = []
    previous_word = ''
    for raw_word in raw_text.split():
        word = previous_word + raw_word.strip()
        previous_word = ''
        if word[-1] == '-':
            previous_word = word[:-1]
            continue
        result.append(word)
    return ' '.join(result)

# remove every existence of regex formula from text
def delete_regex_from_text(regex, raw_text):
    return "".join(re.split(regex, raw_text))


def delete_square_brackets(raw_text):
    return delete_regex_from_text('\[[0-9]*\]', raw_text)


def split_by(raw_text, delimiter):
    splitted_text = raw_text.split(delimiter)
    splitted_text_with_delimiter = [text + delimiter for text in splitted_text[:-1]]
    if len(splitted_text[-1]) > 0:
        splitted_text_with_delimiter.append(splitted_text[-1])
    return splitted_text_with_delimiter


def split_list_by(raw_list, delimiter):
    result = []
    for sentence in raw_list:
        result.extend(split_by(sentence, delimiter))
    return result

#split raw text to seperate sentences
def split_to_sentences(raw_text):
    exclamatory_sentences_split = split_by(raw_text, '!')
    interrogative_sentences_split = split_list_by(exclamatory_sentences_split, '?')
    declarative_sentences_split = split_list_by(interrogative_sentences_split, '.')

    sentences_list = []
    for sentence in declarative_sentences_split:
        if sentence[0] is ' ' and sentence[1].isupper():
            sentences_list.append(sentence)
        elif len(sentences_list) > 0:
            sentences_list[-1] += sentence
    return sentences_list
