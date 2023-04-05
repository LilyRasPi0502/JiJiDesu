from playwright.async_api import async_playwright
import asyncio
import json

playwright = None
browser = None
context = None
page = None

async def ChaInt():
	global playwright
	global browser
	global context
	global page
	playwright = await async_playwright().start()
	browser = await playwright.firefox.launch()
	context = await browser.new_context()
	page = await context.new_page()
	await page.goto(f"https://chat.openai.com/chat")
	
	await Login()
	await ClickAd()
	await selectChat()
	
	
async def Login():
	global page
	config		= open("data/json/chatGPT_Config.json", "r", encoding="utf-8")
	conf		= json.load(config)

	Login = await page.wait_for_selector(".btn-primary")
	await Login.click()
	Email = await page.wait_for_selector(".cf072f6c3")
	await Email.fill(conf["Account"])
	await Email.press("Enter")
	PW = await page.wait_for_selector(".c8f0f4668")
	await PW.fill(conf["Password"])
	await PW.press("Enter")
				

	print("on login")
	await page.screenshot(path="data/example.png")
	
async def ClickAd():
	ADB0 = await page.wait_for_selector(".ml-auto")
	await ADB0.click()
	ADB1 = await page.wait_for_selector(".ml-auto")
	await ADB1.click()
	ADB2 = await page.wait_for_selector(".ml-auto")
	await ADB2.click()
	
async def ReflashAI():
	global page
	
	await page.reload()
	
	Login = await page.query_selector(".btn-primary")
	if str(Login).find("NoneType") != -1:
		if await Login.is_visible():
			await Login()
			await ClickAd()
	await selectChat()

async def selectChat():
	global page
	config		= open("data/json/chatGPT_Config.json", "r", encoding="utf-8")
	conf		= json.load(config)
	await asyncio.sleep(5)
	Chat = ".gap-3"
	ChatName = conf["ChatName"]
	Sstr = ""
	await page.screenshot(path="data/example.png")
	S = await page.query_selector_all(Chat)
	for i in range(len(S)):
		Sstr = await S[i].inner_text()
		if Sstr.find(ChatName) != -1:
			await S[i].click()
			print(f"select chat name: {ChatName}")
			break
	await page.screenshot(path="data/example.png")

async def chai(text):
	global page
	
	await page.screenshot(path="data/example.png")
	
	await page.get_by_placeholder("Send a message...").fill(text)
	await page.get_by_placeholder("Send a message...").press("Enter")
	nextFlag = await page.wait_for_selector(".gap-2")
	if await nextFlag.is_visible():
		Sstr = ""

		while Sstr.find("Regenerate response") != -1:
			for i in range(len(S)):
				Sstr = await S[i].inner_text()
				if Sstr.find("Regenerate response") == -1:
					break

		while Sstr.find("Regenerate response") == -1:
			S = await page.query_selector_all(".gap-2")
			for i in range(len(S)):
				Sstr = await S[i].inner_text()
				if Sstr.find("Regenerate response") != -1:
					break

		div = await page.query_selector_all(".markdown")
		output_text = await div[-1].inner_text()
	else:
		output_text = f"I don't know. <:BocchiPain:1058756560026873856> "
	return output_text


if __name__ == "__main__":
	ChaInt()
	while True:
		print(chai(input(">")))

