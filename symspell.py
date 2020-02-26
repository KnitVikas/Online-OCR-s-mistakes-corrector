
        
import pkg_resources
from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")

# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# lookup suggestions for single-word input strings
# input_term = "Longuge"  # misspelling of "members"

# max edit distance per lookup
# (max_edit_distance_lookup <= max_dictionary_edit_distance)

words = ['Natural', 'Language', 'Understanding',
         'Naturael', 'Longuge', 'Updderctundjing',
         'Motural', 'Lamnguoge', 'Understaating',
         'Naturrow', 'Laguage', 'Unddertandink',
         'Nattural', 'Languagge', 'Umderstoneding']
word=["expiration "]
s=[]
for  word in word:
    

    suggestions = sym_spell.lookup(word, Verbosity.CLOSEST,
                                max_edit_distance=2,transfer_casing=True,ignore_token=r"\w+\d")
    #keep the original casing
    # Avoid correcting phrases matching regex

    # display suggestion term, term frequency, and edit distance
    for suggestion in suggestions:
        # print(suggestion)
        s.append((word,suggestion))
for i in range(len(s)):
    print(s[i][0],s[i][1])
    # print(type(s[i][1]))
    # for i in suggestion:
        # print(i)\
    