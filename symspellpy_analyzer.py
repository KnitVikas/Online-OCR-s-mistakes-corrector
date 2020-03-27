from symspellpy import Verbosity


def symspell_matched_word(sym_spell_len5, sym_spell_len7, incorrect_word):
    if len(incorrect_word) < 8:
        incorrect_word = [incorrect_word]

        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_word:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell_len5.lookup(
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

        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_word:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell_len7.lookup(
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
