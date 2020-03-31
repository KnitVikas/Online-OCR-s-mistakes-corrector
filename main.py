# import sys
import spacy
from pkg_resources import resource_filename as pkg_resources_filename
from symspellpy import SymSpell
from chars2vec import load_model as load_c2v_model
from cython_utils.utils import get_word_with_probability_and_edit_distance,cosine_similar_words, get_c2v_word_embeddings,symspell_matched_word
import numpy
from flask import Flask, request, jsonify,make_response,abort
from flask_api import status
# import timeit


def get_final_similar_word(
    spacy_nlp,
    sym_spell_len5,
    sym_spell_len7,
    white_list_words,
    white_list_word_embeddings,
    incorrect_word,
    incorrect_word_embedding,
):
    matched_words_syms = symspell_matched_word(
        sym_spell_len5, sym_spell_len7, incorrect_word
    )
    # print("matched_words_syms",matched_words_syms)
    matched_words_syms_text = " ".join(matched_words_syms)
    nlp_output = spacy_nlp(matched_words_syms_text)
    # lemmatized the matched words
    matched_words_syms = [word_.lemma_ for word_ in nlp_output]
    # print("lemmatize matched words syms", matched_words_syms)

    matched_words_char2vec = cosine_similar_words(
        incorrect_word_embedding, white_list_word_embeddings, white_list_words
    )
    matched_words_char2vec_text = " ".join(matched_words_char2vec)
    nlp_output = spacy_nlp(matched_words_char2vec_text)
    matched_words_char2vec = [word_.lemma_ for word_ in nlp_output]

    # print("lemmatize matched words char2vec", matched_words_char2vec)

    # finding the common words
    common_words = [
        word for word in matched_words_char2vec if word in matched_words_syms
    ]
    # print("these are common words", common_words)

    try:
        # if common_words exist
        if common_words:
            # start = timeit.default_timer()
            matched_word = get_word_with_probability_and_edit_distance(
                common_words, incorrect_word
            )
            # end = timeit.default_timer()
            # print("get_word_with_probability_and_edit_distance %s" % (end - start))
            # print("this is the common word matched " ,matched_word)
            return matched_word[2]
        else:
            # start = timeit.default_timer()
            best_matched_words_syms = get_word_with_probability_and_edit_distance(
                matched_words_syms, incorrect_word
            )
            # end = timeit.default_timer()
            # print("get_word_with_probability_and_edit_distance %s " % (end - start))
            best_matched_words_char2vec = get_word_with_probability_and_edit_distance(
                matched_words_char2vec, incorrect_word
            )
            # best_matched_words_syms shape (edit distance, probability, word )
            # print(
            #     "best matched symspell word with probability and edit distance",
            #     best_matched_words_syms,
            # )
            # print(
            #     "best matched char2vec word with probability and edit distance",
            #     best_matched_words_char2vec,
            # )

            if (
                len(best_matched_words_syms) != 0
                and len(best_matched_words_char2vec) != 0
            ):
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
                len(best_matched_words_syms) != 0
                and len(best_matched_words_char2vec) == 0
            ):
                return best_matched_words_syms[2]
            elif (
                len(best_matched_words_syms) == 0
                and len(best_matched_words_char2vec) != 0
            ):
                return best_matched_words_char2vec[2]
            else:
                print("No matched word found!")
                return None
    except Exception as e:
        print("Some exception has occured", e)
        return None


def initialize_models():
    spacy_nlp = spacy.load("en_core_web_sm")

    dictionary_path = pkg_resources_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )
    sym_spell_len5 = SymSpell(max_dictionary_edit_distance=2, prefix_length=5)
    # term_index is the column of the term and count_index is the column of the term frequency
    sym_spell_len5.load_dictionary(dictionary_path, term_index=0, count_index=1)

    # The length of word prefixes used for spell checking.
    sym_spell_len7 = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
    # term_index is the column of the term and count_index is the column of the term frequency
    sym_spell_len7.load_dictionary(dictionary_path, term_index=0, count_index=1)

    c2v_model = load_c2v_model("eng_300")

    return spacy_nlp, c2v_model, sym_spell_len5, sym_spell_len7

def get_prediction_on_multi_words(c2v_model,list_of_ocr_words,spacy_nlp,sym_spell_len5,sym_spell_len7,white_list_words,white_list_word_embeddings):
    list_predicted_words=[]
    print("list_of_ocr_words",list_of_ocr_words)
    for incorrect_word in list_of_ocr_words:
        incorrect_word_embedding = get_c2v_word_embeddings(c2v_model, [incorrect_word])
        word = get_final_similar_word(
            spacy_nlp,
            sym_spell_len5,
            sym_spell_len7,
            white_list_words,
            white_list_word_embeddings,
            incorrect_word,
            incorrect_word_embedding,
        )
        list_predicted_words.append(word)

    return list_predicted_words





app = Flask(__name__)

@app.route('/', methods=['POST']) 
def get_prediction():
    data = request.json
    
    
    
    try:
        if data['word']:
            """ """
            list_of_ocr_words = data['word']
            list_predicted_words = get_prediction_on_multi_words(c2v_model,list_of_ocr_words,spacy_nlp,sym_spell_len5,sym_spell_len7,white_list_words,white_list_word_embeddings)
             
            return jsonify(list_predicted_words)
        else:
            response = make_response(jsonify(message="Value can't be empty!"), 400)
            abort(response)
    except:
            response = make_response(jsonify(message="Bad Request!"), 400)
            abort(response)



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
   
    spacy_nlp, c2v_model, sym_spell_len5, sym_spell_len7 = initialize_models()

    white_list_word_embeddings = get_c2v_word_embeddings(c2v_model, white_list_words)

    app.run(debug = True)
    