import difflib
import timeit
s=[('1mvoice','invoice')]

def get_operations_on_characters(list_of_tuple_incorrect_correct_words):
    
    start=timeit.default_timer()
    for a,b in list_of_tuple_incorrect_correct_words:
        # print('{} => {}'.format(a,b))
        list_of_operations=[]
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0]==' ':
                continue
 
            elif s[0]=='-':
                # print(u'Delete "{}" from position {}'.format(s[-1],i))
                list_of_operations.append((i,"Delete",s[-1]))
 
            elif s[0]=='+':
                # print(u'Add "{}" to position {}'.format(s[-1],-1))
                list_of_operations.append((i,"Add",s[-1]))
    end=timeit.default_timer()
    print("time taken by get_operations_on_characters {}".format(end-start))
    return list_of_operations
p=get_operations_on_characters(s)
print(s)