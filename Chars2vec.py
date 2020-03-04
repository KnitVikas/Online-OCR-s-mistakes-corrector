import chars2vec
import sklearn.decomposition
import matplotlib.pyplot as plt
import pickle
import operator
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load Inutition Engineering pretrained model
# Models names: 'eng_50', 'eng_100', 'eng_150', 'eng_200', 'eng_300'


def get_word_embeddings(word):
    c2v_model = chars2vec.load_model("eng_300")
    # Create word embedding of incorrect word
    word_embeddings = c2v_model.vectorize_words(word)
    # filename = 'word_embeddings.sav'
    # pickle.dump(word_embeddings, open(filename, 'wb'))
    return word_embeddings


# load the white list word embedding model from disk
# def load_pickel_emb(path):
#     loaded_word_embeddings = pickle.load(open(path, 'rb'))
#     return loaded_word_embeddings


# finding the cosine_similarity
def cosine_similar_words(incorrect_word_embedding, words_embedding, white_list_words):
    # dist=cosine_similarity([incorrect_word_embedding[0]],[words_embedding[0]])
    cosine_distance = []
    for idx in range(len(words_embedding)):
        dist = cosine_similarity([incorrect_word_embedding[0]], [words_embedding[idx]])
        cosine_distance.append((dist[0][0], words_embedding[idx]))

    # print(cosine_distance)

    # max_cosine_val=max(cosine_distance,key=lambda item:item[0])[0]
    # print(max_cosine_val)
    sort_cosine_distance = sorted(cosine_distance, key=lambda i: i[0], reverse=True)[
        0:3
    ]
    # print(len(sort_cosine_distance))

    similar_words = []
    for idx in range(len(words_embedding)):
        for i in range(len(sort_cosine_distance)):
            if (sort_cosine_distance[i][1] == words_embedding[idx]).all():
                if white_list_words[idx] not in similar_words:
                    similar_words.append(white_list_words[idx])

    return similar_words


# Project embeddings on plane using the PCA
# projection_2d = sklearn.decomposition.PCA(n_components=2).fit_transform(word_embeddings)
# print(incorrect_word_embedding[0].shape, words_embedding[0].shape)

# print(word_vec)
# Draw words on plane
# def sim_word(word_embeddings):
#     similar_word_index=[]
#     for k in range(len(words_embedding)):
#         if (cosine_sim_word(incorrect_word_embedding,word_embeddings)==words_embedding[k]).all():
#             similar_word_index.append(k)
# result=words_embedding[np.where(words_embedding==word_vec)]
# print(result)
# similar_word_index=cosine_similar_word(incorrect_word_embedding,word_embeddings)
# f = plt.figure(figsize=(8, 6))
# # for j in range(len(projection_2d)):
# plt.scatter(projection_2d[similar_word_index, 0], projection_2d[similar_word_index, 1],
#             marker=('$' + words[0] + '$'),
#             s=500 * len(words[0]), label=0,
#             )
# plt.show()

# white_list_words=['information', 'nfmc', 'mark', 'part', 'tariff', 'quantity', 'packages', 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging', 'group', 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
# # incorrect_word=["inform"]
# print(len(white_list_words))
# word_embeddings_path="word_embeddings52.sav"
# print(word_embeddings.shape)

# white_list_words = ['information' , 'gjhy' , 'nfmc' , 'mark' , 'part' , 'tariff' , 'quantity' , 'packages' , 'description', 'gross', 'class', 'hazmat', 'commodity', 'package', 'pallet', 'value', 'marks', 'pieces', 'type', 'parties', 'order', 'volume', 'weight', 'numeric', 'division', 'item', 'shipping', 'product', 'slip', 'batch', 'partial', 'expiration', 'unit', 'details', 'measurement', 'count', 'nature', 'container', 'price', 'rate', 'charge', 'packaging' , 'group' , 'ordered', 'packs', 'goods', 'amount', 'hash', 'chargeable', 'tons', 'total', 'serial', 'descending']
# white_list_embeddings = get_word_embeddings(white_list_words)
# incorrect_word_embedding=get_word_embeddings(["quants"])
# # print(incorrect_word_embedding)

# words=cosine_similar_words(incorrect_word_embedding,white_list_embeddings,white_list_words)

# print(words)
