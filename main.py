from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
from Chars2vec import get_word_embeddings
import Levenshtein
import spacy
import timeit
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import sys
char_replace_list = [
    ["0", "o", "q", "Q", "D", "a"],
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
    ["io", "10"],
]

def get_operations_on_characters(list_of_tuple_incorrect_correct_words):

    for correct_word, incorrect_word in list_of_tuple_incorrect_correct_words:
        # print('{} => {}'.format(correct_word,incorrect_word))
        list_of_operations = []
        for idx, operation in enumerate(difflib.ndiff(correct_word, incorrect_word)):
            if operation[0] == " ":
                # nothing changes at this character location
                continue

            elif operation[0] == "-":
                # print(u'Delete "{}" from position {}'.format(operation[-1],idx))
                list_of_operations.append((idx, "Delete", operation[-1]))

            elif operation[0] == "+":
                # print(u'Add "{}" to position {}'.format(operation[-1],-1))
                list_of_operations.append((idx, "Add", operation[-1]))
    return list_of_operations


def is_in_same_list(character1, character2):
    start=timeit.default_timer()
    for list_ in char_replace_list:
        if character1 in list_ and character2 in list_:
            return True
    end = timeit.default_timer()
    print("is_in_same_list",end-start)
    return False


def get_probability_of_corret_character_replacement(operations_on_characters):
    # sort the operation on the basis of index of character
    operations_sorted_index = sorted(
        operations_on_characters, key=lambda tuple_: tuple_[0]
    )
    split_at_index = [
        (index1 + 1)
        for (index1, operation1, character1), (index2, operation2, character2) in zip(
            operations_sorted_index, operations_sorted_index[1:]
        )
        if (index2 - index1) != 1
    ]
    print(split_at_index)
    list_character_to_check = []
    last_idx = 0
    for index in split_at_index:
        new_list = [tup for tup in operations_sorted_index[last_idx:] if tup[0] < index]
        print("new list", new_list)
        list_character_to_check.append(new_list)
        last_idx += len(new_list)
    list_character_to_check.append(
        [tuple_ for tuple_ in operations_sorted_index[last_idx:]]
    )
    print()
    # print("list_character_to_check",list_character_to_check)
    # s=[[(0, 'Delete', '1'), (1, 'Add', 'i')], [(10, 'Delete', '0'), (11, 'Add', 'o')], [(13, 'Delete', 'r'), (14, 'Add', 's')]]
    # list_character_length_and_boolean_values shape (length of operation on consecutive character, bool==if character found in char list )
    if len(list_character_to_check) == 1 and len(list_character_to_check[0]) == 1:
        return 0.0
    else:
        list_character_length_and_boolean_values = []
        for list_ in list_character_to_check:
            if len(list_) == 1:
                list_character_length_and_boolean_values.append((1, False))

            else:

                first_character = ""
                second_character = ""
                for (
                    (index1, operation1, character1),
                    (index2, operation2, character2),
                ) in zip(list_, list_[1:]):
                    if operation1 == operation2:
                        if not (first_character):
                            first_character = character1 + character2

                        if (first_character) and (second_character):
                            second_character = second_character + character2

                        else:
                            print(
                                "either first_character or second_chacter are not satisfying the condition when operations are equal"
                            )
                    else:
                        if not (first_character):
                            first_character = character1

                        if first_character and not second_character:
                            second_character = character2

                        else:
                            print(
                                "either first_character or second_chacter are not satisfying the condition when operations are  not equal"
                            )
                # print("first_character","second_character",first_character,second_character)
                if first_character and second_character:
                    if is_in_same_list(first_character, second_character):
                        # print("replace character matched in replace_char_list")
                        list_character_length_and_boolean_values.append(
                            (len(first_character), True)
                        )
                    else:
                        # print("replace character not matched in replace_char_list ")
                        list_character_length_and_boolean_values.append(
                            (len(first_character), False)
                        )
                else:
                    print(
                        "any of first and second character to be matched in character replace list is empty"
                    )

        # print("list_character_length _and_boolean_values", list_character_length_and_boolean_values)
        if list_character_length_and_boolean_values:
            probability_of_correct_characters_updated = len(
                [
                    idx
                    for idx in list_character_length_and_boolean_values
                    if idx[1] == True
                ]
            ) / len(list_character_length_and_boolean_values)
            return probability_of_correct_characters_updated
        else:
            return 0.0


