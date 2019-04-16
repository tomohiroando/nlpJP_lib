#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MeCab

#tagger = MeCab.Tagger('-Ochasen')
tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger.parse('')

class Tokens(object):
	def __init__(self, text):
		self.text = text
		node = tagger.parseToNode(text)
		self.list = []
		while node:
			self.list.append(Token(node.surface, *node.feature.split(',')))
			node = node.next


class Token(object):
	"""形態素の情報"""
	def __init__(self, surface, *args):
		#node.surfaceには表層形が格納
		#Mecabのfeatureに格納されている情報
		#品詞, 品詞細分類1, 品詞細分類2, 品詞細分類3, 活用形, 活用型, 原型, 読み, 発音
		self.surface = surface
		try:
			self.pos = args[0]
			self.pos_detail1 = args[1]
			self.pos_detail2 = args[2]
			self.pos_detail3 = args[3]
			self.verb_form = args[4]
			self.verb_type = args[5]
			self.basic_form = args[6]
			self.ruby = args[7]
			self.pronunciation = args[8]
			self.type = True
		except IndexError:
			self.type = False

class Simple_Token(object):
	"""1形態素のみに行う場合"""
	def __init__(self, word):
		#Mecabのfeatureに格納されている情報
		#品詞, 品詞細分類1, 品詞細分類2, 品詞細分類3, 活用形, 活用型, 原型, 読み, 発音
		node = tagger.parseToNode(word)
		node = node.next
		self.surface = node.surface
		args = node.feature.split(',')
		try:
			self.pos = args[0]
			self.pos_detail1 = args[1]
			self.pos_detail2 = args[2]
			self.pos_detail3 = args[3]
			self.verb_form = args[4]
			self.verb_type = args[5]
			self.basic_form = args[6]
			self.ruby = args[7]
			self.pronunciation = args[8]
			self.type = True
		except IndexError:
			self.type = False


