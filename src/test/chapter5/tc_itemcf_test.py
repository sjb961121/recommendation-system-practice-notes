#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: main.py
@time: 2020/4/20 19:14
@project: recommendation-system-practice-notes
@desc: 时间上下文相关的ItemCF算法测试
"""
import os
import sys

import pandas as pd

from main.chapter5.tc_itemcf import TCItemCF
from main.util import delicious_reader, metric

PROJECT_ROOT = os.path.dirname(sys.path[0])
user_bookmark_path = os.path.join(PROJECT_ROOT, "../data/delicious-2k/user_taggedbookmarks-timestamps.dat")
bookmarks_path = os.path.join(PROJECT_ROOT, "../data/delicious-2k/bookmarks.dat")

original_dataset = delicious_reader.load_data(bookmarks_path, user_bookmark_path)

train_dataset, test_dataset = delicious_reader.split_data(
    delicious_reader.filter_dataset(original_dataset, "www.nytimes.com"))
model = TCItemCF(train_dataset)
model.fit()


def evaluate(model, test_dataset, N, K=None):
    """
    评估模型
    :param N: 推荐的商品个数
    :param K: 搜索邻近的用户个数
    :return: 精确率(precision), 召回率(recall)
    """
    test_dataset = delicious_reader.get_all_items(test_dataset)

    recommens = model.recommend_users(test_dataset.keys(), N=N, K=K)

    recall = metric.recall(recommends=recommens, tests=test_dataset)
    precision = metric.precision(recommends=recommens, tests=test_dataset)

    return precision, recall


metric_value = list()
K = 10
N_list = [i for i in range(10, 110, 10)]

for N in N_list:
    single_eval = evaluate(model, test_dataset, N, K)
    metric_value.append(single_eval)

result_df = pd.DataFrame(
    data=metric_value,
    index=['N=' + str(i) for i in N_list],
    columns=["Precision", "Recall"]
)
print(result_df)
