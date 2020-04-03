# cython: language_level = 3
cimport cython
import string
import re
import difflib
from Levenshtein import distance
cimport numpy as np
from symspellpy import Verbosity
from white_and_black_list_words_ import black_list_words
import unicodedata
from scipy import spatial
cpdef bint is_number(str s):
    try:
        float(s)
        return True
    except ValueError as err:
        # log_in_file('ValueError : ', err)
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError) as err:
        # log_in_file('ValueError or TypeError: ', err)
        pass
char_replace_list = [
    ["0", "o", "q", "Q", "D", "a","G"],
    ["1", "i", "I", "l", "L", "t","f","L"],
    ["3", "8", "B"],["F","P"],
    ["2", "z", "Z", "s"],
    ["4", "H", "k","R"],
    ["5", "S", "s"],
    ["6", "b", "G", "C", "d"],
    ["7", "T", "j"],
    ["9", "g", "y", "Y"],
    ["m", "rn","ni"],
    ["w", "vv","W","VV"],
    ["#","H"],["io","10","IO"]
]
cpdef list get_prediction_on_multi_words(c2v_model, list list_of_ocr_words, spacy_nlp, sym_spell_len5, sym_spell_len7, list white_list_words, np.ndarray[dtype = np.float32_t, ndim=2]  white_list_word_embeddings ):
    
    cdef :
        list list_predicted_words
        np.ndarray[dtype= np.float32_t, ndim=2] incorrect_word_embedding
        str incorrect_word
        list final_output
        list word
        list word_
        list list_corrected_word
        str cleaned_word
        str predicted_word

    final_output= []
    for word in list_of_ocr_words:   
        list_corrected_word =[]
        for word_ in word:
            #print(word_)
            list_corrected_word.append(word_[0])
            incorrect_word = word_[1]
            try:
                if len(incorrect_word)<4:
                    list_corrected_word.append(incorrect_word)
                elif is_number(incorrect_word):
                    list_corrected_word.append(incorrect_word)
                else:    
                    cleaned_word = incorrect_word.translate(str.maketrans("", "", string.punctuation)).lower()                
                    incorrect_word_embedding = get_c2v_word_embeddings(c2v_model, [incorrect_word])
                    predicted_word = get_final_similar_word(
                    spacy_nlp,
                    sym_spell_len5,
                    sym_spell_len7,
                    white_list_words,
                    white_list_word_embeddings,
                    incorrect_word,
                    incorrect_word_embedding,
                    )
                    list_corrected_word.append(predicted_word)
                    print("list_corrected_word",list_corrected_word)
            except:
                  list_corrected_word.append(incorrect_word)
            
            list_corrected_word.append(word_[2])
    final_output.append([list_corrected_word])

    return final_output

cpdef list symspell_matched_word(sym_spell_len5, sym_spell_len7,str incorrect_word):
    cdef:
        list incorrect_words
        list suggested_words
        str word
        list symspell_matched_words
        int idx
        int max_edit_distance
        bint transfer_casing
        list suggestions
        int length_incorrect_word
        int length_of_suggested_words
        
    length_incorrect_word = len(incorrect_word)      
    if length_incorrect_word < 8:
        incorrect_words = [incorrect_word]
   
        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_words:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell_len5.lookup(
                word, Verbosity.ALL, max_edit_distance= 3, transfer_casing=True
            )  
            for suggestion in suggestions:

                # print(suggestion)
                suggested_words.append((word, suggestion))
                # print(type(suggestion))
        symspell_matched_words = []
        length_of_suggested_words=len(suggested_words)
        for idx in range(length_of_suggested_words):
            # print(s[i][0],str(s[i][1]).split()[0][0:-1])
            symspell_matched_words.append(str(suggested_words[idx][1]).split()[0][0:-1])
        return symspell_matched_words
    else:
        incorrect_words = [incorrect_word]
        # lookup suggestions for single-word input strings
        suggested_words = []
        for word in incorrect_words:
            # A Verbosity parameter allows to control the number of returned results:
            suggestions = sym_spell_len7.lookup(
                word, Verbosity.ALL, max_edit_distance= 4, transfer_casing=True
            )
            # display suggestion term, term frequency, and edit distance.
            for suggestion in suggestions:
                # print(suggestion)
                suggested_words.append((word, suggestion))
                # print(type(suggestion))
        symspell_matched_words = []
        length_of_suggested_words=len(suggested_words)
        for idx in range(length_of_suggested_words):

            # print(s[i][0],str(s[i][1]).split()[0][0:-1])
            symspell_matched_words.append(str(suggested_words[idx][1]).split()[0][0:-1])
        return symspell_matched_words

