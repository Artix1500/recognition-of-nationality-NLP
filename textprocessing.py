import re

french_regex = '[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ]'
german_regex = '[a-zA-ZäöüßÄÖÜẞ]'
polish_regex = '[a-pr-uwy-zA-PR-UWY-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'
italian_regex = '[a-zA-ZàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]'
spanish_regex = '[a-zA-ZáéíñóúüÁÉÍÑÓÚÜ]'
small_letters_unicode = 'abcdefghijklmnopqrstuvwxyzàâäáąßôöóòéèëêęłïîìíçćùûúüÿńñśźżæœ'
big_letters_unicode = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÄÁĄẞÔÖÓÒÉÈËÊĘŁÏÎÌÍÇĆÙÛÚÜŸŃÑŚŹŻÆŒ'
all_letters = small_letters_unicode + big_letters_unicode


def split_to_words(rawtext):
    text = []
    buffer = ""
    for raw_word in rawtext.split():
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


def create_dictionary(words_list):
    dictionary = {}
    for word in words_list:
        dictionary[word] = dictionary.get(word, 0) + 1
    return dictionary


if __name__ == '__main__':
    from tika import parser
    pdf_path = 'data/Polish/Bojanczyk.pdf'
    pdf_text = parser.from_file(pdf_path)
    words_list = split_to_words(pdf_text['content'])
    words_dict = create_dictionary(words_list)
    for word in sorted(words_dict, key=words_dict.get, reverse=False):
        print(words_dict[word], word)
    print("Total words count:", len(words_list))

