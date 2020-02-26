import chars2vec
import sklearn.decomposition
import matplotlib.pyplot as plt
import pickle
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

def cosine_sim_word_index(vec1,vec2):
    # dist=cosine_similarity([vec1[0]],[vec2[0]])
    cos_dist=[]
    for i in range(len(vec2)):
        dist=cosine_similarity([vec1[0]],[vec2[i]])
        
        cos_dist.append((dist[0][0],vec2[i]))
    # print(type(cos_dist))
    cos_d=[]
    for i in range(len(cos_dist)):
        cos_d.append(cos_dist[i][0]) 
    # print(cos_dist[0][0])
    # max_cosine_val=max(cos_dist)[0]

    max_cosine_val=max(cos_dist,key=lambda item:item[0])[0]
    # print(max_cosine_val)

    for i in range(len(cos_dist)):
        if cos_dist[i][0] == max_cosine_val :
            word_vec=cos_dist[i][1]
    # print(max_cosine_val) 
    
    similar_word_index=[]
    for k in range(len(vec2)):
        if (word_vec==vec2[k]).all():
            similar_word_index.append(k)
            
    
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
# similar_word_index=cosine_sim_word_index(vec1,word_embeddings)
# f = plt.figure(figsize=(8, 6))
# # for j in range(len(projection_2d)):
# plt.scatter(projection_2d[similar_word_index, 0], projection_2d[similar_word_index, 1],
#             marker=('$' + words[0] + '$'),
#             s=500 * len(words[0]), label=0,
#             )
# plt.show()

if __name__ == "__main__":



    white_list_words = ['weight', 'unit', 'value', 'product', 'parties','partial', 'class', 'numeric', 'pieces/type', 'weight/volume', 'container' , 'count', 'hazmat', 'nmfc', 'ltl', 'serial', 'goods', 'package', 'weight/lbs', 'batch', 'item', 'product', 'ordered', 'tons', 'shipping', 'volume/weight', 'gross', 'marks',  'packs', 'goods', 'information', 'order', 'weight', 'rate', 'amount', 'charge', 'quantity', 'quantity', 'total', 'number of items', 'chargeable', 'price', 'pieces', 'kg', 'volume' , 'descending', 'description', 'descriptions', 'type','package', 'packaging', 'class', 'division','commodity', 'pallet', 'slip', 'group', 'value', 'gross', 'unit', 'ltl', 'nfmc', 'details',  'measurement','item details', 'item id', 'hem id', 'sale / lot', 'product','weight', 'unit', 'class', 'hash code', 'item', 'tariff', 'hazmat', 'commodity description', 'mark',  'description',  'serial number', 'part number', 'expiration date', 'lot number', 'item no', 'weight', 'number of pieces', 'no of pieces', 'rate charge', 'qty of goods', 'quantity of goods', 'quantity oft goods', 'nature and quantity', 'chargeable rate', 'rate class', 'po#', 'po #', 'item #', 'item#', 's no', 'description of', 'container no', 'piece count', 'po#', 'po #', 'no of pkgs', 'no of packages', 'volume/weight', 'volume / weight']


    incorrect_word=["partis"]
    word_embeddings_path="word_embeddings108.sav"
    word_embeddings=load_pickel_emb(word_embeddings_path)
    # print(word_embeddings.shape)
    word_emb_incorrect_word=get_incorrect_word_emb(incorrect_word)
    # print(word_emb)
    similar_word_index=cosine_sim_word_index(word_emb_incorrect_word,word_embeddings)
    # print(index)
    print(white_list_words[similar_word_index[0]])