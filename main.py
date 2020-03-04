from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
import re
from Chars2vec import get_word_embeddings
import Levenshtein
import spacy


char_replace_list = [
    ["0", "o" "q", "Q", "D", "a"],
    ["1", "i", "I", "l", "L", "t"],
    ["3", "8", "B"],
    ["2", "z", "Z", "s"],
    ["4", "H", "k"],
    ["5", "S", "s"],
    ["6", "b", "G", "C", "d"],
    ["7", "T", "j"],
    ["9", "g", "y", "Y"],
    ["m", "rn", "m"],
    ["w", "vv"],
]


def get_operations_on_characters(list_of_tuple_incorrect_correct_words):

    for a, b in list_of_tuple_incorrect_correct_words:
        # print('{} => {}'.format(a,b))
        list_of_operations = []
        for i, s in enumerate(difflib.ndiff(a, b)):
            if s[0] == " ":
                continue

            elif s[0] == "-":
                # print(u'Delete "{}" from position {}'.format(s[-1],i))
                list_of_operations.append((i, "Delete", s[-1]))

            elif s[0] == "+":
                # print(u'Add "{}" to position {}'.format(s[-1],-1))
                list_of_operations.append((i, "Add", s[-1]))
    return list_of_operations


def function_to_check_characters_in_char_list(operation_sequence):

    if len(operation_sequence) == 1:
        return True

    elif len(operation_sequence) == 2:
        for (a, b, c), (d, e, f) in zip(operation_sequence, operation_sequence[1:]):

            if a + 1 == d and b == "Delete" and e == "Add":

                if any([c in list_chars for list_chars in char_replace_list]) and any(
                    [f in list_chars for list_chars in char_replace_list]
                ):
                    return True
                else:
                    return False

            elif a + 1 == d and b == "Add" and e == "Delete":

                if any([c in list_chars for list_chars in char_replace_list]) and any(
                    [f in list_chars for list_chars in char_replace_list]
                ):
                    return True
                else:
                    return False
            else:
                return False

    else:
        for (a, b, c), (d, e, f), (g, h, i) in zip(
            operation_sequence, operation_sequence[1:], operation_sequence[2:]
        ):

            if (
                a + 1 == d == (g - 1)
                and b == "Delete"
                and e == "Delete"
                and h == "Add"
                or b == "Add"
                and e == "Delete"
                and h == "Delete"
                or a + 1 == d == (g - 1)
                and b == "Add"
                and e == "Add"
                and h == "Delete"
                or a + 1 == d == (g - 1)
                and b == "Delete"
                and e == "Add"
                and h == "Add"
            ):

                if any(
                    ["".join([c, f]) in list_chars for list_chars in char_replace_list]
                ) and any([i in list_chars for list_chars in char_replace_list]):
                    return True

                elif any([c in list_chars for list_chars in char_replace_list]) and any(
                    ["".join([f, i]) in list_chars for list_chars in char_replace_list]
                ):
                    return True

                else:
                    return False

            elif a + 1 == d and b == "Delete" and e == "Add":

                if any([c in list_chars for list_chars in char_replace_list]) and any(
                    [f in list_chars for list_chars in char_replace_list]
                ):
                    return True
                else:
                    return False

            elif a + 1 == d and b == "Add" and e == "Delete":

                if any([c in list_chars for list_chars in char_replace_list]) and any(
                    [f in list_chars for list_chars in char_replace_list]
                ):
                    return True
                else:
                    return False
            else:
                False

        else:

            return False