def get_word_with_probability_and_edit_distance(correct_word_list):

    list_correct_small_words = [word for word in correct_word_list if 2 < len(word) < 7]
    list_correct_long_words = [word for word in correct_word_list if len(word) >= 7]
    # shape of word_probability is [edit_distance , probability of words ,word]
    word_probability = []
    # print("list_correct_small_words",list_correct_small_words)
    # print("list_correct_long_words",list_correct_long_words)

    if list_correct_small_words:
        start = timeit.default_timer()
        best_match_small_word_edited_distance = levenshtein_distance_best_common_words(
            list_correct_small_words
        )
        end = timeit.default_timer()
        print("levenshtein_distance_best_common_words",end-start)

        # print("best_match_small_word_edited_distance",best_match_small_word_edited_distance)
        for word in best_match_small_word_edited_distance:
            if word[0] <= 2:
                start=timeit.default_timer()
                print("the wordd is aas",word)
                operations_on_characters = get_operations_on_characters(
                    [(incorrect_word, word[1])]
                )
                end=timeit.default_timer()
                print("get_operations_on_characters",end-start)
                start=timeit.default_timer()
                probability = get_probability_of_corret_character_replacement(
                    operations_on_characters
                )
                end=timeit.default_timer()
                print("get_probability_of_corret_character_replacement used in loop ",probability)
                word_probability.append((word[0], probability, word[1]))
            else:
                print("edit distance is much bigger for small word")
    else:
        print("No small words founds")
    if list_correct_long_words:
        best_match_long_word_edited_distance = levenshtein_distance_best_common_words(
            list_correct_long_words
        )
        # print("best_match_long_word_edited_distance",best_match_long_word_edited_distance)
        for word in best_match_long_word_edited_distance:
            if word[0] <= 4:
                print("the wordd is aas",word)
                start = timeit.default_timer()
                operations_on_characters = get_operations_on_characters(
                    [(incorrect_word, word[1])]
                )
                end=timeit.default_timer()
                print("get_operations_on_characters", end-start)
                start = timeit.default_timer()
                probability = get_probability_of_corret_character_replacement(
                    operations_on_characters
                )
                end=timeit.default_timer()
                print("get_probability_of_corret_character_replacement used in loop",end-start)
                word_probability.append((word[0], probability, word[1]))
            else:
                print("edit distance is much bigger for long word")
    else:
        print("No long words founds")

    # print("word_probability ",word_probability)
    sorted_word_probability = sorted(
        word_probability, key=lambda element: (element[0], element[1])
    )
    sorted_best_matches_list = [
        tuple_
        for tuple_ in sorted_word_probability
        if tuple_[0] == sorted_word_probability[0][0]
    ]
    # print("sorted_best_matches_list",sorted_best_matches_list)
    if sorted_best_matches_list:
        return sorted_best_matches_list[-1]
    else:
        return None


def levenshtein_distance_best_common_words(list_words):
    edit_distance_and_word = []
    incorrect_word = "1nvoice"
    sorted_list_incorrect__word_total_changes = []
    for similar_word in list_words:
        d = Levenshtein.distance(incorrect_word, similar_word)
        edit_distance_and_word.append((d, similar_word))

    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes = sorted(
        edit_distance_and_word, key=lambda i: i[0]
    )
    sorted_list_incorrect__word_total_changes = [ word for word in sorted_list_incorrect__word_total_changes if word[0] == sorted_list_incorrect__word_total_changes[0][0]]
    return sorted_list_incorrect__word_total_changes


