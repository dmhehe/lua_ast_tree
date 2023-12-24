# -*- coding: UTF-8 -*-

import txtool
import txtoken



class TXSentence:
	def __init__(self, dataList):
		self.m_TreeList = dataList
  
		self.m_iColnumStart = None
		self.m_iColnumEnd = None
		self.m_iRowStart = None
		self.m_iRowEnd = None
  
	
	def GetTreeList(self):
		return self.m_TreeList

	def MakeDataList(self):
		import txparagraph
		for tobj in self.m_TreeList:
			if isinstance(tobj, txparagraph.TXParagraph):
				tobj.MakeSentence()

		startObj = self.m_TreeList[0]
		endObj = self.m_TreeList[-1]

		self.m_iColnumStart = startObj.GetColnumStart()
		self.m_iRowStart = startObj.GetRowStart()
		self.m_iColnumEnd = endObj.GetColnumEnd()
		self.m_iRowEnd = endObj.GetRowEnd()
  
	def PrintData(self, level=0):
		str1 = "(TXSentence)"
		print(str1)
		for tobj in self.m_TreeList:
			tobj.PrintData(level+1)

	def GetTextData(self):
		list1 = []
		for tobj in self.m_TreeList:
			list1.append(tobj.GetTextData())
		return "".join(list1)



	def GetColnumStart(self):
		return self.m_iColnumStart
 
	def GetRowStart(self):
		return self.m_iRowStart
 
	def GetColnumEnd(self):
		return self.m_iColnumEnd
 
	def GetRowEnd(self):
		return self.m_iRowEnd