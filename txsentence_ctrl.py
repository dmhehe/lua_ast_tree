# -*- coding: UTF-8 -*-

import txtool
import txtoken

import txkeyword
import txsentence


g_MathlList2 = [
	"<<", ">>",
	"+", "-", "*", "/", "%", 
	"^", "~", "&", "|", "..",
]

g_DataDict = {
"keyWordData" : [["true", "false", "nil", "String", "MulString", "Number", "Word", "DataParagraph", "..."],],
"IndexData2" : ["data", [".", ":"], "data"],
"CallData" : ["data","(", "data", ")"],
"LogicData1" : ["not", "data"],
"LogicData2" : ["data",["or", "and"], "data"],
"CompareData" : ["data", ["==", "~=", "<" , ">", "<=", ">=",], "data"],
"DotData" : ["data", ",", "data"],
"MathData1" : ["#", "data"],
"MathData2" : ["data", g_MathlList2, "data"],


"IndexData1" : ["data", "[", "data", "]"],

"TableData"  : ["{", "data", "}"],
"TableData2" : ["[", "data", "]", "=", "data"],
"MathData3" : ["(", "data", ")"],

"AssignSentence1" : ["data", "=", "data"],
"AssignSentence2" : ["local", "data"],
"AssignSentence3" : ["local", "data", "=", "data"],
# "ReturnSentence1" : ["return"],
"ReturnSentence2" : ["return", "data"],
"Break":["break"],

}


STATE_SENTENCE_NEED_DATA = 1 #一开始的状态需要data
STATE_SENTENCE_HAS_DATA = 2	#已经有数据
STATE_SENTENCE_NEED_SYMBOL = 3  #后面需要某个符号




class TXSentenceCtrl:
	def __init__(self):
		self.m_SentenceList = []
		self.m_CurTokenList = []
		self.m_iColnumStart = None
		self.m_iColnumEnd = None
  
		self.Clear()
  
		self.m_StateList = []
	
	def GetSentenceList(self):
		return self.m_SentenceList
 
	def Clear(self):
		self.m_iState = STATE_SENTENCE_NEED_DATA
		self.m_NeedSymbol = None
		self.m_StateList = []
	
	def PrintCurTokenList(self):
		# txtool.pt()
		print("!!!!!!!!!!!!!!!!!!!!!!!")
		str1 = ""
		for tobj in self.m_CurTokenList:
			str1 += tobj.GetText()

		print(str1)
 
	def MakeNewSentence(self):
		# self.PrintCurTokenList()
		sobj = txsentence.TXSentence(self.m_CurTokenList)
		sobj.MakeDataList()
		self.m_SentenceList.append(sobj)
		self.m_CurTokenList = []
		
		self.Clear()
	
	def PushState(self, value):
		self.m_StateList.append(value)
	
	def IsStateEmpty(self):
		return len(self.m_StateList) <= 0
 
	def PopState(self):
		if len(self.m_StateList) <= 0:
			return None
		return self.m_StateList.pop()
 
	def IsStartNoneToken(self, tokenObj):
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
		for name, lst in g_DataDict.items():
			word = lst[0]
			if word == "data":
				continue
			if self.CheckWord(word, tokenObj):
				for i in range(len(lst)-1, 0, -1):
					newword = lst[i]
					self.PushState(newword)
				return True

		return False
				

 
	def ChangeStateFormStack(self, tokenObj=None):
		self.m_NeedSymbol = None
		val = self.PopState()
		if val == None:
    
			if tokenObj != None:
				self.m_iState = STATE_SENTENCE_HAS_DATA
				return
      
			if len(self.m_CurTokenList) > 0:
				self.m_iState = STATE_SENTENCE_HAS_DATA
			else:
				self.m_iState = STATE_SENTENCE_NEED_DATA
			return

		if "data" == val:
			self.m_iState = STATE_SENTENCE_NEED_DATA
			return

		
		self.m_iState = STATE_SENTENCE_NEED_SYMBOL
		self.m_NeedSymbol = val
		

	def CheckTokenStateNone(self, tokenObj):
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
  
		bOk =  self.IsStartNoneToken(tokenObj)
  
		if not bOk:
			if not self.IsStateEmpty():  #有些data是可以省略掉的  如 a()
				self.ChangeStateFormStack()
				self.CheckDoToken(tokenObj)
				return

			if self.IsStateEmpty() and len(self.m_CurTokenList)>0:
				self.MakeNewSentence()
				# self.m_NeedSymbol = None
				# self.m_iState = STATE_SENTENCE_NEED_DATA
				bOk2 = self.IsStartNoneToken(tokenObj)
				if bOk2:
					self.ChangeStateFormStack(tokenObj)
			else:
				txtool.PrintErr("语法错误3！！！")
			return
		
		self.ChangeStateFormStack(tokenObj)
	
 
 
	def IsStartDataToken(self, tokenObj):
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
		for name, lst in g_DataDict.items():
			word1 = lst[0]
			if word1 != "data" or len(lst) <= 1:
				continue
			
			word2 = lst[1]
			
			if self.CheckWord(word2, tokenObj):
				for i in range(len(lst)-1, 1, -1):
					newword = lst[i]
					self.PushState(newword)
				return True

		return False
	
 
 
	def CheckTokenStateHasData(self, tokenObj):
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()

		bOk =  self.IsStartDataToken(tokenObj)
  
		if not bOk:
			if self.IsStateEmpty():
				self.MakeNewSentence()
				bOk2 = self.IsStartNoneToken(tokenObj)
				if bOk2:
					self.ChangeStateFormStack(tokenObj)
			else:
				txtool.PrintErr("语法错误8！！！")
			return
		
		self.ChangeStateFormStack()
 
 
	def CheckTokenStateNeedSymbol(self, tokenObj):
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
  
		if (sType == "Keyword" or sType == "Symbol") and self.CheckWord(self.m_NeedSymbol, tokenObj):
			self.ChangeStateFormStack(tokenObj)
			return
		
  
		self.PushState(self.m_NeedSymbol)
		self.CheckTokenStateHasData(tokenObj)

	
 
	def  CheckDoToken(self, tokenObj):
		#print("ssssssssssssssssssssss", self.m_StateList, self.m_iState, tokenObj)
		if self.m_iState == STATE_SENTENCE_NEED_DATA:
			#print("11111111111111")
			self.CheckTokenStateNone(tokenObj)
  
		elif self.m_iState == STATE_SENTENCE_HAS_DATA:
			#print('22222222222222222222')
			self.CheckTokenStateHasData(tokenObj)

		elif self.m_iState == STATE_SENTENCE_NEED_SYMBOL:
			#print("33333333333333333333")
			self.CheckTokenStateNeedSymbol(tokenObj)
 
	def EatToken(self, tokenObj):
		
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
		if sType == "MulNode" or sType == "Node":
			return
  
		iColnumStart = tokenObj.GetColnumStart()
		if self.m_iColnumStart == None:
			self.m_iColnumStart = iColnumStart
		
		self.CheckDoToken(tokenObj)
		self.m_CurTokenList.append(tokenObj)


   

	def CheckWord(self, word, tokenObj): #判读这个是否符合模式条件
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
		name = sText
  
		if not (sType == "Keyword" or sType == "Symbol"):
			name = sType
 
		if type(word) == type(""):
			if name == word:
				return True
		elif name in word:
			return True

		return False

 
	def DoMake(self, tokenList):
		for tobj in tokenList:
			# print("ttttttttttttttttttt", tobj)
			self.EatToken(tobj)
		self.MakeNewSentence()
		return self.m_SentenceList
 
