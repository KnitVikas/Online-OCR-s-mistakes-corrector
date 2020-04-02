import re
from utils import *
import requests
import string

# filepath = "/home/trainer/Documents/Loadsure_2020-02-05/Example documents/Commercial invoices/2020-01-30/120-Murphy-Enterprises - Copy.pdf"
# filepath = "/home/trainer/Documents/Calhoun-Demo-10-01-2020/docs/ch-sample-DO-img-005.TIF"
filepath = "C:\\Users\\Vikas Bhardwaj\\Downloads\\Wct invoice # 39397 yusen.pdf"
with open(filepath, "rb") as f:
    file_ = f.read()
    ocr_result = requests.post("http://34.211.44.68:8081/ocr", files={"file": file_})
    print(ocr_result)
    if ocr_result.status_code == 200:
        output = []
        ocr_result = ocr_result.json()["ocr"]

        if filepath.endswith(".pdf"):
            output = ocr_result
        print(output)

    #     else:
    #         output.append(ocr_result)
    #     for page in output:
    #         doc_text = " ".join(i[1] for i in page)
    #         # print(f"doc_text : {doc_text}")
    # else:
    #     print("ocr down")
# print(type(doc_text))
# ocr_output = doc_text.split(" ")
# print(ocr_result)

# print(string.punctuation)

# remove_punctuation = [
#     word.translate(str.maketrans("", "", string.punctuation)).lower()
#     for word in ocr_output
#     if len(word.translate(str.maketrans("", "", string.punctuation)).lower()) > 2
# ]

# print(remove_punctuation)
# def isDigit(ch):
#     ch = ord(ch)
#     if (ch >= ord('0') and ch <= ord('9')):
#         return True
#     return False
