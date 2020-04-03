import string
import re

list_of_ocr_words = [
    [
        [[347, 1287, 432, 1311], "Storage", "primary"],
        [[432, 1287, 502, 1311], "Llc", "primary"],
        [[149, 1315, 201, 1339], "2235", "primary"],
    ]
]
final_output = []
final_output = []
for word in list_of_ocr_words:
    list_corrected_word = []
    for word_ in word:
        # print(word_)
        list_corrected_word.append([word_[0]])
        incorrect_word = word_[1]
        try:
            if len(incorrect_word) < 4:
                list_corrected_word.append(incorrect_word)
            elif is_number(incorrect_word):
                list_corrected_word.append(incorrect_word)
            else:
                cleaned_word = incorrect_word.translate(
                    str.maketrans("", "", string.punctuation)
                ).lower()

                list_corrected_word.append(cleaned_word)
                print("list_corrected_word", list_corrected_word)
        except:
            list_corrected_word.append(incorrect_word)

        list_corrected_word.append(word_[2])
final_output.append([list_corrected_word])
print("fina", final_output)
