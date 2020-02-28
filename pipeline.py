from symspell import symspell_matched_word
from main import get_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib


def word_with_least_change(list_OfTUple_incorrect_correct_long_words): 
    list_incorrect__word_total_change=[]
    sorted_list_incorrect__word_total_changes=[]
    for a,b in list_OfTUple_incorrect_correct_long_words:     
        # print('{} => {}'.format(a,b))  
        diff_position=[]
        
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ': 
                continue
            elif s[0]=='-':
                # print(u'Delete "{}" from position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i)
            elif s[0]=='+':
                # print(u'Add "{}" to position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i) 
        list_incorrect__word_total_change.append((len(diff_position),a)) 
    #get incorrect word with the number changes  
        sorted_list_incorrect__word_total_changes=sorted(list_incorrect__word_total_change,key = lambda i: i[0])[0]
        # word_with_small_change=sorted_list_incorrect__word_total_changes[0][1]  #get only word

    return sorted_list_incorrect__word_total_changes



def get_best_match_common_word(common_words):
    words_with_small_len=[]
    word_with_bigger_len=[]

    # if single common_words
    if len(common_words)==1:
        return common_words

    #if common words presents are more then one
    
    elif len(common_words)>1:
        for i in common_words:

            if 3<len(i)<7:
                words_with_small_len.append(i)
              # list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
            else:
                word_with_bigger_len.append(i)
             # word_with_bigger_len=[word for word in common_words if len(word)>=7]

        list_incorrect_correct_small_words = [(incorrect_word,word) for word in words_with_small_len ]
        # print("list_incorrect_correct_small_words",list_incorrect_correct_small_words)
        list_incorrect_correct_long_words = [(incorrect_word,word) for word in word_with_bigger_len]
        # print("list_incorrect_correct_long_words",list_incorrect_correct_long_words)
       # best  match small words conditions 
        best_match_small_word=word_with_least_change(list_incorrect_correct_small_words)
        # print("best match small word",best_match_small_word,type(best_match_small_word))
        if best_match_small_word and best_match_small_word[0]<2:
            return best_match_small_word[1]
        else:
            pass 
        best_match_long_word=word_with_least_change(list_incorrect_correct_long_words)
        #best match long words conditions
        # print("best match long word",best_match_long_word)
        if best_match_long_word and best_match_long_word[0]<4:
            return best_match_long_word
        else:
            pass




def get_best_match_words_not_common(not_common_words):
    words_with_small_len=[]
    word_with_bigger_len=[]

    # if single not_common_words
    if len(not_common_words)==1:
        return (0,not_common_words[0])

    #if common words presents are more then one
    
    elif len(not_common_words)>1:
        for i in not_common_words:

            if 3<len(i)<7:
                words_with_small_len.append(i)
        #list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]

            else:
                word_with_bigger_len.append(i)
        #word_with_bigger_len=[word for word in not_common_words if len(word)>=7]

        list_incorrect_correct_small_words = [(incorrect_word,word) for word in words_with_small_len ]
        # print(list_incorrect_correct_small_words)
        list_incorrect_correct_long_words = [(incorrect_word,word) for word in word_with_bigger_len]
        print(list_incorrect_correct_long_words)
       #best  match small words conditions 
        best_match_small_word=word_with_least_change(list_incorrect_correct_small_words)
        # print("best match small word",best_match_small_word,type(best_match_small_word))
        if best_match_small_word and best_match_small_word[0]<2:
            return best_match_small_word
        else:
            pass 
        best_match_long_word=word_with_least_change(list_incorrect_correct_long_words)
        #best match long words conditions
        print("best match long word",best_match_long_word)
        if best_match_long_word and best_match_long_word[0]<4:
            return best_match_long_word
        else:
            pass

def remove_number_from_sym_incorrect_words(string): 
    # remove_number_from_sym_word marks 
    numbers = '0123456789' 
    # marks occur replace it with null 
    for x in string.lower(): 
        if str(x) in numbers: 
            string = string.replace(x, "?")
    return string
  
    # Print string without punctuation 


if __name__== "__main__":
    
    white_list_words=['information', 'nfmc', 'mark', 'part', 'tariff', 'quantity', 'packages', 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging', 'group', 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
    
    incorrect_word="we1ght"
    incorrect_word_symspell=remove_number_from_sym_incorrect_words(incorrect_word)

    LENGHT_INCORRECT=len(incorrect_word)
    word_embeddings_path="static/word_embeddings52.sav"
    # print("this is word_embe")
    try:
        matched_words_syms= symspell_matched_word(incorrect_word_symspell)
        matched_words_char2vec=get_similar_words([incorrect_word],word_embeddings_path,white_list_words)
        #finding the common words
        common_words=[word for word in matched_words_char2vec if word in matched_words_syms]
        
        print("matched_words_syms",matched_words_syms)
        print("matched_words_char2vec",matched_words_char2vec)
        print("this is common words",common_words)

        # if common_words exist
        if common_words:
            matched_word=get_best_match_common_word(common_words)
            print("matched word",matched_word)
            # return common_words
        # if common words not exist
        else:
            best_matched_words_syms=get_best_match_words_not_common(matched_words_syms)

            best_matched_words_char2vec=get_best_match_words_not_common(matched_words_char2vec)
           
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
                
                if best_matched_words_syms[0]>best_matched_words_char2vec[0]:
                    print("matched word",best_matched_words_char2vec[1])
                    # return best_matched_words_char2vec[1]
    except :
        pass





