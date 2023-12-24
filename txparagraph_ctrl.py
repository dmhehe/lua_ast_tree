# -*- coding: UTF-8 -*-

import txtool
import txtoken

import txkeyword
import txsentence_ctrl

import txparagraph


g_RepeatParagraph = ["repeat", "data", "until", "data"]
g_WhileParagraph = ["while", "data", "do", "Paragraph", "end"]
g_ForParagraph = ["for", "data", ["=", "in"], "data", "do", "Paragraph", "end"]
g_IfParagraph = ["if", "data", "then", "Paragraph", (["elseif", "Paragraph", "then"], ["else", "Paragraph"], ["end",])]
g_FuncParagraph = ["function", "data", "(", "data", ")", "Paragraph", "end"]
g_DoParagraph = ["do", "Paragraph", "end"]

g_ParagraphDict = {
	g_WhileParagraph[0]: g_WhileParagraph,
	g_ForParagraph[0]: g_ForParagraph,
	g_IfParagraph[0]: g_IfParagraph,
 	g_FuncParagraph[0]: g_FuncParagraph,
	g_DoParagraph[0]: g_DoParagraph,
}

  




class TXParagraphCtrl:
	def __init__(self, textFile, fileData=None):
		import txtoken_ctrl
		ctrlObj = txtoken_ctrl.TxTokenCtrl(textFile, fileData)

		self.m_listToken = ctrlObj.GetNoNodeTokenList()
		self.m_FuncSectionList = []
		self.m_ParagraphStack = []

		self.m_ParagraphAnsList = []
  
		self.m_curSection = None

 
	def GetCurParagraph(self):
		iLen = len(self.m_ParagraphStack)
		if iLen <= 0:
			return None

		return self.m_ParagraphStack[iLen-1]

	def PushParagraph(self, ParagraphObj):
		parentObj = self.GetCurParagraph()
		if parentObj:
			parentObj.AddDataList(ParagraphObj)
		self.m_ParagraphStack.append(ParagraphObj)
	
	def PopParagraph(self):
		ParagraphObj = self.m_ParagraphStack.pop()

		# if len(self.m_ParagraphStack) <= 0:
		# 	if ParagraphObj:
		# 		ParagraphObj.PrintData()

		return ParagraphObj
	
 
	def CheckCanAddParagraph(self, sType, sText, sTypeNext, sTextNext):
		if not (sType == "Keyword" and sText in g_ParagraphDict):
			return None

		# print("ccccccccccccccccccccccc", sText, sTypeNext, sTextNext)
		if sText == "function" and sTypeNext == "Symbol" and sTextNext == "(":
			return "bCanData"


		ParagraphObj = self.GetCurParagraph()   #解决Do需要的问题
		if ParagraphObj and ParagraphObj.CountIsNeedKeyword(sText):
			return None
  
		return "true"
 
	def GetFunctionTree(self): #获取主要函数树
		self.m_TreeTokenList = []
		for i in range(0, len(self.m_listToken)):
			tokenObj = self.m_listToken[i]
			sType = tokenObj.GetType()
			sText = tokenObj.GetText()
			nextI = i+1
			tokenObjNext = None
			sTypeNext = None
			sTextNext = None
			if len(self.m_listToken) > nextI:
				tokenObjNext = self.m_listToken[nextI]
				sTypeNext = tokenObjNext.GetType()
				sTextNext = tokenObjNext.GetText()

			iColnumStart = tokenObj.GetColnumStart()

			sCan = self.CheckCanAddParagraph(sType, sText, sTypeNext, sTextNext)
			if sCan:
				ParagraphList = g_ParagraphDict[sText]
				bCan = sCan == "bCanData"
				newParagraphObj = txparagraph.TXParagraph(sText, ParagraphList, bCan)
				self.PushParagraph(newParagraphObj)
			
			
			ParagraphObj = self.GetCurParagraph()
			if ParagraphObj:
				ParagraphObj.EatToken(tokenObj)
				if ParagraphObj.IsFinish():
					self.PopParagraph()
					if not self.GetCurParagraph():
						self.m_TreeTokenList.append(ParagraphObj)
			else:
				self.m_TreeTokenList.append(tokenObj)
	
 
	def MakeTXSentenceCtrl(self, list1, treeList):
		if len(list1) <= 0:
			return

		sobj = txsentence_ctrl.TXSentenceCtrl()
		sentenceList = sobj.DoMake(list1)
		list1.clear()
		treeList.extend(sentenceList)
	
	def MakeTree(self):
		
		self.m_TreeList = []
		list1 = []
		for obj in self.m_TreeTokenList:
			if isinstance(obj, txtoken.TXToken):
				list1.append(obj)
				continue
			
			if isinstance(obj,  txparagraph.TXParagraph) and obj.IsCanData():
				list1.append(obj)
				continue
			
			if isinstance(obj, txparagraph.TXParagraph):
				if list1:
					self.MakeTXSentenceCtrl(list1, self.m_TreeList)

				obj.MakeSentence()
				self.m_TreeList.append(obj)
				continue
			txtool.PrintErr("不会来到这里")

		self.MakeTXSentenceCtrl(list1, self.m_TreeList)

	def GetTreeList(self):
		return self.m_TreeList
 
	def PrintTree(self):
		level = 0
		for tobj in self.m_TreeList:
			tobj.PrintData(level)
   