cpdef np.ndarray[np.float32_t , ndim =2] get_c2v_word_embeddings(c2v_model, list word):
    # Create word embedding of incorrect word
    word_embeddings = c2v_model.vectorize_words(word)
    return word_embeddings

cdef float sort_key_cosine_distance (tuple element):
    return element[0]

cpdef list cosine_similar_words(np.ndarray[dtype=np.float32_t, ndim = 2 ] incorrect_word_embedding, np.ndarray[dtype = np.float32_t, ndim=2 ]  words_embedding, list white_list_words):
    cdef :
        list cosine_distance
        list cosine_similar_words
        int idx
        list sort_cosine_distance
    
    cosine_distance = []
    for idx in range(len(words_embedding)):
        #dist = cosine_similarity([incorrect_word_embedding[0]], [words_embedding[idx]])
        dist = 1 - spatial.distance.cosine(incorrect_word_embedding[0], words_embedding[idx])
        cosine_distance.append((dist, words_embedding[idx]))
    sort_cosine_distance = sorted(cosine_distance, key=sort_key_cosine_distance, reverse=True)[
        0:3
    ]
    print([word[0] for word in sort_cosine_distance ])
    # filter the cosine distance on the basis of threshold value . 
    # sort_cosine_distance = [word[0] for word in cosine_distance if word[0] > threshold ] 
    similar_words = []
    for idx in range(len(words_embedding)):
        for i in range(len(sort_cosine_distance)):
            if (sort_cosine_distance[i][1] == words_embedding[idx]).all():
                if white_list_words[idx] not in similar_words:
                    similar_words.append(white_list_words[idx])

    return similar_words

cdef int sort_key_Levenshtein(tuple tup ):
    return tup[0]

cdef list levenshtein_distance_best_common_words(list list_words, str incorrect_word):
    cdef:
        list edit_distance_and_word =[]
        list sorted_list_incorrect__word_total_changes 
        str similar_word
        int d
        list sorted_list_incorrect__word_total_change
    incorrect_word = incorrect_word
    for similar_word in list_words:
        d = distance(incorrect_word, similar_word)
        edit_distance_and_word.append((d, similar_word))
    # print("this is edited distance",edit_distance_and_word)
    sorted_list_incorrect__word_total_changes = sorted( edit_distance_and_word, key=sort_key_Levenshtein)
    sorted_list_incorrect__word_total_change = [ word for word in sorted_list_incorrect__word_total_changes if word[0] == sorted_list_incorrect__word_total_changes[0][0]]
    return sorted_list_incorrect__word_total_change

cdef list get_operations_on_characters(list list_of_tuple_incorrect_correct_word):
    #print("entered in list_of_tuple_incorrect_correct_word",list_of_tuple_incorrect_correct_word)
    cdef:
        list list_of_tuple_incorrect_correct_words
        str correct_word
        str incorrect_word
        int idx
        str operation
        
    list_of_tuple_incorrect_correct_words = list_of_tuple_incorrect_correct_word
    for correct_word, incorrect_word in list_of_tuple_incorrect_correct_words:
        # print('{} => {}'.format(correct_word,incorrect_word))
        list_of_operations = []
        for idx, operation in enumerate(difflib.ndiff(correct_word, incorrect_word)):
            if operation[0] == " ":
                # nothing changes at this character location
                continue
            elif operation[0] == "-":
                # print(u'Delete "{}" from position {}'.format(operation[-1],idx))
                list_of_operations.append((idx, "Delete", operation[-1]))
            elif operation[0] == "+":
                # print(u'Add "{}" to position {}'.format(operation[-1],-1))
                list_of_operations.append((idx, "Add", operation[-1]))
    #print("list_of_operations found are",list_of_operations)
    return list_of_operations

cdef tuple sort_key(tuple element):
    return (element[0], element[1])


cdef bint is_in_same_list(str character1, str character2):
    cdef :
        list list_
        
    for list_ in char_replace_list:
        if character1 in list_ and character2 in list_:
            return True
    return False

