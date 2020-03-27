from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
from Chars2vec import get_word_embeddings

import spacy
import timeit
from cython_utils.utils import get_word_with_probability_and_edit_distance
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
    print("lemmatize matched words syms",matched_words_syms)

    matched_words_char2vec = cosine_similar_words(
        incorrect_word_embedding, white_list_word_embeddings, white_list_words
    )
    nlp = spacy.load("en_core_web_sm")
    matched_words_char2vec_text = " ".join(matched_words_char2vec)
    nlp = nlp(matched_words_char2vec_text)
    matched_words_char2vec = [word_.lemma_ for word_ in nlp]

    print("lemmatize matched words char2vec",matched_words_char2vec)

    # finding the common words
    common_words = [word for word in matched_words_char2vec if word in matched_words_syms]
    # print("these are common words", common_words)

    try:
        # if common_words exist
        if common_words:
            start = timeit.default_timer()
            matched_word = get_word_with_probability_and_edit_distance(common_words,incorrect_word)
            end = timeit.default_timer()
            print("get_word_with_probability_and_edit_distance %s" %(end - start))
            # print("this is the common word matched " ,matched_word)
            return matched_word[2]

        else:
            start = timeit.default_timer()
            best_matched_words_syms = get_word_with_probability_and_edit_distance(
                matched_words_syms, incorrect_word
            )
            end= timeit.default_timer()
            print("get_word_with_probability_and_edit_distance %s " %(end-start))
            best_matched_words_char2vec = get_word_with_probability_and_edit_distance(
                matched_words_char2vec, incorrect_word
            )
            # best_matched_words_syms shape (edit distance, probability, word )
            print("best matched symspell word with probability and edit distance",best_matched_words_syms)
            print("best matched char2vec word with probability and edit distance",best_matched_words_char2vec)
           
            if len(best_matched_words_syms) != 0 and len(best_matched_words_char2vec) !=0 :
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

            elif len(best_matched_words_syms)!=0  and len(best_matched_words_char2vec) == 0:
                
                return best_matched_words_syms[2]

            elif len(best_matched_words_syms) == 0 and len(best_matched_words_char2vec) != 0 :
            
                return best_matched_words_char2vec[2]

            else:
                print("No matched word found !")
                return None
    except Exception as e:
        print("Some exception has occured",e)
        return None


if __name__ == "__main__":

    white_list_words = [
        "place",
        "mark",
        "invoice",
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
    incorrect_word = "1mp0rtant"
    incorrect_word_embedding = get_word_embeddings([incorrect_word])
    white_list_word_embeddings = get_word_embeddings(white_list_words)
    # start=timeit.default_timer()
    word = get_final_similar_word(
        white_list_words,
        incorrect_word,
        incorrect_word_embedding,
        white_list_word_embeddings,
    )
    # end=timeit.default_timer()
    

    # import line_profiler
    # l = line_profiler.LineProfiler()
    # l.add_function(get_final_similar_word)
    # l.run('get_final_similar_word( white_list_words,incorrect_word,incorrect_word_embedding,white_list_word_embeddings, )')
    # import cProfile
    # cProfile.run("get_final_similar_word(white_list_words, incorrect_word, incorrect_word_embedding,white_list_word_embeddings)" )
    # print("get_final_similar_word",end-start)
    print(word)
    # print(sys.path) 
    # def cfunc(int n):

