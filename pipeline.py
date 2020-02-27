from symspell import symspell_matched_word
from main import get_similar_words
import pkg_resources
from symspellpy import SymSpell, Verbosity
import difflib


def word_with_least_change(list_incorrect_correct_long_words): 
    list_incorrect__word_total_changes=[]
    for a,b in list_incorrect_correct_long_words:     
        print('{} => {}'.format(a,b))  
        diff_position=[]
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ': 
                continue
            elif s[0]=='-':
                print(u'Delete "{}" from position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i,a)
            elif s[0]=='+':
                print(u'Add "{}" to position {}'.format(s[-1],i))
                if i not in diff_position:
                    diff_position.append(i) 
        list_incorrect__word_total_changes.append((len(diff_position),a)) 
    #get incorrect word with the number changes  
        sorted_list_incorrect__word_total_changes=sorted(list_incorrect__word_total_changes,key = lambda i: i[0])[0]
        # word_with_small_change=sorted_list_incorrect__word_total_changes[0][1]  #get only word

    return sorted_list_incorrect__word_total_changes



def get_best_match_common_word(common_words):
    words_with_small_len=[]
    word_with_bigger_len=[]

    # if single common_words
    if len(common_words)==1:
        return common_words

    #if common words presents are more then one
    
    elif common_words and len(common_words)>1:
        for i in common_words:

            if 3<len(i)<7:
                words_with_small_len.append(i)
        #   list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]


            else:
                word_with_bigger_len.append(i)
        # word_with_bigger_len=[word for word in common_words if len(word)>=7]

        list_incorrect_correct_small_words = [(word,incorrect_word) for word in words_with_small_len ]
        
        list_incorrect_correct_long_words = [(word,incorrect_word) for word in word_with_bigger_len]
       
       # best  match small words conditions 
        best_match_small_word=word_with_least_change(list_incorrect_correct_long_words)
        if best_match_small_word[0]<2:
            return best_match_small_word[1]
        else:
            pass 
        best_match_long_word=word_with_least_change(list_incorrect_correct_long_words)
        #best match long words conditions
        if best_match_long_word[0]<4:
            return best_match_long_word
        else:
            pass





if __name__== "__main__":
    
   

    white_list_words = ['weight', 'unit', 'value', 'product', 'parties','partial', 'class', 'numeric', 'pieces/type', 'weight/volume', 'container' , 'count', 'hazmat', 'nmfc', 'ltl', 'serial', 'goods', 'package', 'weight/lbs', 'batch', 'item', 'product', 'ordered', 'tons', 'shipping', 'volume/weight', 'gross', 'marks',  'packs', 'goods', 'information', 'order', 'weight', 'rate', 'amount', 'charge', 'quantity', 'quantity', 'total', 'number of items', 'chargeable', 'price', 'pieces', 'kg', 'volume' , 'descending', 'description', 'descriptions', 'type','package', 'packaging', 'class', 'division','commodity', 'pallet', 'slip', 'group', 'value', 'gross', 'unit', 'ltl', 'nfmc', 'details',  'measurement','item details', 'item id', 'hem id', 'sale / lot', 'product','weight', 'unit', 'class', 'hash code', 'item', 'tariff', 'hazmat', 'commodity description', 'mark',  'description',  'serial number', 'part number', 'expiration date', 'lot number', 'item no', 'weight', 'number of pieces', 'no of pieces', 'rate charge', 'qty of goods', 'quantity of goods', 'quantity oft goods', 'nature and quantity', 'chargeable rate', 'rate class', 'po#', 'po #', 'item #', 'item#', 's no', 'description of', 'container no', 'piece count', 'po#', 'po #', 'no of pkgs', 'no of packages', 'volume/weight', 'volume / weight']
    incorrect_word="partia"
    LENGHT_INCORRECT=len(incorrect_word)
    word_embeddings_path="word_embeddings108.sav"
    print("this is word_embe")

    matched_words_syms= symspell_matched_word(incorrect_word)
    matched_words_char2vec=get_similar_words([incorrect_word],word_embeddings_path,white_list_words)
    #finding the common words
    common_words=[word for word in matched_words_char2vec if word in matched_words_syms]
    
    print("matched_words_syms",matched_words_syms)
    print("matched_words_char2vec",matched_words_char2vec)
    print("this is ",common_words)

    # if common_words exist
    # if common_words:
    matched_word=get_best_match_common_word(common_words)
    print("matched word",matched_word)
        # return common_words
    # if common words not exist
    # else:
    #     best_matched_words_syms=get_best_match_common_word(matched_words_syms)

    #     best_matched_words_char2vec=get_best_match_common_word(matched_words_char2vec)

    #     if best_matched_words_syms[0]