@cython.cdivision(True)
cdef float get_probability_of_correct_character_replacement(list operations_on_characters):
    # sort the operation on the basis of index of character
    #print("enterred in get_probability_of_correct_character_replacement",get_probability_of_correct_character_replacement)
    cdef :
        list operations_sorted_index = sorted(operations_on_characters, key=lambda tuple_: tuple_[0])
        int index1
        int index2
        float probability_of_correct_characters_updated
        int length_list_character_length_and_boolean_values
        list new_list
        int index
        list split_at_index
        list list_character_to_check
        int last_idx
        list list_character_length_and_boolean_values 
        list list_
        str first_character
        str second_character
        str operation1
        str operation2
        str character1
        str character2
        (int, bint) tup_ 

    #print("this need to be print",operations_sorted_index)
    split_at_index = [(index1 + 1) for (index1, operation1, character1), (index2, operation2, character2) in zip(operations_sorted_index, operations_sorted_index[1:]) if (index2 - index1) != 1]
    #print(split_at_index)
    list_character_to_check = []
    last_idx = 0
    for index in split_at_index:
        new_list = [idx for idx in operations_sorted_index[last_idx:] if idx[0] < index]
        list_character_to_check.append(new_list)
        last_idx += len(new_list)
    list_character_to_check.append([tuple_ for tuple_ in operations_sorted_index[last_idx:]])
    # print("list_character_to_check",list_character_to_check)
    # s=[[(0, 'Delete', '1'), (1, 'Add', 'i')], [(10, 'Delete', '0'), (11, 'Add', 'o')], [(13, 'Delete', 'r'), (14, 'Add', 's')]]
    # list_character_length_and_boolean_values shape (length of operation on consecutive character, bool==if character found in char list )
    list_character_length_and_boolean_values = []
    if len(list_character_to_check) == 1 and len(list_character_to_check[0]) == 1:
        return 0.0
    else:
     
        for list_ in list_character_to_check:
            if len(list_) == 1:
                list_character_length_and_boolean_values.append((1, False))

            else:
               # convert string to cython data types
                first_character = ""
                second_character = ""
                for ((index1, operation1, character1),
                    (index2, operation2, character2),
                ) in zip(list_, list_[1:]):
                    if operation1 == operation2:
                        if not (first_character):
                            first_character = character1 + character2
                        if (first_character) and (second_character):
                            second_character = second_character + character2
                        else:
                            print(
                                "either first_character or second_chacter are not satisfying the condition when operations are equal"
                            )
                    else:
                        if not (first_character):
                            first_character = character1

                        if first_character and not second_character:
                            second_character = character2

                        else:
                            print(
                                "either first_character or second_chacter are not satisfying the condition when operations are  not equal"
                            )
                if first_character and second_character:
                    
                    if is_in_same_list(first_character, second_character):
                        # print("replace character matched in replace_char_list")
                        list_character_length_and_boolean_values.append(
                            (len(first_character), True)
                        )
                    else:
                        # print("replace character not matched in replace_char_list ")
                        list_character_length_and_boolean_values.append(
                            (len(first_character), False)
                        )
                else:
                    print("any of first and second character to be matched in character replace list is empty")
                    
        #print("list_character_length _and_boolean_values", list_character_length_and_boolean_values)
        probability_of_correct_characters_updated = len([ tup_ for tup_ in list_character_length_and_boolean_values if tup_[1] == True])
        length_list_character_length_and_boolean_values = len(list_character_length_and_boolean_values)
        #print("found length_list_character_length_and_boolean_values ",length_list_character_length_and_boolean_values)
        if list_character_length_and_boolean_values:
            probability_of_correct_characters_updated = probability_of_correct_characters_updated / length_list_character_length_and_boolean_values
            return probability_of_correct_characters_updated
        else:
            return 0.0

