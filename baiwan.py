# -*- coding:utf-8 -*-  

import urllib, base64, sys, json, time, os
from urllib import request
from PIL import ImageGrab
from http import cookiejar
from zhidao import zhidao_search
from PIL import ImageGrab

def grabScreen():
	image = ImageGrab.grab(bbox=(20, 150, 285, 225))  # 抓取屏幕
	image.save('screen.jpg')

# 获取百度API的许可口令
def getAccessToken():
	# client_id 为官网获取的AK， client_secret 为官网获取的SK
	client_id = "l5RVOjE4EnG4NxpIKvqloM6Q"
	client_secret = "PR7XUcll1lkGr43Auo113OQsj8TYKU5V"
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&\
			client_id=%s&client_secret=%s' % (client_id, client_secret)
	request = request.Request(host)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = request.urlopen(request)
	content = json.loads( response.read() )
	access_token = content['access_token']
	return access_token

def getOCR(picPath):
	access_token = "24.8a52714b73aa2338d5face06109eb3f1.2592000.1518097187.282335-10664264"
	# 百度文字识别API地址
	# url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
	url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
	# 二进制方式打开图文件
	f = open(picPath, 'rb')
	# 参数image：图像base64编码
	img = base64.b64encode(f.read())
	params = {
				"image": img,
				"language_type": "CHN_ENG"
			}
	params = urllib.parse.urlencode(params).encode(encoding='UTF8')
	request = urllib.request.Request(url, params)
	request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	response = urllib.request.urlopen(request)
	content = response.read().decode("utf-8")
	content = json.loads(content)
	ocrString = ""
	for item in content['words_result']:
		ocrString += item['words']
	return ocrString

def robot(ocrString):
	host = 'http://jisuznwd.market.alicloudapi.com'
	path = '/iqa/query'
	method = 'GET'
	appcode = '0698f335797345508be4b6c577423a79'
	querys = 'question=%s' + urllib.parse.quote(ocrString)
	bodys = {}
	url = host + path + '?' + querys
	print( url )
	request = urllib.request.Request(url)
	request.add_header('Authorization', 'APPCODE ' + appcode)
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf-8')
	
	return content

def showChome(ocrString):
	# 谷歌浏览器地址
	chromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
	# 百度搜索请求地址
	searchQuery = "https://www.baidu.com/s?wd=%s" % urllib.parse.quote( ocrString )
	# 使用谷歌浏览器打开百度搜索页面
	os.system('"%s" %s' % (chromePath, searchQuery))


if __name__ == "__main__":
	# 截图并保存
	grabScreen()

	# 使用百度API识图，得到文字
	picPath = r"screen.jpg"
	ocrString = getOCR(picPath)

	# 使用百度知道搜索答案
	answers = zhidao_search(
        keyword=ocrString,
        default_answer_select=2,
        timeout=5
    )
	answers = filter(None, answers)
	for text in answers:
		print('=' * 70)
		# text = text.replace("\u3000", "")
		# print("\n".join(textwrap.wrap(text, width=45)))
		print(text)

	# 在浏览器中打开
	showChome( ocrString )