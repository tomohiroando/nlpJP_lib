# -*- coding: utf-8 -*-

import mecab_lib
import collections as cl

def splitStr(str, num):
	l = []
	for i in range(num):
		l.append(str[i::num])
	l = ["".join(i) for i in zip(*l)]
	rem = len(str) % num
	if rem:
		l.append(str[-rem:])
	return l

def classifyPos(words, pos_list=["名詞","動詞","形容詞"]):

	stop_words = ["こと", "もの"]

	texts = []
	for token in words.list:
		if (token.surface in stop_words) or (len(token.surface) == 1): continue
		elif token.pos in pos_list:
			if token.basic_form == "*":
				texts.append(token.surface)
			else:
				texts.append(token.basic_form)
	return texts

def classifyPos_proper(words, pos_list=["固有名詞"]):

	stop_words = ["こと", "もの"]

	texts = []
	for token in words.list:
		if (token.surface in stop_words) or (len(token.surface) == 1): continue
		elif token.pos_detail1 in pos_list:
			if token.basic_form == "*":
				texts.append(token.surface)
			else:
				texts.append(token.basic_form)
	return texts

def make_proper_dict(words, pos_list=["固有名詞"]):
    body_list = []
    for i in range(len(words.list)):
        if(words.list[i].surface == ""):
            continue
        else:
            proper_dict = cl.OrderedDict()
            proper_dict["text"] = words.list[i].surface
            #proper_dict["id"] = num
            #num += 1
            if(words.list[i].pos_detail1 in pos_list):
                proper_dict["is_prior_noun"] = True
            else:
                proper_dict["is_prior_noun"] = False
            proper_dict["porality"] = None
            body_list.append(proper_dict)
    return body_list

def shapePos(words, pos_list=["名詞","動詞","形容詞","副詞","感動詞","連体詞"]):
    texts = []
    for token in words.list:
        if token.pos in pos_list:
            if token.basic_form == "*":
                texts.append(token.surface)
            else:
                texts.append(token.basic_form)
    return texts

def shapePos2(words, prior_list, pos_list = ["名詞","動詞","形容詞","副詞","感動詞","連体詞"]):
    texts = []
    if (len(prior_list) != 0):
        prior = prior_list.pop(0)
    else:
        prior = None
    for token in words.list:
        if (prior != None) and (prior[0] == token.surface):
            texts.append([prior[0],prior[2]])
            if(len(prior_list)!=0):
                prior = prior_list.pop(0)
            else:
                prior = None
            continue
        else:
            if token.pos in pos_list:
                if token.basic_form == "*":
                    texts.append(token.surface)
                else:
                    texts.append(token.basic_form)
            if (token.pos == "助動詞") and (token.basic_form == "ない"):

                gokan = texts[-1]
                texts[-1] = (gokan, 'ない')
                # print(texts)
    if(len(prior_list)!=0):
        print(prior_list)
        print(texts)
    return texts


def tokenize(text):
	#pos_list=["名詞","動詞","形容詞"]
	words = mecab_lib.Tokens(text)#ここでできるのはトークンのインスタンス
	texts = classifyPos(words)
	return texts

def shape_corpus(text):
    words = mecab_lib.Tokens(text)
    texts = shapePos(words)
    return texts


def proper(text):
	#pos_list=["名詞","動詞","形容詞"]
	words = mecab_lib.Tokens(text)#ここでできるのはトークンのインスタンス
	texts = classifyPos_proper(words)
	return texts

def oreore(text):
    words = mecab_lib.Tokens(text)#ここでできるのはトークンのインスタンス
    body_list = make_proper_dict(words)
    return body_list

def oreore2(text,prior_list):
    words = mecab_lib.Tokens(text)
    sentence_list = mendoi(words, prior_list)
    return sentence_list



