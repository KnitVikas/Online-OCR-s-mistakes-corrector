# Online-OCR-s-mistakes-corrector

when we try to find the OCR of some documents or images containing text online using tesseract or other online ocr we got some similar kind of mistakes in reading those docs.. Here is the  spell corrector which will correct those mistakes and gives you the correct  interpretations

Here we are using chars2vec and symspellPy  our two way to coorect the spell.
we can train the the chars2vec as given here : https://hackernoon.com/chars2vec-character-based-language-model-for-handling-real-world-texts-with-spelling-errors-and-a3e4053a147d

Data for trainingchars2vec could be prepared using the data_generaror_script. train the model and placed it in chars2vec directory.
Run server.py for getting prediction on wrong words.
