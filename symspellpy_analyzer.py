from pkg_resources import resource_filename as pkg_resources_filename
from symspellpy import SymSpell, Verbosity


def symspell_matched_word(incorrect_word):
    if len(incorrect_word) < 8:
        incorrect_word = [incorrect_word]
        # The length of word prefixes used for spell checking.
        sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=5)
        dictionary_path = pkg_resources_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_word:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell.lookup(
                word, Verbosity.CLOSEST, max_edit_distance=2, transfer_casing=True
            )  # ignore_token = r"\w+\d"
            # keep the original casing
            # Avoid correcting phrases matching regex
            # display suggestion term, term frequency, and edit distance
            for suggestion in suggestions:
                # print(suggestion)
                suggested_words.append((word, suggestion))
                # print(type(suggestion))

        symspell_matched_words = []
        for idx in range(len(suggested_words)):
            # print(s[i][0],str(s[i][1]).split()[0][0:-1])
            symspell_matched_words.append(str(suggested_words[idx][1]).split()[0][0:-1])
        return symspell_matched_words
    else:
        incorrect_word = [incorrect_word]
        # The length of word prefixes used for spell checking.
        sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
        dictionary_path = pkg_resources_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        # term_index is the column of the term and count_index is the
        # column of the term frequency
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_word:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell.lookup(
                word, Verbosity.CLOSEST, max_edit_distance=3, transfer_casing=True
            )  # ignore_token = r"\w+\d"
            # keep the original casing
            # Avoid correcting phrases matching regex
            # display suggestion term, term frequency, and edit distance.
            for suggestion in suggestions:
                # print(suggestion)
                suggested_words.append((word, suggestion))
                # print(type(suggestion))

        symspell_matched_words = []
        for idx in range(len(suggested_words)):
            # print(s[i][0],str(s[i][1]).split()[0][0:-1])
            symspell_matched_words.append(str(suggested_words[idx][1]).split()[0][0:-1])
        return symspell_matched_words


# print(symspell_matched_word("1mporlanl"))
