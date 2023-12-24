# -*- coding: UTF-8 -*-
import txtool
import txtoken

import txkeyword
import txsentence_ctrl


class TXParagraph:
	def __init__(self, name, lst, bCanData=False):
		self.m_Name = name
		self.m_List = lst
		self.m_idxCur = -1
		self.m_tokenList = []
		self.m_HittokenList = []
  
		self.m_iColnumStart = None
		self.m_iColnumEnd = None
		self.m_iRowStart = None
		self.m_iRowEnd = None


		self.bCanData = bCanData
  
		self.m_DataList = []
		self.m_ChildParagraphList = []
  
		self.ClearNeedData()
		self.MoveNextKeyword()
	
 
	def GetType(self):
		if self.bCanData:
			return "DataParagraph"

		return "Paragraph"

	def GetText(self):
		return ""
 
	def IsCanData(self):
		return self.bCanData
 
	def AddDataList(self, pobj):
		self.m_DataList.append(pobj)
  
	def GetName(self):
		return self.m_Name
 

	def GetColnumStart(self):
		return self.m_iColnumStart
 
	def GetRowStart(self):
		return self.m_iRowStart
 
	def GetColnumEnd(self):
		return self.m_iColnumEnd
 
	def GetRowEnd(self):
		return self.m_iRowEnd

 
	def MoveKeyFunc(self, idx, moveList):
		idx += 1
		iStart = idx
		for i in range(iStart, len(moveList)):
			sText = self.m_List[i]
			if sText != "Paragraph" and sText != "data":
				idx = i
				break
		else:
			idx = len(moveList)

		keyword = None
  
		if idx < len(moveList):
			keyword = moveList[idx]

		return idx, keyword
 
	def MoveNextKeyword(self):
		keyword = None
		if self.m_LoopWordList != None:
			self.m_CurNeedLoopWordIdx, keyword = self.MoveKeyFunc(self.m_CurNeedLoopWordIdx, self.m_LoopWordList)
			
			self.m_CurNeedLoopWord = keyword
			if self.m_CurNeedLoopWord == None:
				if self.m_HitKeyword == "end": #不是end， 就一直在循环体内了
					self.m_idxCur += 1
					self.ClearNeedData()
					return
				
				self.CountNeedKeyword()
			return

		self.m_idxCur, keyword = self.MoveKeyFunc(self.m_idxCur, self.m_List)
		self.m_NeedWord = keyword
		self.CountNeedKeyword()
  
	def IsFinish(self):
		return len(self.m_List) <= self.m_idxCur
	
	
 
	def CountNeedKeyword(self):  
		if type(self.m_NeedWord) == type(()):
			list1 = list(self.m_NeedWord)
			self.ClearNeedData()
			self.m_bLoopWord = True
			self.m_StartLoopWordList = list1
		
 
	def ClearNeedData(self):
		self.m_HitKeyword = None  #命中的关键字
     
		self.m_NeedWord = None  #单个关键词匹配
		
		self.m_bLoopWord = False
		self.m_StartLoopWordList = None
		self.m_LoopWordList = None
		self.m_CurNeedLoopWord = None
		self.m_CurNeedLoopWordIdx = 0

 
	def CheckOneKeyWord(self, sText, keyWord):
		if type(keyWord) == type(""):
			return sText == keyWord

		return sText in keyWord

 
	def CountIsNeedKeyword(self, sText):
		if self.m_bLoopWord:
			if self.m_CurNeedLoopWord:
				return self.CheckOneKeyWord(sText, self.m_CurNeedLoopWord)
			else:
				for lst1 in self.m_StartLoopWordList:
					keyWord = lst1[0]
					if self.CheckOneKeyWord(sText, keyWord):
						self.m_LoopWordList = lst1
						self.m_CurNeedLoopWordIdx = 0
						return True
			return False

		return self.CheckOneKeyWord(sText, self.m_NeedWord)
 
	def EatToken(self, tokenObj):
		self.m_tokenList.append(tokenObj)
		self.m_DataList.append(tokenObj)
		sType = tokenObj.GetType()
		sText = tokenObj.GetText()
		

		if self.m_iColnumStart == None:
			self.m_iColnumStart = tokenObj.GetColnumStart()
			self.m_iRowStart = tokenObj.GetRowStart()
  
		if (sType == "Keyword" or sType == "Symbol") and self.CountIsNeedKeyword(sText):
			self.m_HitKeyword = sText
			self.m_HittokenList.append(tokenObj)
			self.MoveNextKeyword()

		if self.IsFinish():
			self.m_iColnumEnd = tokenObj.GetColnumEnd()
			self.m_iRowEnd = tokenObj.GetRowEnd()
   
		# print("jjjjjjjjjjjjjjjjjjjj", self.m_idxCur)
	


	def MakeTXSentenceCtrl(self, list1, treeList):
		if len(list1) <= 0:
			return

		sobj = txsentence_ctrl.TXSentenceCtrl()
		sentenceList = sobj.DoMake(list1)
		list1.clear()
		treeList.extend(sentenceList)

 
	def MakeSentence(self):
		self.m_TreeList = []
		import txsentence_ctrl
		list1 = []
		for i in range(0, len(self.m_DataList)):
			obj = self.m_DataList[i]
			if isinstance(obj, TXParagraph):
				obj.MakeSentence()
				if obj.IsCanData():
					list1.append(obj)
					continue
				
				if list1:
					self.MakeTXSentenceCtrl(list1, self.m_TreeList)
				self.m_TreeList.append(obj)
				continue
			
			if obj in self.m_HittokenList:
				if list1:
					self.MakeTXSentenceCtrl(list1, self.m_TreeList)
				self.m_TreeList.append(obj)
			else:
				list1.append(obj)
	
		self.MakeTXSentenceCtrl(list1, self.m_TreeList)
 
	def PrintData(self, level=0):
		str1 = "(TXParagraph)"
		print(str1)
		for tobj in self.m_TreeList:
			tobj.PrintData(level+1)

	def GetTextData(self):
		list1 = []
		for tobj in self.m_TreeList:
			list1.append(tobj.GetTextData())
		return "".join(list1)


	def GetFunctionName(self):
		if self.m_Name != "function":
			return ""

		funcName = ""
  
		list1 = []
		list2 = []
		bFirst = False
		for i in range(1, len(self.m_tokenList)):
			tokenObj = self.m_tokenList[i]
			sType = tokenObj.GetType()
			sText = tokenObj.GetText()
			if sText == "(":
				break
			
			list1.append(tokenObj)
			funcName += sText
		
		
		for i in range(1, len(self.m_tokenList)):
			tokenObj = self.m_tokenList[i]
			sType = tokenObj.GetType()
			sText = tokenObj.GetText()

			if sText == "end":
				break
			
			list2.append(tokenObj)
   
			if sText == ")" and bFirst == False:
				list2.clear()
				bFirst = True
		import txsentence_ctrl
		sobj = txsentence_ctrl.TXSentenceCtrl()
		sobj.DoMake(list2)
  
		return funcName
	
 
 
