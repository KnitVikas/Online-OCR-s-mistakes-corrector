import seaborn as sns
import matplotlib.pyplot as plt


from chars2vec_s.model import load_model
import sklearn.decomposition
import matplotlib.pyplot as plt
import chars2vec
from scipy import spatial
import numpy as np

# Load Inutition Engineering pretrained model
# Models names: 'eng_50', 'eng_100', 'eng_150', 'eng_200', 'eng_300'
c2v_model = load_model("single_word_trained_model")

white_list_words_incorrect_word = [
    "place",
    "mark",
    "invoice",
    "part",
    "tariff",
    "quantity",
    "packages",
    "description",
    "information",
    "commodity",
    "marks",
    "piece",
    "pieces",
    "type",
    "parties",
    "order",
    "volume",
    "weight",
    "lnformotlon",
    "plece",
    "comm0dlty",
    "yolunre",
    "1nf0rmati0n",
    "numerlc",
    "weight",
    "yolume",
    "partlie5",
    "dascrlpt1on",
    "auantity",
    "packayes",
    "mork",
    "plec",
    "0rder",
    "1mvoice",
    "tgpe",
]
print(len(white_list_words_incorrect_word))

incorrect_word_embedding = c2v_model.vectorize_words(white_list_words_incorrect_word)
# for j in range(1, 5):
projection_2d = sklearn.decomposition.PCA(n_components=2).fit_transform(
    incorrect_word_embedding
)
print(projection_2d.shape)
cos_dist = []
for embe in range(len(projection_2d)):
    for idx in range(len(projection_2d)):

        dist = 1 - spatial.distance.cosine(projection_2d[embe], projection_2d[idx])
        cos_dist.append(
            (
                dist,
                (
                    white_list_words_incorrect_word[idx],
                    white_list_words_incorrect_word[embe],
                ),
            )
        )

cos_dist_nearest = sorted(cos_dist, key=lambda x: x[0], reverse=True)
print("cosine dist for dimentionality reduction  component 2 ", cos_dist_nearest)
white_list_words_incorrect_word = white_list_words_incorrect_word[:-1]


f_word = []
s_word = []
cosine = []
for item in cos_dist_nearest:
    cosine.append(item[0])
    f_word.append(item[1][0])
    s_word.append(item[1][1])


import pandas as pd

df_tmp = pd.DataFrame({"f_word": f_word, "s_word": s_word, "cosine": cosine})

df_tmp["pairs"] = list(zip(df_tmp.f_word, df_tmp.s_word, round(df_tmp.cosine, 7)))
df_hm = pd.DataFrame(
    {"ind": range(1225), "cols": range(1225), "vals": pd.Series(np.zeros(1225))}
)
df_hm = df_hm.pivot(index="ind", columns="cols").fillna(0)

for row, col, similarity in df_tmp.pairs:
    #     print(row, col, similarity)
    try:
        df_tmp.iloc[col, df_tmp.columns.get_loc(row)] = similarity
    except:
        pass


def plot_heatmap(df_hm, xlabels, ylabels):
    """
    Given a dataframe containing similarity grid, plot the heatmap
    """
    sns.set(style="white")

    # Set up the matplotlib figure
    # (to enlarge the cells, increase the figure size)
    f, ax = plt.subplots(figsize=(18, 18))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(df_hm, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(
        df_hm,
        mask=mask,
        cmap=cmap,
        center=0.5,
        xticklabels=xlabels,
        yticklabels=ylabels,
        square=True,
        linewidths=0.5,
        fmt=".2f",
        annot=True,
        cbar_kws={"shrink": 0.5},
        vmax=1,
        vmin=-1,
    )

    ax.set_title("Heatmap of cosine similarity scores").set_fontsize(15)
    ax.set_xlabel("")
    ax.set_ylabel("")

    return ax


plot_heatmap(df_hm, f_word, f_word)
