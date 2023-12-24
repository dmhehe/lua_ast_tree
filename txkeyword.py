# -*- coding: UTF-8 -*-

import txtool

class TXKeyword:
	def __init__(self, sType, strText, endText):
		self.m_strText = strText
		self.m_EndText = endText
		self.m_sType = sType

	def GetType(self):
		return self.m_sType

	def GetEndText(self):
		return self.m_EndText

	def GetStrText(self):
		return self.m_strText

	def GetStr(self):
		str1 = "sType:{} strText:{} endText:{}".format(self.m_sType, self.m_strText, self.m_EndText)
		return str1

	def __str__(self):
		return self.GetStr()



TK_NODE = 1  #注释
TK_FLOAT = 2
TK_INT = 3
TK_STRING = 4




g_KeywordList = [
    "not", "and", "or",
    "function", "nil", "end", 
    "for", "while", "do", "break", "in", "return", "until", "goto", "repeat",
	"true", "false",
	"then", "if", "elseif", "else",
	"local",
	"break",
]

g_KeywordDict = txtool.MakeDict(g_KeywordList)

def IsKeyword(str1):
    return str1 in g_KeywordDict




g_SymbolList = [
    ".", ":", 
    "=",
    "[", "]",
    "<<", ">>",
	"+", "-", "*", "/", "%", 
	"^", "~", "&", "|", "..", "#",
	
 	",", ";", 
	
	"(", ")", "{", "}",
 	"==", "~=", "<" , ">",
	"<=", ">=",
	"...",
]


g_NodeList = [
	"--", 
]


g_MulNodeList = [
	[ "--[[", "]]"],
]


g_StringList = [
	["\"", "\""],
	["\'", "\'"],
]


g_MulStringList = [
	[ "[[", "]]"],
]





g_Char2WordDict = {
}

def GetStartStr2Keyword(str1):
	if str1 not in g_Char2WordDict:
		return None
	return g_Char2WordDict[str1]



g_WordDict  = {
	
}




def InitKeywordDict():
	

	# for sText in g_KeywordList:
	# 	g_WordDict[sText] = TXKeyword("Keyword", sText)

	for strText, endText in g_MulStringList:
		g_WordDict[strText] = TXKeyword("MulString", strText, endText)


	for strText, endText in g_MulNodeList:
		g_WordDict[strText] = TXKeyword("MulNode", strText, endText)

	for strText, endText in g_StringList:
		g_WordDict[strText] = TXKeyword("String", strText, endText)
  
	
	for sText in g_NodeList:
		g_WordDict[sText] = TXKeyword("Node", sText, None)



	for sText in g_SymbolList:
		g_WordDict[sText] = TXKeyword("Symbol", sText, None)



	lst = list(g_WordDict.keys())
 
	lst.sort(key=lambda x:-1*len(x))

	for sText in lst:
		KeywordObj = g_WordDict[sText]
		for i in range(len(sText)):
			newword = sText[0:i+1]
			g_Char2WordDict[newword] = KeywordObj

 
 
	# for sText, KeywordObj in g_Char2WordDict.items():
	# 	print(sText, KeywordObj)

	
	# g_WordDict[TK_NODE] = TXKeyword(TK_FLOAT, "")
	# g_WordDict[TK_FLOAT] = TXKeyword(TK_FLOAT, "")
	# g_WordDict[TK_INT] = TXKeyword(TK_FLOAT, "")
	# g_WordDict[TK_STRING] = TXKeyword(TK_FLOAT, "")
 
 
 
    

InitKeywordDict()


