from flask import Flask, request, jsonify, make_response, abort
from load_models import (
    spacy_nlp,
    c2v_model,
    sym_spell_len5,
    sym_spell_len7,
    white_list_word_embeddings,
)
from white_and_black_list_words_ import white_list_words
from cython_utils.utils import get_prediction_on_multi_words, get_c2v_word_embeddings


app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_prediction():
    data = request.json

    try:
        if "ocr" in data.keys():

            # check if key entered is correct and list of words is not empty

            list_of_ocr_words = data["ocr"]
            list_predicted_words = get_prediction_on_multi_words(
                c2v_model,
                list_of_ocr_words,
                spacy_nlp,
                sym_spell_len5,
                sym_spell_len7,
                white_list_words,
                white_list_word_embeddings,
            )
            # list_predicted_words = data["ocr"]
            # print("data collected  and type ", data["ocr"], type(data["ocr"]))
            # list_predicted_words = list_predicted_words

            return jsonify(list_predicted_words)
        else:
            response = make_response(
                jsonify(message="Bad request! Missing ocr in body"), 400,
            )
            abort(response)

    except:

        # print("some exception has occured", e)
        response = make_response(
            jsonify({"status": False, "statusMessage": "Server Error"}), 500,
        )
        return jsonify(response)


if __name__ == "__main__":

    app.run(debug=True)
