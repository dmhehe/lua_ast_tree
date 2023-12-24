# -*- coding: UTF-8 -*-

import os
import txtool
import txlua
import txtoken_ctrl
import txkeyword
import txparagraph_ctrl


g_TextFile = r"H:\pcclient1\lua\csdebug.lua"


def CheckNameList(list1, name):
    pass


def Main():
    print("txlua txlua！！！！！！！！！！！！！")

    lst = txtool.GetLuaFileList(None)
    lst.sort(reverse=True)
    # print("xxxxxxxxxxxxxx", lst)
    # for textFile in lst:
    #     objCtrl = txtoken_ctrl.TxTokenCtrl(textFile)
    #     print(objCtrl.PrintTokenList())
    
    
    
    
    # for textFile in lst:
    #     treeObj = txparagraph_ctrl.TXParagraphCtrl(textFile)
    #     treeObj.GetFunctionTree()
        
        
    for textFile in lst:
        print("ccccccccccccccccccccc", textFile)
        treeObj = txparagraph_ctrl.TXParagraphCtrl(textFile)
        treeObj.GetFunctionTree()
        treeObj.MakeTree()
    #     treeObj.PrintTree()
    
    
    # treeObj = txparagraph_ctrl.TXParagraphCtrl(g_TextFile)
    # treeObj.GetFunctionTree()
    # treeObj.MakeTree()
    # treeObj.PrintTree()