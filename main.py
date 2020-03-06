from symspell import symspell_matched_word
from Chars2vec import cosine_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib
from itertools import groupby
from operator import itemgetter
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


def get_operations_on_characters(list_of_tuple_incorrect_correct_words):

    for a,b in list_of_tuple_incorrect_correct_words:
        # print('{} => {}'.format(a,b))
        list_of_operations=[]
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ' :
                continue
 
            elif s[0]=='-' :
                # print(u'Delete "{}" from position {}'.format(s[-1],i))
                list_of_operations.append((i,"Delete",s[-1]))
 
            elif s[0]=='+':
                # print(u'Add "{}" to position {}'.format(s[-1],-1))
                list_of_operations.append((i,"Add",s[-1]))
    return list_of_operations


def get_best_matched_word_from_operations_using_char_list(operations):
      
    # sort the operation on the basis of index of character
    operations=sorted(operations,key = lambda i: i[0])
    index_sorted = [tup[0] for tup in operations]
    print( "operations" ,operations)
    list_index=[]
    for k,g in groupby(enumerate(index_sorted),lambda ix :ix[0] - ix[1]):
        list_index.append(list(map(itemgetter(1),g)))
    index_to_check=[idx for idx in list_index if len(list_index)>=1]

    print( "index_to_check" ,index_to_check)
    list_char_to_check=[]
    for list_ in index_to_check:
        list_consecutive_char=[]
        for index in list_:
            for operation in operations:
                if index==operation[0]:
                    list_consecutive_char.append(operation)
        list_char_to_check.append(list_consecutive_char)
    print("this is list_char_to_check" , list_char_to_check)
    # s=[[(0, 'Delete', '1'), (1, 'Add', 'i')], [(10, 'Delete', '0'), (11, 'Add', 'o')], [(13, 'Delete', 'r'), (14, 'Add', 's')]]
    list_tup_length_bool_value=[]
    #list_tup_length_bool_value shape (length of operation on consecutive character, bool==if character found in char list )
    
    for list_ in list_char_to_check:
        first_character = ""
        second_character = ""
        for (index1, operation1, character1) , (index2, operation2, character2) in zip(list_,list_[1:]):
            if operation1 == operation2:
                if not (first_char):
                    first_character = character1 + character2

                if (first_character) and (second_char) :
                    second_character = second_character + character2
                
                else :
                     print("sequence of operation does not  matches")
            else:
                if not (first_character):
                    first_character = character1
                if first_character and not second_character:
                    second_character = character2

                print("sequence of operation does not  matches")
        if first_char and second_char:
            if in_same_group(first_character,second_character): 
                # print("this got in")
                list_tup_length_bool_value.append((len(first_char), True))
            else :
                # print("this not got in")
                list_tup_length_bool_value,append((len(first_char),False))
        else:
            list_tup_length_bool_value,append((len(first_char),False))
                # ''' work on list_tup_length_bool_value '''
         
    return list_tup_length_bool_value

def get_best_match_words_not_common(not_common_words):

    # if single not_common_words
    if len(not_common_words)==1:
        return not_common_words[0]
    
    elif len(not_common_words)>1:
        list_correct_small_words=[word for word in not_common_words if 3<len(word_)<7 ]
        list_correct_long_words=[ word for word in not_common_words if len(word_)>=7 ]
       
        word_prob=[]
        try:
            best_match_small_word_edited_distance=levenshtein_distance_best_common_words(list_correct_small_words)
            for word in best_match_small_word_edited_distance:
                
                if word[0]<=2:
                    probability=get_best_matched_word_from_operations(word[1])
                    word_prob.append((word[0],probability,word[1]))
                else:
                    pass

        except:
           pass

        try:
            best_match_long_word_edited_distance=levenshtein_distance_best_common_words(list_correct_long_words)
            for word in best_match_long_word_edited_distance:
                if word<=4:
                    probability = get_best_matched_word_from_operations((word[1],probabaility))
                    word_prob.append((word[0],probability,word[1]))
        except:
            pass

        sorted_best_matches_list=sorted(word_prob,key = lambda element:(element[0],element[1]))
        sorted_best_matches_list=[prob for prob in sorted_best_matches_list if prob[0]==sorted_best_matches_list[0]]
        
    return sorted_best_matches_list[-1][2]
                                                                                                                                   

def get_best_match_word(common_words):
    if len(common_words)==1:
        return common_words[0]
    
    #if common words presents are more then one
    elif len(common_words)>1:

        
        best_match_word=levenshtein_distance_best_common_words(common_words)
        sorted_best_matches_list_words=[]
        sorted_best_matches_list=[]
 
        if best_match_word:
        #word to return
            sorted_best_matches_list=sorted(best_match_word,key = lambda i: i[0])
            if len(sorted_best_matches_list)==1:
                sorted_best_matches_list_words.append(sorted_best_matches_list[0][1])
            
            else :
            #select bestmatch
                common_edit_distance_word=[idx for idx in sorted_best_matches_list if idx[0]==sorted_best_matches_list[0][0]]
                # print("common_edit_distance_word",common_edit_distance_word)
                correct_word_containing_char_in_char_list=[]

                for word in common_edit_distance_word:
                    operation_sequence = get_operations_on_characters([(incorrect_word,word[1])])
                    bool_value= function_to_check_characters_in_char_list(operation_sequence)

                    if bool_value == True :
                        correct_word_containing_char_in_char_list.append((word[1],bool_value))
                        
                    else:
                        correct_word_containing_char_in_char_list.append((word[1],bool_value))
                
                matched_word=[idx for idx in correct_word_containing_char_in_char_list if idx[1]==True]
                sorted_best_matches_list_words.extend(matched_word)
                print("matched word",sorted_best_matches_list_words[0][0])

            return sorted_best_matches_list_words[0][0]
        
           
    
