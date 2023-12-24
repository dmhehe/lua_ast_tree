# -*- coding: UTF-8 -*-

import txtool
import txtoken
import txkeyword


class TxTokenCtrl:
	def __init__(self, fileName, fileData=None):
		self.m_totkenSM = TXStateMachine(fileName, fileData)
		self.m_totkenSM.DoTranslate()
		self.m_listToken = self.m_totkenSM.GetListToken()
		self.m_idxStart = 0

	def PopToken(self):
		if self.m_idxStart >= len(self.m_listToken):
			return None

		self.m_idxStart += 1

		return self.m_listToken[self.m_idxStart]
	
	def GetTokenList(self):
		return self.m_listToken

	def GetNoNodeTokenList(self):
		list1 = []

		for tokenObj in self.m_listToken:
			sType = tokenObj.GetType()
			sText = tokenObj.GetText()
			if sType == "MulNode" or sType == "Node":
				continue
			list1.append(tokenObj)
		return list1
  

 
	def PrintTokenList(self):
		for tokenObj in self.m_listToken:
			print(tokenObj)


class TXReader:
	def __init__(self, fileName, fileData):
		self.m_sFileName = fileName
		self.m_sFileData = fileData
		self.m_sAllText = ""
		self.m_iCurIndex = -1
  
		self.m_iCurRow = 0
		self.m_iCurColnum = 1
		self.InitAllText()


	def InitAllText(self):
		self.m_iCurIndex = -1
		
		if self.m_sFileData != None:
			self.m_sAllText = self.m_sFileData
			return
		f = open(self.m_sFileName, "r", encoding="utf-8")
		self.m_sAllText = f.read()      #读取全部内容 ，并以列表方式返回  
		f.close()


	def GetNextChar(self):
		self.m_iCurIndex += 1
		if self.IsEnd():
			return None, None, None


		c = self.m_sAllText[self.m_iCurIndex]
		self.m_iCurRow += 1
		iRow = self.m_iCurRow
		iColnum = self.m_iCurColnum
		if c == "\n":
			self.m_iCurRow = 0
			self.m_iCurColnum += 1
		return c, iRow, iColnum


	def IsEnd(self):
		return self.m_iCurIndex >= len(self.m_sAllText)






TX_STATE_NONE = 1
TX_STATE_STRING = 2
TX_STATE_NUMBER = 3
TX_STATE_WORD = 7
TX_STATE_SYMBOL = 8
TX_STATE_SYMBOL_NODE = 9
TX_STATE_SYMBOL_MUL_NODE = 10
TX_STATE_SYMBOL_STRING = 11
TX_STATE_SYMBOL_MUL_STRING = 12

g_NumDict = {
"1":1,
"2":1,
"3":1,
"4":1,
"5":1,
"6":1,
"7":1,
"8":1,
"9":1,
"0":1,
}

g_Num16Str = "xabcdefABCDEF"
g_Num16List = list(g_Num16Str)

