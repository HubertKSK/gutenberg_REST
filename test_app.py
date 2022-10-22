#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase

import requests

BASE = "http://127.0.0.1:8080"


class Test(TestCase):
    def test_count_words(self):
        response = requests.get(BASE + "/count_word&https://www.gutenberg.org/files/2701/2701-0.txt&CHAPTER")
        assert response.status_code == 200
        assert response.json() == {"chapter": 308}

    def test_top10(self):
        response = requests.get(BASE + "/top10&https://www.gutenberg.org/files/2701/2701-0.txt")
        assert response.status_code == 200
        assert response.json() == [['the', 14535], ['of', 6624], ['and', 6447], ['a', 4747], ['to', 4627], ['in', 4184], ['that', 3085], ['his', 2532], ['it', 2522], ['i', 2127]]

    def test_similar(self):
        response = requests.get(
            BASE + "/similar&https://www.gutenberg.org/files/2701/2701-0.txt&CHAPTER")
        assert response.status_code == 200
        assert response.json() == ['chapter', 'chapters', 'charter', 'hater', 'caper', 'haters', 'hamper', 'halter', 'crater', 'chaste']