def get_best_match_words_not_common(not_common_words):

    # if single not_common_words
    if len(not_common_words) == 1:
        return not_common_words[0]

    elif len(not_common_words) > 1:
        list_correct_small_words = []
        list_correct_long_words = []

        for word_ in not_common_words:
            if 3 < len(word_) < 7:
                list_correct_small_words.append(word_)
            # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
            else:
                list_correct_long_words.append(word_)
        # print("small words",list_correct_small_words)
        # print("long words",list_correct_long_words)
        try:
            best_match_small_word = levenshtein_distance_best_word(
                list_correct_small_words
            )
        except:
            best_match_small_word = None
        try:
            best_match_long_word = levenshtein_distance_best_word(
                list_correct_long_words
            )
        except:
            best_match_long_word = None
        print("best match long word are", best_match_small_word)
        print("best match small word are", best_match_long_word)
        best_matches_list = []
        sorted_best_matches_list = []

        if best_match_small_word and best_match_small_word[0] < 9:
            best_matches_list.append(best_match_small_word)

        if best_match_long_word and best_match_long_word[0] < 12:
            best_matches_list.append(best_match_long_word)

        else:
            pass

        sorted_best_matches_list = sorted(best_matches_list, key=lambda i: i[0])[0]

    return sorted_best_matches_list


def get_best_match_word(common_words):
    if len(common_words) == 1:
        return common_words[0]

    # if common words presents are more then one
    elif len(common_words) > 1:

        best_match_word = levenshtein_distance_best_common_words(common_words)
        sorted_best_matches_list_words = []
        sorted_best_matches_list = []

        if best_match_word:
            # word to return
            sorted_best_matches_list = sorted(best_match_word, key=lambda i: i[0])
            if len(sorted_best_matches_list) == 1:
                sorted_best_matches_list_words.append(sorted_best_matches_list[0][1])

            else:
                # select bestmatch
                common_edit_distance_word = [
                    idx
                    for idx in sorted_best_matches_list
                    if idx[0] == sorted_best_matches_list[0][0]
                ]
                # print("common_edit_distance_word",common_edit_distance_word)
                correct_word_containing_char_in_char_list = []

                for word in common_edit_distance_word:
                    operation_sequence = get_operations_on_characters(
                        [(incorrect_word, word[1])]
                    )
                    bool_value = function_to_check_characters_in_char_list(
                        operation_sequence
                    )

                    if bool_value == True:
                        correct_word_containing_char_in_char_list.append(
                            (word[1], bool_value)
                        )

                    else:
                        correct_word_containing_char_in_char_list.append(
                            (word[1], bool_value)
                        )

                matched_word = [
                    idx
                    for idx in correct_word_containing_char_in_char_list
                    if idx[1] == True
                ]
                sorted_best_matches_list_words.extend(matched_word)
                # print("matched word",sorted_best_matches_list_words[0][0])

            return sorted_best_matches_list_words[0][0]


def levenshtein_distance_best_word(list_words):
    edit_distance_and_word = []
    sorted_list_incorrect__word_total_changes = []
    for similar_word in list_words:
        d = Levenshtein.distance(incorrect_word, similar_word)
        edit_distance_and_word.append((d, similar_word))

    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes = sorted(
        edit_distance_and_word, key=lambda i: i[0]
    )[0]

    return sorted_list_incorrect__word_total_changes


def levenshtein_distance_best_common_words(list_words):
    edit_distance_and_word = []
    sorted_list_incorrect__word_total_changes = []
    for similar_word in list_words:
        d = Levenshtein.distance(incorrect_word, similar_word)
        edit_distance_and_word.append((d, similar_word))

    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes = sorted(
        edit_distance_and_word, key=lambda i: i[0]
    )

    return sorted_list_incorrect__word_total_changes

    # Print string without punctuation


