#!/usr/bin/env python
# -*- coding: utf-8 -*-

import CaboCha
import numpy as np
c = CaboCha.Parser(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

class GetPair(object):

	def __init__(self, sentence):
		self.sentence = sentence#いらないかも
		self.pairs = []#空のリストの自己インスタンス
		tree = c.parse(sentence)
		dictionary = {}
		chunk_num = 0
		for i in range (tree.size()):
			token = tree.token(i)
			if token.chunk:#係り受けが存在する場合
				dictionary[chunk_num] = token.chunk
				chunk_num +=1
			
		for chunk_num, chunk in dictionary.items():
			if chunk.link > 0:
				from_word =  self.__get_chunk_formed(tree, chunk)#係り元の文節
				to_chunk = dictionary[chunk.link]#連結先のチャンク
				to_word = self.__get_chunk_formed(tree, to_chunk)#係り先の文節
				self.pairs.append((from_word, to_word))

	def __get_chunk_formed(self, tree, chunk):#助詞助動詞をのぞいて返す(基本形変換)
		word = ''
		for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
			token = tree.token(i)
			features = token.feature.split(',')
			if features[0] in  ['形容詞', '動詞']:
				word += features[6]
				break
			else:
				word += token.surface
				break
		return word

class GetPair2():

	def __init__(self, sentence):
		self.sentence = sentence#いらないかも
		self.pairs = []#空のリストの自己インスタンス
		tree = c.parse(sentence)
		dictionary = {}
		chunk_num = 0
		for i in range (tree.size()):
			token = tree.token(i)
			if token.chunk:#係り受けが存在する場合
				dictionary[chunk_num] = token.chunk
				chunk_num +=1
			
		for chunk_num, chunk in dictionary.items():
			if chunk.link > 0:
				# from_word =  self.__get_chunk_formed(tree, chunk)#係り元の文節
				from_word =  self.__get_chunk(tree, chunk)#係り元の文節
				to_chunk = dictionary[chunk.link]#連結先のチャンク
				# to_word = self.__get_chunk_formed(tree, to_chunk)#係り先の文節
				to_word = self.__get_chunk(tree, to_chunk)#係り先の文節
				self.pairs.append((from_word, to_word))

	def __get_chunk_formed(self, tree, chunk):#助詞助動詞をのぞいて返す(基本形変換)
		token = tree.token(chunk.token_pos)
		features = token.feature.split(',')
		if features[0] in  ['形容詞', '動詞']:
			word_li = [features[6],chunk.token_pos]
		else:
			word_li = [token.surface,chunk.token_pos]
		return word_li

	def __get_chunk(self, tree, chunk):#その文節の単語を全て連結する関数
		word_li = None
		for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
			token = tree.token(i)
			features = token.feature.split(',')
			if (features[0] != None) and (i == chunk.token_pos):
				word_li = [features[6],chunk.token_pos]
			elif (features[0] == '助動詞') and (features[6] == 'ない') and (word_li != None):
				word_li.append('ない')
		return word_li
		# pos_list = ["名詞","動詞","形容詞","副詞","感動詞","連体詞"]


def Info_CaboCha(text):
	tree = c.parse(text)
	for i in range(tree.chunk_size()):
		chunk = tree.chunk(i)
		print('Chunk', i)
		print('Score', chunk.score)
		print('Link', chunk.link)
		print('Size', chunk.token_size)
		print('Pos', chunk.token_pos)
		print('Head', chunk.head_pos)
		print('Func', chunk.func_pos)
		print('Features')
		for j in range(chunk.feature_list_size):
			print (chunk.feature_list(j))

		print('---------------------------------')

	for i in range(tree.token_size()):
		token = tree.token(i)
		print('Surface', token.surface)
		print('Normalized', token.normalized_surface)
		print('Feature', token.feature)
		print('NE:', token.ne)
		print('Info', token.additional_info)
		print('Chunk', token.chunk)

		print('----------------------------------')
	print('################################')


		
		

		
		
		
		
		

