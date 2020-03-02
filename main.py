from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
import re
from Chars2vec import get_word_embeddings
import Levenshtein 


# def word_with_least_change(list_of_tuple_incorrect_correct_words): 
#     list_incorrect__word_total_change=[]
#     sorted_list_incorrect__word_total_changes=[]
#     for a,b in list_of_tuple_incorrect_correct_words:     
#         # print('{} => {}'.format(a,b))  
#         diff_position=[]
        
#         for i,s in enumerate(difflib.ndiff(a, b)):
#             if s[0]==' ': 
#                 continue
#             elif s[0]=='-':
#                 # print(u'Delete "{}" from position {}'.format(s[-1],i))
#                 if i not in diff_position:
#                     diff_position.append(i)
#             elif s[0]=='+':
#                 # print(u'Add "{}" to position {}'.format(s[-1],i))
#                 if i not in diff_position:
#                     diff_position.append(i) 
#         list_incorrect__word_total_change.append((len(diff_position),b)) 
#     #get incorrect word with the number changes  
#         sorted_list_incorrect__word_total_changes=sorted(list_incorrect__word_total_change,key = lambda i: i[0])[0]
#         # word_with_small_change=sorted_list_incorrect__word_total_changes[0][1]  #get only word
#     return sorted_list_incorrect__word_total_changes
                                                                                                                                   




def get_best_match_word(not_common_words):
    list_incorrect_correct_small_words=[]
    list_incorrect_correct_long_words=[]

    # if single not_common_words
    if len(not_common_words)==1:
        return (0,not_common_words)

    #if common words presents are more then one
    
    elif len(not_common_words)>1:
            
        for idx in common_words:
            if 3<len(idx)<7:
                    list_incorrect_correct_small_words.append(idx)
                # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
            else:
                    list_incorrect_correct_long_words.append(idx)
       
        best_match_small_word=levenshtein_distance_best_word(list_incorrect_correct_small_words)
        # print("best match small word",best_match_small_word,type(best_match_small_word))
        if best_match_small_word and best_match_small_word[0]<6:
            return best_match_small_word
        else:
            pass 
        best_match_long_word=levenshtein_distance_best_word(list_incorrect_correct_long_words)
        #best match long words conditions
        print("best match long word",best_match_long_word)
        if best_match_long_word and best_match_long_word[0]<9:
            return best_match_long_word
        else:
            pass

def levenshtein_distance_best_word(list_words):
    edit_distance_and_word=[]
    sorted_list_incorrect__word_total_changes=[]
    for similar_word in list_words:
        d=Levenshtein.distance(incorrect_word,similar_word)
        edit_distance_and_word.append((d,similar_word))
    print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes=sorted(edit_distance_and_word,key = lambda i: i[0])[0]
    
    return sorted_list_incorrect__word_total_changes
  
    # Print string without punctuation 


if __name__== "__main__":
    
    white_list_words=['information', 'gjhy', 'nfmc', 'mark', 'part', 'tariff', 'quantity', 'packages', 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging', 'group', 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
    incorrect_word="informa"
    incorrect_word_embedding=get_word_embeddings([incorrect_word])
    white_list_word_embeddings=get_word_embeddings(white_list_words)

    # print("this is word_embe")
    try:
        
        matched_words_syms= symspell_matched_word(incorrect_word)
        print("matched_words_syms",matched_words_syms)
        matched_words_char2vec=cosine_similar_words(incorrect_word_embedding,white_list_word_embeddings,white_list_words)
        print("matched_words_char2vec",matched_words_char2vec)
        #finding the common words
    
        common_words=[word for word in matched_words_char2vec if word in matched_words_syms]
        # print("matched_words_syms",matched_words_syms)
        # print("matched_words_char2vec",matched_words_char2vec)
        print("this is common words",common_words)

        # if common_words exist
        if common_words:
            matched_word=get_best_match_word(common_words)
            print("matched word ",matched_word[1])
            # return common_words
        # if common words not exist
        else:
            
            best_matched_words_syms=get_best_match_word(matched_words_syms)
            print("this must print1")
            best_matched_words_char2vec=get_best_match_word(matched_words_char2vec)

            print("this must print")
            print("best_matched_words_syms",best_matched_words_syms)
            print("best_matched_words_char2vec",best_matched_words_char2vec)
            
            if best_matched_words_syms and best_matched_words_char2vec:
                if best_matched_words_syms[0] > best_matched_words_char2vec[0]:
                    print("matched word",best_matched_words_char2vec[1])
                    # return best_matched_words_char2vec[1]

                elif best_matched_words_syms[0]==best_matched_words_char2vec[0]:
                    print("matched word",best_matched_words_char2vec[1])
                    # return best_matched_words_char2vec[1]

                elif best_matched_words_syms[0] < best_matched_words_char2vec[0] :
                    print("matched word",best_matched_words_syms[1])
                    # return best_matched_words_syms[1]
            if best_matched_words_syms!=None and best_matched_words_char2vec==None:
            
                # if best_matched_words_syms[0]>best_matched_words_char2vec[0]:
                    print("matched word",best_matched_words_syms[1])
                    # return best_matched_words_char2vec[1]

            if best_matched_words_syms==None and best_matched_words_char2vec!=None:
                
                # if best_matched_words_syms[0]>best_matched_words_char2vec[0]:
                    print("matched word",best_matched_words_char2vec[1])
                    # return best_matched_words_char2vec[1]

            if  best_matched_words_char2vec==None and best_matched_words_syms==None:
                print("Nothing matched perfectly")
    except :

        pass