class TXStateMachine:
	def __init__(self, fileName, fileData=None):
		self.ClearState()

		self.m_AccStartIndex = 0
		self.m_objReader = TXReader(fileName, fileData)
		self.m_fileName = fileName
		self.m_listToken = []

	def GetListToken(self):
		return self.m_listToken

	def ClearState(self):
		self.m_stateCur = TX_STATE_NONE
		self.m_sCache = ""
		self.m_wordMaybe = None
		self.m_firstCache = ""


		self.m_iStartIndex = None
		self.m_iRowStart = None
		self.m_iColnumStart= None
		self.m_iRowEnd = None
		self.m_iColnumEnd = None
		self.m_NextCharInvalid = False  #搞字符串的时候用

	
 
	def GetLatestToken(self):
		iLen = len(self.m_listToken)
		if iLen > 0:
			return	self.m_listToken[iLen-1]

  
	def AddToken(self, sType):
		if sType == "Word" and txkeyword.IsKeyword(self.m_sCache):
			sType = "Keyword"
		
		tobj = txtoken.TXToken(self.m_fileName, self.m_sCache, sType, self.m_iRowStart, 
                             self.m_iColnumStart, self.m_iRowEnd, self.m_iColnumEnd, self.m_iStartIndex)
		self.m_listToken.append(tobj)
		self.ClearState()

	def CheckStateNormal(self, c, iRow, iColnum, iAccStartIndex):
		if txtool.IsEmptyChar(c):
			return

		self.m_firstCache = c
		self.m_sCache = c
		self.m_iRowStart = iRow
		self.m_iColnumStart = iColnum
		self.m_iStartIndex = iAccStartIndex

		wordObj = txkeyword.GetStartStr2Keyword(c)
		if wordObj != None:
			self.m_wordMaybe = wordObj
			self.m_stateCur = TX_STATE_SYMBOL
			self.AjustSymbolState()
		elif c in g_NumDict:
			self.m_stateCur = TX_STATE_NUMBER
		else:
			self.m_stateCur = TX_STATE_WORD

	def CheckNumber(self, c, iRow, iColnum, iAccStartIndex):
		fuList = (".", "e", "E")
		if c.isnumeric() or c in fuList:
			self.m_sCache += c
			return

		if c == "-" and (self.m_sCache.endswith("e") or self.m_sCache.endswith("E")):
			self.m_sCache += c
			return
  
		if (self.m_sCache.startswith("0") or self.m_sCache.startswith("-0")) and (c in g_Num16List or c.isnumeric()):
			self.m_sCache += c
			return
  
		self.AddToken("Number")
		self.CheckStateNormal(c, iRow, iColnum, iAccStartIndex)


	def CheckWord(self, c, iRow, iColnum, iAccStartIndex):
		if c.isalnum() or c == "_":
			self.m_sCache += c
			return
		
		self.AddToken("Word")
		self.CheckStateNormal(c, iRow, iColnum, iAccStartIndex)


	def CheckString(self, c, iRow, iColnum, iAccStartIndex):
		if c == "\n":
			if self.m_sCache.endswith("\\"):
				self.m_NextCharInvalid = False
				self.m_sCache = self.m_sCache[0:len(self.m_sCache)-1]
			else:
				txtool.PrintErr(iRow, iColnum, "语法错误")
				return
  
		invalid = False

		if self.m_NextCharInvalid:
			self.m_NextCharInvalid = False
			invalid = True
		elif c == "\\":
			self.m_NextCharInvalid = True
   
		self.m_sCache += c
		if c == self.m_firstCache and not invalid:
			self.m_iRowEnd = iRow
			self.m_iColnumEnd = iColnum
			self.AddToken("String")
			return
	
	def checkMulString(self, c, iRow, iColnum, iAccStartIndex):
		self.m_sCache += c
		endText = self.m_wordMaybe.GetType()
		if self.m_sCache.endswith(endText) and not self.m_sCache.endswith("\\"+endText):
			self.m_iRowEnd = iRow
			self.m_iColnumEnd = iColnum
			self.AddToken("MulString")
			return

 

	def CheckNode(self, c, iRow, iColnum, iAccStartIndex):
		self.m_sCache += c
		if c == "\n":
			self.AddToken("Node")
			return

		if self.m_sCache.startswith("--[["): #特殊处理
			self.m_stateCur = TX_STATE_SYMBOL_MUL_NODE
			return
		
  
	def CheckMulNode(self, c, iRow, iColnum, iAccStartIndex):
		self.m_sCache += c
		endText = self.m_wordMaybe.GetType()
		if self.m_sCache.endswith(endText):
			self.m_iRowEnd = iRow
			self.m_iColnumEnd = iColnum
			self.AddToken("MulNode")
			return

 
	def AjustSymbolState(self):
		sType = self.m_wordMaybe.GetType()
		self.m_stateCur = TX_STATE_SYMBOL
		if sType == "String":
			self.m_stateCur = TX_STATE_SYMBOL_STRING
			
		if sType == "Node":
			self.m_stateCur = TX_STATE_SYMBOL_NODE
			

		if sType == "MulNode":
			self.m_stateCur = TX_STATE_SYMBOL_MUL_NODE
   
		if sType == "MulString":
			self.m_stateCur = TX_STATE_SYMBOL_MUL_STRING
	
	def CheckCanChange2FuNumber(self, c):
		oldToken = self.GetLatestToken()
		if oldToken == None:
			return False

		if oldToken.GetType() == "Word":
			return False

		if oldToken.GetType() == "Symbol" and oldToken.GetText() == ")":
			return False
		
		return True
  
	def CheckSymbol(self, c, iRow, iColnum, iAccStartIndex):
		if self.m_sCache == "-" and c in g_NumDict and self.CheckCanChange2FuNumber(c):  #是数字的负号的话
			self.m_stateCur = TX_STATE_NUMBER
			self.CheckNumber(c, iRow, iColnum, iAccStartIndex)
			return

		str1 = self.m_sCache + c
		wordObj = txkeyword.GetStartStr2Keyword(str1)
		
		if wordObj != None:
			self.m_wordMaybe = wordObj
			self.m_sCache = str1
			self.AjustSymbolState()
			return

	
		self.AddToken("Symbol")
		self.ClearState()
		self.CountOneChar(c, iRow, iColnum, iAccStartIndex)



	def CountOneChar(self, c, iRow, iColnum, iAccStartIndex):
		if self.m_stateCur == TX_STATE_NONE:
			self.CheckStateNormal(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_SYMBOL:
			self.CheckSymbol(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_WORD:
			self.CheckWord(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_SYMBOL_STRING:
			self.CheckString(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_SYMBOL_NODE:
			self.CheckNode(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_SYMBOL_MUL_NODE:
			self.CheckMulNode(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_NUMBER:
			self.CheckNumber(c, iRow, iColnum, iAccStartIndex)
		elif self.m_stateCur == TX_STATE_SYMBOL_MUL_STRING:
			self.checkMulString(c, iRow, iColnum, iAccStartIndex)
  
		self.m_iRowEnd = iRow
		self.m_iColnumEnd = iColnum


	def DoCheckNext(self):
		
		c, iRow, iColnum = self.m_objReader.GetNextChar()

		if c == None:
			return

		self.CountOneChar(c, iRow, iColnum, self.m_AccStartIndex)
		self.m_AccStartIndex += len(c)

	def DoTranslate(self):
		self.m_AccStartIndex = 0
		for i in range(9999999999999):
			if self.m_objReader.IsEnd():
				break
			
			self.DoCheckNext()








	