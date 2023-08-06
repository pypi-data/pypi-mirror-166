from mlphon import PhoneticAnalyser
from ml_to_en import ml_to_en

t = ml_to_en.ml_to_en()
mlphon = PhoneticAnalyser()


def split_ipa(word_ipa):
    """
    Split ipa of word into individual ipa sounds.
    :param word_ipa: (str) ipa representation of word. Example: akai̯t̪aʋamaːja
    :return: (str) split word_ipa into constituent ipa sounds. Example: a k ai̯ t̪ a ʋ a m aː j a
    """
    ipa_split = []
    idx = 0
    for ch in word_ipa[0]:
        # Special cases for unique IPA sounds composed of mulitple characters. Example: aː, bʱ, t̪
        if ch == ' ̪ '[1] or ch == "ː":
            ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        elif ch == '̯':
            try:
                if ipa_split[idx-1] in ['u', 'i'] and ipa_split[idx-2] == 'a':
                    ipa_split[idx-2] = ipa_split[idx-2] + ipa_split[idx-1] + ch + ' '
                    ipa_split = ipa_split[:-1]
                    idx -= 1
                else:
                    ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
            except IndexError:
                ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        elif ch == "ɨ" and ipa_split[idx-1] == "r":
            ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        elif ch == "ʃ":
            if idx == 0:
                ipa_split.append(ch)
                idx += 1
            elif ipa_split[idx-1] == ' ͡ '[1]:
                ipa_split[idx-2] = ipa_split[idx-2] + ' ͡ '[1] + ch + ' '
                ipa_split = ipa_split[:-1]
                idx -= 1
        elif ch == "ʰ" or ch == "ʱ":
            if len(ipa_split[idx-1]) > 1:
                ipa_split[idx-1] = ipa_split[idx-1][:-1] + ch + ' '
            else:
                ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        else:
            ipa_split.append(ch)
            idx += 1
    for idx, ch in enumerate(ipa_split):
        if len(ch) == 1:
            ipa_split[idx] = ch + ' '
    ipa_split = ''.join(ipa_split)
    if ipa_split[-1] == " ":
        ipa_split = ipa_split[:-1]
    return ipa_split


def get_ipa(input_words):
    """
    Generate IPA pronunciation for input word(s)
    :param input_words: Malayalam word (str) or list of Malayalam words for which ipa pronounciation is to be generated
    :return: Dictionary with Malayalam word and corresponding ipa representation as the key:value pair
    """
    ipa = {}
    mlwords, word_ipa = [''], ['']
    if isinstance(input_words, str):
        mlwords[0] = ''.join(input_words.split())
    else:
        mlwords = input_words
    for word in mlwords:
        try:    # if word in the mlphon dictionary of words, get ipa pronunciation of word using mlphon
            word_ipa = mlphon.grapheme_to_phoneme(word)
        except ValueError:  # else generate ipa pronunciation of word by concatenating pronunciation of characters
            word_ipa[0] = ''.join([mlphon.grapheme_to_phoneme(letter)[0] for letter in word])
        ipa_split = split_ipa(word_ipa)
        ipa[word] = ' '.join(ipa_split.split(' '))
    return ipa