def levenshtein_distance_best_word(list_words):
    edit_distance_and_word=[]
    sorted_list_incorrect__word_total_changes=[]
    for similar_word in list_words:
        d=Levenshtein.distance(incorrect_word,similar_word)
        edit_distance_and_word.append((d,similar_word))
    
    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes=sorted(edit_distance_and_word,key = lambda i: i[0])[0]

    
    return sorted_list_incorrect__word_total_changes


def levenshtein_distance_best_common_words(list_words):
    edit_distance_and_word=[]
    sorted_list_incorrect__word_total_changes=[]
    for similar_word in list_words:
        d=Levenshtein.distance(incorrect_word,similar_word)
        edit_distance_and_word.append((d,similar_word))
    
    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes=sorted(edit_distance_and_word,key = lambda i: i[0])
    sorted_list_incorrect__word_total_changes=[word for word in sorted_list_incorrect__word_total_changes if word[0]==sorted_list_incorrect__word_total_changes[0][0]]

    
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
        # print("matched_words_syms",matched_words_syms)

        matched_words_char2vec=cosine_similar_words(incorrect_word_embedding,white_list_word_embeddings,white_list_words)
        nlp=spacy.load("en")
        matched_words_char2vec_text = " ".join(matched_words_char2vec)
        nlp=nlp(matched_words_char2vec_text)
        matched_words_char2vec=[word_.lemma_ for word_ in nlp]

        # print("matched_words_char2vec",matched_words_char2vec)
        
        #finding the common words
        common_words=[word for word in matched_words_char2vec if word in matched_words_syms]
        print("this is common words",common_words)

        try:
        # if common_words exist
            if common_words:
                matched_word = get_best_match_word(common_words)
                print("this is the matche one " ,matched_word)
                return matched_word
            # elif len(common_words)=22:

            #     peration_sequence_syms = get_operations_on_characters([(incorrect_word,best_matched_words_syms[1])])
            #     bool_value_symspell = function_to_check_characters_in_char_list(operation_sequence_syms)
            # # if common words not exist
            else:
                # print("this must print")
                
                best_matched_words_syms = get_best_match_words_not_common(matched_words_syms)
                best_matched_words_char2vec = get_best_match_words_not_common(matched_words_char2vec)
                # print("this must print")
                print("best_matched_words_syms",best_matched_words_syms)
                print("best_matched_words_char2vec",best_matched_words_char2vec)
                
                if  best_matched_words_syms and best_matched_words_char2vec:
                    if best_matched_words_syms[0] > best_matched_words_char2vec[0]:
                        return best_matched_words_char2vec[1]

                    # replaced character if it is in char_list
                    elif best_matched_words_syms[0] == best_matched_words_char2vec[0] :
         
                        
                        operation_sequence_syms = get_operations_on_characters([(incorrect_word,best_matched_words_syms[1])])
                        bool_value_symspell = function_to_check_characters_in_char_list(operation_sequence_syms)
                    
                        operation_sequence_char2vec = get_operations_on_characters([(incorrect_word,best_matched_words_char2vec[1])])
                        bool_value_char2vec= function_to_check_characters_in_char_list(operation_sequence_char2vec)

                        if bool_value_symspell == True and bool_value_char2vec==True:
                            return best_matched_words_char2vec[1]
                        elif bool_value_symspell == False and bool_value_char2vec==True:
                            return best_matched_words_char2vec[1]
                        elif bool_value_symspell == True and bool_value_char2vec==False:
                            return best_matched_words_syms[1]
                        else:
                            return best_matched_words_char2vec[1]
                    
                    else :
                        return best_matched_words_syms[1]

                


                       
                elif best_matched_words_syms!=None and best_matched_words_char2vec==None:
                        return best_matched_words_syms[1]
                       

                elif best_matched_words_syms==None and best_matched_words_char2vec!=None:
                        return best_matched_words_char2vec[1]

                else:
              
                    return incorrect_word
        except:
            pass







if __name__== "__main__":
    
    white_list_words=['information', 'place', 'mark', 'part', 'tariff', 'quantity', 'packages', 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging', 'group', 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
    incorrect_word="plece"

    incorrect_word_embedding=get_word_embeddings([incorrect_word])
    white_list_word_embeddings=get_word_embeddings(white_list_words)

    # print("this is word_embe")
    # word=get_final_similar_word(white_list_words,incorrect_word,incorrect_word_embedding,white_list_word_embeddings)
    # print(word)  