cpdef list  get_word_with_probability_and_edit_distance(list correct_word_list,str incorrect_word):
    #print("entered in get_word_with_probability_and_edit_distance", correct_word_list)
    cdef:
        float probability
        list list_correct_small_words 
        list list_correct_long_words
        list operations_on_characters
        list best_match_small_word_edited_distance
        list word_probability=[]
        list sorted_word_probability
        str  string
        list sorted_best_matches_list
        
    incorrect_word = incorrect_word
    # print("list_correct_small_words",list_correct_small_words)
    # print("list_correct_long_words",list_correct_long_words)
    list_correct_small_words = [string for string in correct_word_list if 2 < len(string) < 7]
    list_correct_long_words  = [string for string in correct_word_list if len(string) >= 7] 
    if list_correct_small_words:
        best_match_small_word_edited_distance = levenshtein_distance_best_common_words(
            list_correct_small_words, incorrect_word)
        #print("small words are there ")
        for  word in best_match_small_word_edited_distance:
                if word[0] <= 3:
                    operations_on_characters = get_operations_on_characters([(incorrect_word, word[1])])
                    #start = timeit.default_timer()
                    probability = get_probability_of_correct_character_replacement(operations_on_characters)
                    #print("get_probability_of_corret_character_replacement used in loop ",probability)
                    word_probability.append((word[0], probability, word[1]))
                    #print("the type of the string is ",type(word[0]),type(word[1]))
                else:
                    print("edit distance is much bigger for small word")
        else:
            print("No small words founds")
    if list_correct_long_words:
        best_match_long_word_edited_distance = levenshtein_distance_best_common_words(list_correct_long_words, incorrect_word)
        #print("best_match_long_word_edited_distance",best_match_long_word_edited_distance)
        for word in best_match_long_word_edited_distance:
            if word[0] <= 4:
                operations_on_characters = get_operations_on_characters(
                    [(incorrect_word, word[1])]
                )
                probability = get_probability_of_correct_character_replacement(operations_on_characters)
                word_probability.append((word[0], probability, word[1]))
            else:
                print("edit distance is much bigger for long word")
    else:
        print("No long words founds")

    sorted_word_probability = sorted(
    word_probability, key=sort_key
    )
    sorted_best_matches_list = [
        tuple_
        for tuple_ in sorted_word_probability
        if tuple_[0] == sorted_word_probability[0][0]
    ]
    #print("sorted_best_matches_list",sorted_best_matches_list)
    if sorted_best_matches_list:
    #print("lsit of best matched words are",sorted_best_matches_list)
        return list(sorted_best_matches_list[-1])
    else:
        #print("Edit distance is more")
        return []




cdef str get_final_similar_word(
    spacy_nlp,
    sym_spell_len5,
    sym_spell_len7,
    list white_list_words,
    np.ndarray[dtype=np.float32_t, ndim = 2 ]  white_list_word_embeddings,
    str incorrect_word,
    np.ndarray[dtype=np.float32_t, ndim = 2 ]  incorrect_word_embedding,
 ): 
    cdef:
        str matched_words_syms_text
        list matched_words_syms
        list matched_words_char2vec
        str matched_words_char2vec_text
        list common_words
        list matched_word
        list best_matched_words_syms
        list sorted_best_matches_list
        list best_matched_words_char2vec
        

    matched_words_syms = symspell_matched_word(
        sym_spell_len5, sym_spell_len7, incorrect_word
    )
    # print("matched_words_syms",matched_words_syms)
    matched_words_syms_text = " ".join(matched_words_syms)
    nlp_output = spacy_nlp(matched_words_syms_text)
    # lemmatized the matched words
    matched_words_syms = [word_.lemma_ for word_ in nlp_output]
    print("lemmatize matched words syms", matched_words_syms)
    matched_words_char2vec = cosine_similar_words(
        incorrect_word_embedding, white_list_word_embeddings, white_list_words
)
    matched_words_char2vec_text = " ".join(matched_words_char2vec)
    nlp_output = spacy_nlp(matched_words_char2vec_text)
    matched_words_char2vec = [word_.lemma_ for word_ in nlp_output]
    print("lemmatize matched words char2vec", matched_words_char2vec)
    common_words = [
        word for word in matched_words_char2vec if word in matched_words_syms
    ]

    try:
        if  common_words:
            matched_word = get_word_with_probability_and_edit_distance(
                 common_words, incorrect_word
             )

            return matched_word[2]
        else:
            best_matched_words_syms = get_word_with_probability_and_edit_distance(
                matched_words_syms, incorrect_word
            )
            matched_words_char2vec = [
                word for word in matched_words_char2vec if word not in black_list_words
            ]

            best_matched_words_char2vec = get_word_with_probability_and_edit_distance(
                matched_words_char2vec, incorrect_word
            )
            matched_words_char2vec = [
                word for word in matched_words_char2vec if word not in black_list_words
            ]

            print(
                "best matched symspell word with probability and edit distance",
                best_matched_words_syms,
            )
            print(
                "best matched char2vec word with probability and edit distance",
                best_matched_words_char2vec,
            )

            if best_matched_words_syms and best_matched_words_char2vec:
                best_matched_words_from_symspell_Char2vec = [
                    best_matched_words_syms,
                    best_matched_words_char2vec,
                ]
                sorted_best_matches_list = sorted(
                    best_matched_words_from_symspell_Char2vec,
                    key=lambda element: (element[0], element[1]),
                )[0]
                return sorted_best_matches_list[2]
            elif best_matched_words_syms and not best_matched_words_char2vec:
                return best_matched_words_syms[2]
            elif not best_matched_words_syms and best_matched_words_char2vec:
                return best_matched_words_char2vec[2]
            else:
                print("No matched word found!")
                return incorrect_word
    except Exception as e:
        print("Some exception has occured", e)
        return incorrect_word