def get_final_similar_word(
    white_list_words,
    incorrect_word,
    incorrect_word_embedding,
    white_list_word_embeddings,
):

    matched_words_syms = symspell_matched_word(incorrect_word)
    # print("matched_words_syms",matched_words_syms)
    nlp = spacy.load("en")
    matched_words_syms_text = " ".join(matched_words_syms)
    nlp = nlp(matched_words_syms_text)
    # lemmatized the matched words
    matched_words_syms = [word_.lemma_ for word_ in nlp]
    # print("matched_words_syms",matched_words_syms)

    matched_words_char2vec = cosine_similar_words(
        incorrect_word_embedding, white_list_word_embeddings, white_list_words
    )
    nlp = spacy.load("en")
    matched_words_char2vec_text = " ".join(matched_words_char2vec)
    nlp = nlp(matched_words_char2vec_text)
    matched_words_char2vec = [word_.lemma_ for word_ in nlp]

    # print("matched_words_char2vec",matched_words_char2vec)

    # finding the common words
    common_words = [
        word for word in matched_words_char2vec if word in matched_words_syms
    ]
    # print("this is common words",common_words)

    try:
        # if common_words exist
        if common_words:
            matched_word = get_best_match_word(common_words)
            # print("this is the matche one " ,matched_word)
            return matched_word
        # elif len(common_words)=22:

        #     peration_sequence_syms = get_operations_on_characters([(incorrect_word,best_matched_words_syms[1])])
        #     bool_value_symspell = function_to_check_characters_in_char_list(operation_sequence_syms)
        # # if common words not exist
        else:
            # print("this must print")

            best_matched_words_syms = get_best_match_words_not_common(
                matched_words_syms
            )
            best_matched_words_char2vec = get_best_match_words_not_common(
                matched_words_char2vec
            )
            # print("this must print")
            print("best_matched_words_syms", best_matched_words_syms)
            print("best_matched_words_char2vec", best_matched_words_char2vec)

            if best_matched_words_syms and best_matched_words_char2vec:
                if best_matched_words_syms[0] > best_matched_words_char2vec[0]:
                    return best_matched_words_char2vec[1]

                # replaced character if it is in char_list
                elif best_matched_words_syms[0] == best_matched_words_char2vec[0]:

                    operation_sequence_syms = get_operations_on_characters(
                        [(incorrect_word, best_matched_words_syms[1])]
                    )
                    bool_value_symspell = function_to_check_characters_in_char_list(
                        operation_sequence_syms
                    )

                    operation_sequence_char2vec = get_operations_on_characters(
                        [(incorrect_word, best_matched_words_char2vec[1])]
                    )
                    bool_value_char2vec = function_to_check_characters_in_char_list(
                        operation_sequence_char2vec
                    )

                    if bool_value_symspell == True and bool_value_char2vec == True:
                        return best_matched_words_char2vec[1]
                    elif bool_value_symspell == False and bool_value_char2vec == True:
                        return best_matched_words_char2vec[1]
                    elif bool_value_symspell == True and bool_value_char2vec == False:
                        return best_matched_words_syms[1]
                    else:
                        return best_matched_words_char2vec[1]

                else:
                    return best_matched_words_syms[1]

            elif (
                best_matched_words_syms != None and best_matched_words_char2vec == None
            ):
                return best_matched_words_syms[1]

            elif (
                best_matched_words_syms == None and best_matched_words_char2vec != None
            ):
                return best_matched_words_char2vec[1]

            else:

                return incorrect_word
    except:
        pass


if __name__ == "__main__":

    white_list_words = [
        "information",
        "invoice",
        "place",
        "gjhy",
        "nfmc",
        "mark",
        "part",
        "tariff",
        "quantity",
        "packages",
        "description",
        "gross",
        "class",
        "hazmat",
        "commodity",
        "package",
        "pallet",
        "value",
        "marks",
        "pieces",
        "type",
        "parties",
        "order",
        "volume",
        "weight",
        "numeric",
        "division",
        "item",
        "shipping",
        "product",
        "slip",
        "batch",
        "partial",
        "expiration",
        "unit",
        "details",
        "measurement",
        "count",
        "nature",
        "container",
        "price",
        "rate",
        "charge",
        "packaging",
        "group",
        "ordered",
        "packs",
        "goods",
        "amount",
        "hash",
        "chargeable",
        "tons",
        "total",
        "serial",
        "descending",
    ]
    incorrect_word = "plece"

    incorrect_word_embedding = get_word_embeddings([incorrect_word])
    white_list_word_embeddings = get_word_embeddings(white_list_words)

    # print("this is word_embe")
    word = get_final_similar_word(
        white_list_words,
        incorrect_word,
        incorrect_word_embedding,
        white_list_word_embeddings,
    )
    print(word)
