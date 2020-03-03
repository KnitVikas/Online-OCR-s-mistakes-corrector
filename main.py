from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
import re
from Chars2vec import get_word_embeddings
import Levenshtein 
import spacy



char_replace_list = [ ['0','o' 'q','Q','D','a'],
            ['1','i','I','l','L','t'],
            ['3','8','B'],
            ['2','z','Z','s'],
            ['4','H','k'],
            ['5' ,'S','s'],
            ['6','b','G','C','d'],
            ['7','T','j'],            
            ['9','g','y','Y'],['m','rn','m'],['w','vv']]


def word_with_least_change(list_Of_tuple_incorrect_correct_long_words): 
    list_incorrect__word_total_change=[]
    sorted_list_incorrect__word_total_changes=[]
    for a,b in list_Of_tuple_incorrect_correct_long_words:     
        # print('{} => {}'.format(a,b))  
        diff_position=[]
        
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ': 
                continue
            elif s[0]=='-':
                print(u'Delete "{}" from position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i)
            elif s[0]=='+':
                print(u'Add "{}" to position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i) 
        list_incorrect__word_total_change.append((len(diff_position),b)) 
    #get incorrect word with the number changes  
        sorted_list_incorrect__word_total_changes=sorted(list_incorrect__word_total_change,key = lambda i: i[0])[0]
        # word_with_small_change=sorted_list_incorrect__word_total_changes[0][1]  #get only word

    return sorted_list_incorrect__word_total_changes



# def get_best_match_words_not_common(not_common_words):

#     # if single not_common_words
#     if len(not_common_words)==1:
#         return (0,not_common_words[0])
    
#     elif len(not_common_words)>1:
#         list_correct_small_words=[]
#         list_correct_long_words=[]

#         for word_ in not_common_words:
#             if 3<len(word_)<7:
#                     list_correct_small_words.append(word_)
#                 # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
#             else:
#                     list_correct_long_words.append(word_)
#         print("small words",list_correct_small_words)
#         print("long words",list_correct_long_words)
#         best_match_small_word=word_with_least_change(list_correct_long_words)
#         best_match_long_word=word_with_least_change(list_correct_long_words)
#         print("best match long word are",best_match_small_word)
#         print("best match small word are",best_match_long_word)
#         best_matches_list=[]
#         sorted_best_matches_list=[]
        
#         if best_match_small_word and best_match_small_word[0]<6:
#             best_matches_list.append(best_match_small_word)
        
        
#         if best_match_long_word and best_match_long_word[0]<9:
#             best_matches_list.append(best_match_long_word)
        
#         else :
#             pass

#         sorted_best_matches_list=sorted(best_matches_list,key = lambda i: i[0])[0]
        
#     return sorted_best_matches_list

def get_best_match_words_not_common(not_common_words):

    # if single not_common_words
    if len(not_common_words)==1:
        return (0,not_common_words[0])
    
    elif len(not_common_words)>1:
        list_correct_small_words=[]
        list_correct_long_words=[]

        for word_ in not_common_words:
            if 3<len(word_)<7:
                    list_correct_small_words.append(word_)
                # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
            else:
                    list_correct_long_words.append(word_)
        # print("small words",list_correct_small_words)
        # print("long words",list_correct_long_words)
        try:
            best_match_small_word=levenshtein_distance_best_word(list_incorrect_correct_small_words)
        except:
           best_match_small_word=None
        try:
            best_match_long_word=levenshtein_distance_best_word(list_incorrect_correct_long_words)
        except:
            best_match_long_word=None
        # print("best match long word are",best_match_small_word)
        # print("best match small word are",best_match_long_word)
        best_matches_list=[]
        sorted_best_matches_list=[]
        
        if best_match_small_word and best_match_small_word[0]<9:
            best_matches_list.append(best_match_small_word)
        
        
        if best_match_long_word and best_match_long_word[0]<12:
            best_matches_list.append(best_match_long_word)
        
        else :
            pass

        sorted_best_matches_list=sorted(best_matches_list,key = lambda i: i[0])[0]
        
    return sorted_best_matches_list
                                                                                                                                   

def get_best_match_word(common_words):
    list_incorrect_correct_small_words=[]
    list_incorrect_correct_long_words=[]

    # if single not_common_words
    if len(common_words)==1:
        return (0,common_words)
    
    #if common words presents are more then one
    elif len(common_words)>1:
        for word_ in common_words:
            if 3<len(word_)<7:
                    list_incorrect_correct_small_words.append(word_)
                # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
            else:
                    list_incorrect_correct_long_words.append(word_)
       
        try:
            best_match_small_word=levenshtein_distance_best_word(list_incorrect_correct_small_words)
        except:
           best_match_small_word=None
        try:
            best_match_long_word=levenshtein_distance_best_word(list_incorrect_correct_long_words)
        except:
            best_match_long_word=None

        print("this is  match small word",best_match_small_word)
        # best match long words conditions
        print("this is match long word",best_match_long_word)
        best_matches_list=[]
        sorted_best_matches_list=[]
        
        if best_match_small_word and best_match_small_word[0]<9:
            best_matches_list.append(best_match_small_word)
        
        
        if best_match_long_word and best_match_long_word[0]<12:
            best_matches_list.append(best_match_long_word)
        
        else :
            pass

        sorted_best_matches_list=sorted(best_matches_list,key = lambda i: i[0])[0]
        print("this is match long word",sorted_best_matches_list)
        
    return sorted_best_matches_list
                                     
    
def levenshtein_distance_best_word(list_words):
    edit_distance_and_word=[]
    sorted_list_incorrect__word_total_changes=[]
    for similar_word in list_words:
        d=Levenshtein.distance(incorrect_word,similar_word)
        edit_distance_and_word.append((d,similar_word))
    
    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes=sorted(edit_distance_and_word,key = lambda i: i[0])[0]
    
    return sorted_list_incorrect__word_total_changes
  
    # Print string without punctuation 

def get_final_similar_word(white_list_words,incorrect_word,incorrect_word_embedding,white_list_word_embeddings):
       
        matched_words_syms = symspell_matched_word(incorrect_word)
        # print("matched_words_syms",matched_words_syms)
        nlp=spacy.load("en")
        matched_words_syms_text = " ".join(matched_words_syms)
        nlp=nlp(matched_words_syms_text)
        #lemmatized the matched words 
        matched_words_syms= [word_.lemma_ for word_ in nlp]
        print("matched_words_syms",matched_words_syms)

        matched_words_char2vec=cosine_similar_words(incorrect_word_embedding,white_list_word_embeddings,white_list_words)
        nlp=spacy.load("en")
        matched_words_char2vec_text = " ".join(matched_words_char2vec)
        nlp=nlp(matched_words_char2vec_text)
        matched_words_char2vec=[word_.lemma_ for word_ in nlp]
        print("matched_words_char2vec",matched_words_char2vec)
        
        #finding the common words
    
        common_words=[word for word in matched_words_char2vec if word in matched_words_syms]
        print("this is common words",common_words)

        try:
        # if common_words exist
            if common_words:
                matched_word = get_best_match_word(common_words)
                return matched_word[1]
                # return common_words
            # if common words not exist
            else:
                
                best_matched_words_syms = get_best_match_words_not_common(matched_words_syms)
                best_matched_words_char2vec = get_best_match_words_not_common(matched_words_char2vec)
                # print("this must print")
                print("best_matched_words_syms",best_matched_words_syms)
                print("best_matched_words_char2vec",best_matched_words_char2vec)
                
                if best_matched_words_syms and best_matched_words_char2vec:
                    if best_matched_words_syms[0] > best_matched_words_char2vec[0]:
                        return best_matched_words_char2vec[1]

                        # return best_matched_words_char2vec[1]

                    elif best_matched_words_syms[0]==best_matched_words_char2vec[0]:
                        '''    code to be added '''


                        return best_matched_words_syms[1]




                        # return best_matched_words_char2vec[1]

                    else :
                        # best_matched_words_syms[0] < best_matched_words_char2vec[0] :
                        return best_matched_words_syms[1]
                        # return best_matched_words_syms[1]
                elif best_matched_words_syms!=None and best_matched_words_char2vec==None:
                
                    # if best_matched_words_syms[0]>best_matched_words_char2vec[0]:
                        return best_matched_words_syms[1]
                        # return best_matched_words_char2vec[1]

                elif best_matched_words_syms==None and best_matched_words_char2vec!=None:
                    
                    # if best_matched_words_syms[0]>best_matched_words_char2vec[0]:
                        return best_matched_words_char2vec[1]
                        # return best_matched_words_char2vec[1]
                else:
                # if  best_matched_words_char2vec==None and best_matched_words_syms==None:
                    return False
        except:
            pass







if __name__== "__main__":
    
    white_list_words=['information', 'place','gjhy', 'nfmc', 'mark', 'part', 'tariff', 'quantity', 'packages', 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging', 'group', 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
    incorrect_word="plece"
    incorrect_word_embedding=get_word_embeddings([incorrect_word])
    white_list_word_embeddings=get_word_embeddings(white_list_words)

    # print("this is word_embe")
    word=get_final_similar_word(white_list_words,incorrect_word,incorrect_word_embedding,white_list_word_embeddings)
    print(word)
        
    