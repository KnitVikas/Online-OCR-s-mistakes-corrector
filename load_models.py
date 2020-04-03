import spacy
from white_and_black_list_words_ import white_list_words
from pkg_resources import resource_filename as pkg_resources_filename
from symspellpy import SymSpell
from chars2vec.model import load_model as load_c2v_model
from cython_utils.utils import get_c2v_word_embeddings


def initialize_models():
    spacy_nlp = spacy.load("en_core_web_sm")

    dictionary_path = pkg_resources_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )
    sym_spell_len5 = SymSpell(max_dictionary_edit_distance=3, prefix_length=5)
    # term_index is the column of the term and count_index is the column of the term frequency
    sym_spell_len5.load_dictionary(dictionary_path, term_index=0, count_index=1)

    # The length of word prefixes used for spell checking.
    sym_spell_len7 = SymSpell(max_dictionary_edit_distance=4, prefix_length=7)
    # term_index is the column of the term and count_index is the column of the term frequency
    sym_spell_len7.load_dictionary(dictionary_path, term_index=0, count_index=1)

    c2v_model = load_c2v_model("single_word_trained_model")

    return spacy_nlp, c2v_model, sym_spell_len5, sym_spell_len7


(spacy_nlp, c2v_model, sym_spell_len5, sym_spell_len7,) = initialize_models()
# print("all weights has been loaded... ")
white_list_word_embeddings = get_c2v_word_embeddings(c2v_model, white_list_words)
