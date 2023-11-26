from sklearn.feature_extraction.text import TfidfVectorizer
# готовая реализация TF IDF из библиотеки sklearn
from pymystem3 import Mystem
from keyword_search.stop_word import stop_w

rus_stops = stop_w.split(",")

# Создаем специальный объект-векторайзер
make_tf_idf = TfidfVectorizer (stop_words=rus_stops)
moi_analizator = Mystem()

def preprocess_for_tfidif (some_text):
    lemmatized_text = moi_analizator.lemmatize(some_text.lower())
    return (' '.join(lemmatized_text))
    # поскольку tfidf векторайзер принимает на вход строку,
    #после лемматизации склеим все обратно

async def search_message(message):
    file_texts = [message]

    make_tf_idf = TfidfVectorizer(stop_words=rus_stops)
    texts_as_tfidf_vectors = make_tf_idf.fit_transform(preprocess_for_tfidif(text) for text in file_texts)
    id2word = {i: word for i, word in enumerate(make_tf_idf.get_feature_names())}

    # теперь пройдемся по матрице и вытащим для каждого текста слова с самым большим tfidf

    for text_row in range(texts_as_tfidf_vectors.shape[0]):
        # берем ряд в нашей матрице -- он соответстует тексту
        row_data = texts_as_tfidf_vectors.getrow(text_row)
        # сортируем в нем все слова (вернее, индексы слов) -- получаем от самых маленьких к самым большим
        words_for_this_text = row_data.toarray().argsort()
        # берем крайние 6 слов отсортированного ряда
        top_words_for_this_text = words_for_this_text[0, :-6:-1]
    return [id2word[w] for w in top_words_for_this_text]


