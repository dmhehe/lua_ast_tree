# -*- coding: UTF-8 -*-


class TXToken:
	def __init__(self, fileName, sText, sType, rowStart, colnumStart, rowEnd, colnumEnd, iStartIndex):
		self.m_sFileName = fileName
		self.m_iRowStart = rowStart
		self.m_iColnumStart= colnumStart
		self.m_iRowEnd = rowEnd
		self.m_iColnumEnd= colnumEnd
		self.m_iStartIndex = iStartIndex
		self.m_sText = sText
		self.m_sType = sType
		self.m_iLen = len(self.m_sText)

 
	def GetType(self):
		return self.m_sType

	def GetText(self):
		return self.m_sText
	
	
	def GetColnumStart(self):
		return self.m_iColnumStart
 
	def GetRowStart(self):
		return self.m_iRowStart
 
	def GetColnumEnd(self):
		return self.m_iColnumEnd
 
	def GetRowEnd(self):
		return self.m_iRowEnd
 
 
	def GetStr(self):
		str1 = "sType:{} sText:{} iRowStart:{} iColnumStart:{} iRowEnd:{} iColnumEnd:{}".format(self.m_sType, self.m_sText, 
		self.m_iRowStart, self.m_iColnumStart, 	self.m_iRowEnd, self.m_iColnumEnd)
		return str1

	def __str__(self):
		return self.GetStr()

	def Print(self):
		print(self.GetStr())
  
	def PrintData(self, level=0):
		str1 = ""
		if level > 0:
			str1 = "	"*level
		str1 += self.m_sText
		print(str1)

 
	def GetStartIndex(self):
		return self.m_iStartIndex

	def GetTextData(self):
		return self.m_sText

	