# -*- coding: UTF-8 -*-

import os

def ReadAllFileLine(dir):
	f = open(dir,"r")   
	lst = []
	lines = f.readlines()      #读取全部内容 ，并以列表方式返回  
	f.close()
	for line1 in lines:
		str1 = line1.encode('utf-8').decode('utf-8')
		lst.append(str1)
	return lst


def IsEmptyChar(str1):
	return len(str1.strip()) == 0


def PrintErr(*str1):
	import traceback
	traceback.print_stack()
	print("!!!!!!!!!!!!!!!!!!!!!")
	print(str1)



def MakeDict(lst):
	dct = {}
	for str1 in lst:
		dct[str1] = 1
	return dct



def pt():
	import traceback
	traceback.print_stack()


def GetLuaFileList(file):
	if file == None or file == "":
		file = r"H:\pcclient1\lua"
	lst = []
	for root, dirs, files in os.walk(file):
		for file in files:
			path = os.path.join(root, file)
			if path.endswith(".lua"):
				lst.append(path)
	return lst



def PrintTokenList(list1):
	str1 = ""
	for tobj in list1:
		str1 += tobj.GetText()
	print(str1)
	return str1



def GetCMDAnsStr(str1):
	import subprocess
	# print("GetCMDAnsStr!!!!!", str1)
	p = subprocess.Popen(str1, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	try:
		ansStr = str(output, "utf-8")
	except Exception as e:
		ansStr = str(output)
	ansStr = ansStr.replace("\r\n", "\n")
 
	return ansStr


def WriteFile(fullFileName, dataStr):
	MakeDir(fullFileName)
	import codecs
	f = codecs.open(fullFileName, 'w', 'utf-8')
	f.write(dataStr)
	f.close()
 
 
def ReadFile(fullFileName):
	import codecs
	f = codecs.open(fullFileName, 'r', 'utf-8')
	ansStr = f.read()
	ansStr = ansStr.replace("\r\n", "\n")
	return ansStr
 
def MakeDir(fullFileName):
	idx = fullFileName.rfind("/")
	file_path = fullFileName
	if idx >= 0:
		file_path = fullFileName[0:idx]
  
	if os.path.exists(file_path) is False:
		os.makedirs(file_path)





def ReplaceStrByIndex(orgStr, replaceIndexList):
	iStartIdx = 0
	newList = []
	for (iStart, iEnd, sNewStr) in replaceIndexList:
		newList.append(orgStr[iStartIdx:iStart])
		newList.append(sNewStr)
		iStartIdx = iEnd
	newList.append(orgStr[iStartIdx:len(orgStr)])
	return "".join(newList)
