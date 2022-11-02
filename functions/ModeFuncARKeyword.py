import time
import PySimpleGUI as sg
import pyautogui

from functions.setGUI import setGUI
from functions.common import Reset_Game, CheckTappedArea
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def updateDictProc_ARKeyword(dictProc):
	dictProc_this = {
		"ARENTRY"     : AREntry_ModeProc,
		"ARWORD1"     : ARWord1_ModeProc,
		"ARWORD2"     : ARWord2_ModeProc,
		"ARWORD3"     : ARWord3_ModeProc,
		"ARWORD4"     : ARWord4_ModeProc,
		"ARWRONG"     : ARWrong_ModeProc,
		"ARCORRECT"   : ARCorrect_ModeProc,
		"AREND"       : AREnd_ModeProc,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_ARKeyword(dictWindow):
	layoutAREntry = make_fullimage_layout("images/AR_Enter.png", "ARENTRY")
	layoutARWord1 = make_4choice_layout("images/AR_Word1.png", ["メ", "ロ", "カ", "ラ"])
	layoutARWord2 = make_4choice_layout("images/AR_Word2.png", ["リ", "ス", "イ", "ク"])
	layoutARWord3 = make_4choice_layout("images/AR_Word3.png", ["キョ", "キャ", "キッ", "キュ"])
	layoutARWord4 = make_4choice_layout("images/AR_Word4.png", ["ーン", "アップ", "ウ", "ル"])
	layoutARWrong = make_fullimage_layout("images/wrong.png", "ARWRONG")
	layoutARCorrect = make_fullimage_layout("images/correct.png", "ARCORRECT")
	layoutAREND = make_fullimage_layout("images/AR_End.png", "AREND")

	dictLayout = {
		"ARENTRY"     : layoutAREntry,
		"ARWORD1"     : layoutARWord1,
		"ARWORD2"     : layoutARWord2,
		"ARWORD3"     : layoutARWord3,
		"ARWORD4"     : layoutARWord4,
		"ARWRONG"     : layoutARWrong,
		"ARCORRECT"   : layoutARCorrect,
		"AREND"       : layoutAREND,
    }
	dictWindow_this = setGUI(dictLayout)
	
	return dict(dictWindow, **dictWindow_this)

def AREntry_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "ARENTRY":
		dictArgument["Start time"] = cState.updateState("ARWORD1")

def ARWord1_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudioOut = dictArgument["AudioOut"]

	if event == "メ":
		dictArgument["Start time"] = cState.updateState("ARWORD2")
	elif event == "ロ" or event == "カ" or event == "ラ":
		cAudioOut.playSoundAsync("sound/wrong_24.wav")
		dictArgument["Start time"] = cState.updateState("ARWRONG")

def ARWord2_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudioOut = dictArgument["AudioOut"]

	if event == "イ":
		dictArgument["Start time"] = cState.updateState("ARWORD3")
	elif event == "リ" or event == "ス" or event == "ク":
		cAudioOut.playSoundAsync("sound/wrong_24.wav")
		dictArgument["Start time"] = cState.updateState("ARWRONG")

def ARWord3_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudioOut = dictArgument["AudioOut"]

	if event == "キュ":
		dictArgument["Start time"] = cState.updateState("ARWORD4")
	elif event == "キョ" or event == "キャ" or event == "キッ":
		cAudioOut.playSoundAsync("sound/wrong_24.wav")
		dictArgument["Start time"] = cState.updateState("ARWRONG")

def ARWord4_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudioOut = dictArgument["AudioOut"]

	if event == "ウ":
		cAudioOut.playSoundAsync("sound/correct_24.wav")
		dictArgument["Start time"] = cState.updateState("ARCORRECT")
	elif event == "ーん" or event == "アップ" or event == "ル":
		cAudioOut.playSoundAsync("sound/wrong_24.wav")
		dictArgument["Start time"] = cState.updateState("ARWRONG")

def ARWrong_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if time.time() - dictArgument["Start time"] >= 2:
		dictArgument["Start time"] = cState.updateState("ARWORD1")

def ARCorrect_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if time.time() - dictArgument["Start time"] >= 2:
		cCtrlCard.write_result("ar_labyrinth", "T")
		dictArgument["Start time"] = cState.updateState("AREND")


def AREnd_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "AREND":
		cState.dictWindow["SELECT_GAME"]["AR\nラビリンス"].update(disabled=True)
		if cCtrlCard.checkComplete():
			dictArgument["Start time"] = cState.updateState("ENDING")
		else:
			dictArgument["Start time"] = cState.updateState("SELECT_GAME")
