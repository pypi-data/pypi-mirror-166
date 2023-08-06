#!/usr/bin/env python
import enum
import json
import pickle
import threading
from typing import List

import codefast as cf
import jieba

from .const import Const

cf.info("GOGOGO.")


class myconsts(object):
    PICKLED_TENCENT_WORD_EMBEDDING = '/tmp/tencent-embedding-100-small.pkl'
    TENCENT_EMBEDDING_URL = 'https://bit.ly/38tqveD'
    TENCENT_EMBEDDING = None

    @classmethod
    def init(cls):
        cf.info('Downloading Tencent embedding from {}'.format(
            cls.TENCENT_EMBEDDING_URL))
        cf.net.download(cls.TENCENT_EMBEDDING_URL,
                        cls.PICKLED_TENCENT_WORD_EMBEDDING)
        cls.TENCENT_EMBEDDING = pickle.load(
            open(cls.PICKLED_TENCENT_WORD_EMBEDDING, 'rb'))
        assert "向量" in cls.TENCENT_EMBEDDING
        cf.info("Tencent embedding loaded")


class NlpWorker(object):
    def __init__(self) -> None:
        pass

    def jieba(self, sentence):
        return jieba.lcut(sentence)

    def batch_token(self, sentence_list: List[str]) -> List[List[str]]:
        return [jieba.lcut(sentence) for sentence in sentence_list]

    def word_embedding(self, word) -> List[float]:
        if word in myconsts.TENCENT_EMBEDDING:
            return myconsts.TENCENT_EMBEDDING[word].tolist()
        else:
            return [0.0] * 100

    def batch_word_embedding(self, word_list: List[str]) -> List[List[float]]:
        return [self.word_embedding(word) for word in word_list]


class TaskTypeEnum(enum.Enum):
    token = 1
    batch_token = 2
    word_embedding = 3
    batch_word_embedding = 4
    sentence_embedding = 5


class Task(object):
    def __init__(self, task_id: str, data: dict):
        self.id = task_id
        self.type = data["task_type"]
        self.sentence = data.get("sentence", Const.texts.sentence)
        self.sentence_list = data.get("sentence_list", [])
        self.word = data.get("word", "")
        self.word_list = data.get("word_list", [])

    def __str__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)


class Dispatch(object):
    def __init__(self, nlp_worker):
        self.nlp_worker = nlp_worker

    def collect_tasks(self) -> dict:
        try:
            resp = Const.redis.blpop(Const.nlp_list, timeout=60)
            if resp:
                _json = json.loads(resp[1].decode())
                cf.info("task_data:", _json)
                return _json
        except:
            return {}

    def dispatch(self, task_data: dict) -> bool:
        task = Task(task_data["task_id"], task_data["data"])
        cf.info("task:", task)

        if task.type == TaskTypeEnum.token.name:
            resp = self.nlp_worker.jieba(task.sentence)
        elif task.type == TaskTypeEnum.batch_token.name:
            resp = self.nlp_worker.batch_token(task.sentence_list)
        elif task.type == TaskTypeEnum.word_embedding.name:
            resp = self.nlp_worker.word_embedding(task.word)
        elif task.type == TaskTypeEnum.batch_word_embedding.name:
            resp = self.nlp_worker.batch_word_embedding(task.word_list)
        else:
            return False
        cf.info("resp:", resp)
        resp = json.dumps({"result": resp})
        Const.redis.lpush(task.id, resp)
        return True

    def loop(self):
        while True:
            task_data = self.collect_tasks()
            if task_data:
                self.dispatch(task_data)


if __name__ == '__main__':
    myconsts.init()
    dispatch = Dispatch(NlpWorker())
    threads = [threading.Thread(target=dispatch.loop) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
