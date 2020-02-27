import chars2vec
import sklearn.decomposition
import matplotlib.pyplot as plt
import pickle
import operator
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load Inutition Engineering pretrained model
# Models names: 'eng_50', 'eng_100', 'eng_150', 'eng_200', 'eng_300'

def get_incorrect_word_emb(word):
    c2v_model = chars2vec.load_model('eng_300')

    # Create word embedding of incorrect word
    word_embedding = c2v_model.vectorize_words(word)
    
    # filename = 'word_embeddings.sav'
    # pickle.dump(word_embeddings, open(filename, 'wb'))
    return word_embedding

# load the white list word embedding model from disk
def load_pickel_emb(path):
    loaded_model = pickle.load(open(path, 'rb'))
    word_embeddings=loaded_model
    vec2=word_embeddings
    return vec2


#finding the cosine_similarity ,

def cosine_similar_word_index(vec1,vec2):
    # dist=cosine_similarity([vec1[0]],[vec2[0]])
    cosine_distance=[]
    for i in range(len(vec2)):
        dist=cosine_similarity([vec1[0]],[vec2[i]])
        
        cosine_distance.append((dist[0][0],vec2[i]))

    
    # print(cosine_distance)

    # max_cosine_val=max(cosine_distance,key=lambda item:item[0])[0]
    # print(max_cosine_val)
    sort_cosine_distance = sorted(cosine_distance,key = lambda i: i[0],reverse=True)[0:3]
    print(len(sort_cosine_distance))

    print(sort_cosine_distance[0])

    # print(max_cosine_val)

    # for i in range(len(cosine_distance)):
    #     if cosine_distance[i][0] == max_cosine_val :
    #         word_vec=cosine_distance[i][1]
    # # print(max_cosine_val) 
    
    similar_word_index=[]
    for k in range(len(vec2)):
        for i in range(len(sort_cosine_distance)):
            if (sort_cosine_distance[i][1]==vec2[k]).all():
                if k not in similar_word_index:
                    similar_word_index.append(k)
    # print(similar_word_index)
    # print(sort_cosine_distance)
            
    
    return similar_word_index


# Project embeddings on plane using the PCA
# projection_2d = sklearn.decomposition.PCA(n_components=2).fit_transform(word_embeddings)
# print(vec1[0].shape, vec2[0].shape)

# print(word_vec)
# Draw words on plane
# def sim_word(word_embeddings):
#     similar_word_index=[]
#     for k in range(len(vec2)):
#         if (cosine_sim_word(vec1,word_embeddings)==vec2[k]).all():
#             similar_word_index.append(k)
# result=vec2[np.where(vec2==word_vec)]
# print(result)
# similar_word_index=cosine_similar_word_index(vec1,word_embeddings)
# f = plt.figure(figsize=(8, 6))
# # for j in range(len(projection_2d)):
# plt.scatter(projection_2d[similar_word_index, 0], projection_2d[similar_word_index, 1],
#             marker=('$' + words[0] + '$'),
#             s=500 * len(words[0]), label=0,
#             )
# plt.show()




white_list_words = ['weight', 'unit', 'value', 'product', 'parties','partial', 'class', 'numeric', 'pieces/type', 'weight/volume', 'container' , 'count', 'hazmat', 'nmfc', 'ltl', 'serial', 'goods', 'package', 'weight/lbs', 'batch', 'item', 'product', 'ordered', 'tons', 'shipping', 'volume/weight', 'gross', 'marks',  'packs', 'goods', 'information', 'order', 'weight', 'rate', 'amount', 'charge', 'quantity', 'quantity', 'total', 'number of items', 'chargeable', 'price', 'pieces', 'kg', 'volume' , 'descending', 'description', 'descriptions', 'type','package', 'packaging', 'class', 'division','commodity', 'pallet', 'slip', 'group', 'value', 'gross', 'unit', 'ltl', 'nfmc', 'details',  'measurement','item details', 'item id', 'hem id', 'sale / lot', 'product','weight', 'unit', 'class', 'hash code', 'item', 'tariff', 'hazmat', 'commodity description', 'mark',  'description',  'serial number', 'part number', 'expiration date', 'lot number', 'item no', 'weight', 'number of pieces', 'no of pieces', 'rate charge', 'qty of goods', 'quantity of goods', 'quantity oft goods', 'nature and quantity', 'chargeable rate', 'rate class', 'po#', 'po #', 'item #', 'item#', 's no', 'description of', 'container no', 'piece count', 'po#', 'po #', 'no of pkgs', 'no of packages', 'volume/weight', 'volume / weight']
incorrect_word=["class"]
word_embeddings_path="word_embeddings108.sav"

def get_similar_words(incorrect_word,word_embeddings_path,white_list_words):
    word_embeddings=load_pickel_emb(word_embeddings_path)
    # print(word_embeddings.shape)
    word_emb_incorrect_word=get_incorrect_word_emb(incorrect_word)
    # print(word_emb_incorrect_word)

    similar_word_index=cosine_similar_word_index(word_emb_incorrect_word,word_embeddings)
    # print(similar_word_index)
    matched_words=[]
    for i in range(len(similar_word_index)):
        matched_words.append(white_list_words[i])
        # print(matched_words)
    return matched_words
print(get_similar_words(incorrect_word,word_embeddings_path,white_list_words))