def get_final_similar_word(
    white_list_words,
    incorrect_word,
    incorrect_word_embedding,
    white_list_word_embeddings,
):

    matched_words_syms = symspell_matched_word(incorrect_word)
    # print("matched_words_syms",matched_words_syms)
    nlp = spacy.load("en_core_web_sm")
    matched_words_syms_text = " ".join(matched_words_syms)
    nlp = nlp(matched_words_syms_text)
    # lemmatized the matched words
    matched_words_syms = [word_.lemma_ for word_ in nlp]
    # print("lemmatize matched words syms",matched_words_syms)

    matched_words_char2vec = cosine_similar_words(
        incorrect_word_embedding, white_list_word_embeddings, white_list_words
    )
    nlp = spacy.load("en_core_web_sm")
    matched_words_char2vec_text = " ".join(matched_words_char2vec)
    nlp = nlp(matched_words_char2vec_text)
    matched_words_char2vec = [word_.lemma_ for word_ in nlp]

    # print("lemmatize matched words char2vec",matched_words_char2vec)

    # finding the common words
    common_words = [word for word in matched_words_char2vec if word in matched_words_syms]
    # print("these are common words", common_words)

    try:
        # if common_words exist
        if common_words:
            start = timeit.default_timer()
            matched_word = get_word_with_probability_and_edit_distance(common_words)
            end = timeit.default_timer()
            print("get_word_with_probability_and_edit_distance", end - start)
            # print("this is the common word matched " ,matched_word)
            return matched_word[2]

        else:

            best_matched_words_syms = get_word_with_probability_and_edit_distance(
                matched_words_syms
            )
            best_matched_words_char2vec = get_word_with_probability_and_edit_distance(
                matched_words_char2vec
            )
            # best_matched_words_syms shape (edit distance, probability, word )
            # print("best matched symspell word with probability and edit distance",best_matched_words_syms)
            # print("best matched char2vec word with probability and edit distance",best_matched_words_char2vec)

            if best_matched_words_syms and best_matched_words_char2vec:
                best_matched_words_from_symspell_Char2vec = [
                    best_matched_words_syms,
                    best_matched_words_char2vec,
                ]
                sorted_best_matches_list = sorted(
                    best_matched_words_from_symspell_Char2vec,
                    key=lambda element: (element[0], element[1]),
                )[0]

                # print("get in ",sorted_best_matches_list)

                return sorted_best_matches_list[2]

            elif (
                best_matched_words_syms != None and best_matched_words_char2vec == None
            ):
                return best_matched_words_syms[2]

            elif (
                best_matched_words_syms == None and best_matched_words_char2vec != None
            ):
                return best_matched_words_char2vec[2]

            else:

                return None
    except:
        return None


if __name__ == "__main__":

    white_list_words = [
        "place",
        "mark",
        "part",
        "tariff",
        "quantity",
        "packages",
        "description",
        "information",
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
    incorrect_word = "1mvoice"

    incorrect_word_embedding = get_word_embeddings([incorrect_word])
    white_list_word_embeddings = get_word_embeddings(white_list_words)
    start=timeit.default_timer()
    word = get_final_similar_word(
        white_list_words,
        incorrect_word,
        incorrect_word_embedding,
        white_list_word_embeddings,
    )
    end=timeit.default_timer()
    print(end-start)

    # import line_profiler
    # l = line_profiler.LineProfiler()
    # l.add_function(get_final_similar_word)
    # l.run('get_final_similar_word( white_list_words,incorrect_word,incorrect_word_embedding,white_list_word_embeddings, )')
    # import cProfile
    # cProfile.run("get_final_similar_word (white_list_words, incorrect_word, incorrect_word_embedding,white_list_word_embeddings)" )
    # print("get_final_similar_word",end-start)
    # print(word)
    # print(sys.path) 
    # def cfunc(int n):

