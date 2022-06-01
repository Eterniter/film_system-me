import json
import math
import jieba
import operator
from mysql_query import DB
from collections import defaultdict


class TfIdf:
    @staticmethod
    def get_stopwords(file_path="film_system-me\stop_word.txt"):
        stopwords = [
            line.strip() for line in open(file_path, encoding="UTF-8").readlines()
        ]
        stopwords += " "
        stopwords += "\n"
        return stopwords

    @staticmethod
    def word_segmentation_without_stopwords(text, stopwords=[]):
        if len(stopwords) == 0:
            stopwords = TfIdf.get_stopwords()
        words = jieba.cut(text)
        res = []
        for word in words:
            word = word.strip().strip("\u0329")
            if len(word) > 0 and (word not in stopwords):
                res.append(word)
        return res

    @staticmethod
    def tf_idf(text_list: tuple):
        stopwords = TfIdf.get_stopwords()
        word_list = []
        for text in text_list:
            word_list.append(
                TfIdf.word_segmentation_without_stopwords(text, stopwords)
            )
        # 统计总词频
        word_frequency = defaultdict(int)
        for item in word_list:
            for word in item:
                word_frequency[word] += 1
        # 计算TF值
        word_tf = defaultdict(int)
        total = max(
            word_frequency.values()
        )  # 选取出现次数最多的词的出现次数，使词频的值相对大点，便于分析，比如一本书出现一个词语100次，但整本书10万字
        for word, frequency in word_frequency.items():
            word_tf[word] = frequency / total
        # 计算IDF值
        total = len(text_list)
        word_idf = {}
        word_doc = defaultdict(int)  # 存储包含该词的文档数
        for word in word_frequency.keys():
            for list in word_list:
                if word in list:
                    word_doc[word] += 1
        for word in word_frequency.keys():
            word_idf[word] = math.log(total / (word_doc[word] + 1))
        # 计算TF-IDF
        for word in word_frequency.keys():
            word_tf[word] *= word_idf[word]
        return sorted(word_tf.items(), key=operator.itemgetter(1), reverse=True)

    @staticmethod
    def store_tf_idf():
        # 存储TF-IDF算法计算出的前20个关键词进入数据库中
        db = DB()
        film_id_ls = db.get_film_id_without_tf_idf_keywords()
        for film_id in film_id_ls:
            text = db.select_comment_content(film_id)
            key_words = TfIdf.tf_idf(text)
            if len(key_words) >= 20:
                key_words = key_words[:20]
            key_words = json.dumps(key_words, ensure_ascii=False)
            db.store_film_item_one_field("tf_idf_keywords", film_id, key_words)

    @staticmethod
    def compute_cosine_similarity(key_words1: list, key_words2: list):
        # 可能有列表长度不等的问题
        union_key_word = [key_words1[i][0] for i in range(len(key_words1))]
        for word in [key_words2[i][0] for i in range(len(key_words2))]:
            if word not in union_key_word:
                union_key_word.append(word)
        key_words1 = dict(key_words1)
        key_words2 = dict(key_words2)
        for word in union_key_word:
            key_words1.setdefault(word, 0)
            key_words2.setdefault(word, 0)
        s = sum([key_words1[word] * key_words2[word] for word in union_key_word])
        den1 = math.sqrt(sum([pow(key_words1[word], 2) for word in union_key_word]))
        den2 = math.sqrt(sum([pow(key_words2[word], 2) for word in union_key_word]))
        return s / (den1 * den2)

    @staticmethod
    def store_compute_cosine_similarity():
        db = DB()
        movid_id_ls = db.get_film_id()
        for film_id in movid_id_ls:
            res = []
            film_item = db.get_film_item(film_id, extra_info=False)
            for film_other in movid_id_ls:
                if film_id != film_other:
                    film_other_item = db.get_film_item(film_other, extra_info=False)
                    key_words1 = json.loads(film_item["tf_idf_keywords"])
                    key_words2 = json.loads(film_other_item["tf_idf_keywords"])
                    similarity = TfIdf.compute_cosine_similarity(
                        key_words1, key_words2
                    )
                    res.append(
                        {
                            "film_id": film_other,
                            "film_name": film_other_item["film_name"],
                            "similarity": similarity,
                        }
                    )
            res.sort(key=lambda tmp: tmp["similarity"], reverse=True)
            res = json.dumps(res[:12], ensure_ascii=False)
            db.store_film_item_one_field("similarity_film", film_id, res)

    @staticmethod
    def calculate():
        TfIdf.store_tf_idf()
        TfIdf.store_compute_cosine_similarity()


if __name__ == "__main__":
    TfIdf().calculate()
