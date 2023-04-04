# -*- coding: utf-8 -*-

from discord.ext import tasks
from discord.ext import commands
from Fnc.asyncChat import *

import datetime
import discord
import asyncio
import json

#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents		= discord.Intents.default()
intents.message_content = True
intents.members = True
client		= commands.Bot(command_prefix='?', intents=intents)

config		= open("data/json/DC_config.json", "r", encoding="utf-8")
conf		= json.load(config)
bot_ID		= conf["bot_ID"]
Master_ID	= conf["Master_ID"]
Token		= conf["DC_key"]

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
	print("目前登入身份：", client.user)
	changeActivity.start()
	await ChaInt()
	Reflash_CharacterAI.start()
	

#更改機器人狀態
@tasks.loop(seconds=5.0)
async def changeActivity():
	f = open("data/json/Stetas.json", "r", encoding="utf-8")
	data			=	json.load(f)
	State			=	data["State"]
	await client.change_presence(activity=discord.Activity(name=State, type=1))

#Reflash CharacterAI
@tasks.loop(minutes=30)
async def Reflash_CharacterAI():
	await Reflash_Character()
	
async def Reflash_Character():
	await ReflashAI()
	print("On_Reflash")

@client.event
#當有訊息時
async def on_message(message):
	#排除自己的訊息，避免陷入無限循環
	if message.author == client.user:
		return
	
	#設定是否已回覆旗標
	send = True

	#列印接收到的訊息
	print(f"[{Get_Time()}] Get Message from {str(message.guild)}.{str(message.channel)}.{str(message.author)}: {str(message.content)}")
	
	#判斷有無回覆訊息
	if message.reference is not None:
		#獲取被回覆的訊息
		ctx = await message.channel.fetch_message(message.reference.message_id)
		
		#如果被回覆的對象是此機器人
		if (ctx.author == client.user):
			await cmd(message, f"{ID_To_Name(message.content)}")
			send = False
	
	#指令程序
	if ((message.content.find(bot_ID) != -1) or (is_Mention(message.content))) and (send == True):
	
		await cmd(message, ID_To_Name(message.content))
		send = False

#指令讀取
async def cmd(ctx, cmd):

	if cmd.find("Replace ") != -1:					#測試功能:取代訊息
		if ctx.reference is not None:
			message = await ctx.channel.fetch_message(ctx.reference.message_id)
			print(f"[{Get_Time()}] Replace message of {str(ctx.guild)}.{str(ctx.channel)}: {message.content}")
			if len(message.content) > 0:
				await sender(ctx, message.content)
			if message.attachments:
				FileName	= f"./data/file/file.{message.attachments[0].url.split('/')[-1].split('.')[-1]}"
				res2 = requests.post(message.attachments[0].url)
				with open(FileName, mode='wb') as f:
					f.write(res2.content)
				await FileSender(ctx, FileName)
			await message.delete()
		else:
			print(f"[{Get_Time()}] Replace message of {str(ctx.guild)}.{str(ctx.channel)}: {Cut_Name(cmd)[8:]}")
			await sender(ctx, Cut_Name(cmd)[8:])
			if ctx.attachments:
				FileName	= f"./data/file/file.{ctx.attachments[0].url.split('/')[-1].split('.')[-1]}"
				res2 = requests.post(ctx.attachments[0].url)
				with open(FileName, mode='wb') as f:
					f.write(res2.content)
				await FileSender(ctx, FileName)
		await ctx.delete()
		
	elif cmd.find("ReAI") != -1:					#測試功能:Reflash CharacterAI page
		async with ctx.channel.typing():
			await Reflash_Character()
			Str = "Reflash CharacterAI page"
		await ctx.reply(Str)
		print(f"[{Get_Time()}] Reply message to {str(ctx.guild)}.{str(ctx.channel)}.{ctx.author}: {Str}")
	
	else:								#暴力連接chatGPT

		async with ctx.channel.typing():
			f = open("data/json/CharacterSet.json", "r", encoding="utf-8")
			text = ChangeText(ctx, f"{json.load(f)['Character']}")
			Str = await chai(text)
		await ctx.reply(Str)
		print(f"[{Get_Time()}] Reply message to {str(ctx.guild)}.{str(ctx.channel)}.{ctx.author}: {Str}")

def ChangeText(ctx, text):
	text = text.replace("&author;", str(ctx.author))
	text = text.replace("&guild;", str(ctx.guild))
	text = text.replace("&channel;", str(ctx.channel))
	text = text.replace("&Master_ID;", str(Master_ID))
	text = text.replace("&bot_ID;", str(bot_ID))
	text = text.replace("&message;", str(ctx.content))
	return text
	

#傳送訊息用
async def sender(Message, Str):
	await Message.channel.send(Str)
	print(f"[{Get_Time()}] Send message to {str(Message.guild)}.{str(Message.channel)}: {Str}")

#傳送檔案用
async def FileSender(Message, File):
	print(f"[{Get_Time()}] Send file to {str(Message.guild)}.{str(Message.channel)}")
	await Message.channel.send(file=discord.File(File))

#獲取時間
def Get_Time():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

#是否被文字提及
def is_Mention(Message):
	My_Name = open("data/json/Name.json", "r", encoding="utf-8")
	data			=	json.load(My_Name)
	NameList		=	data["Name"]
	for i in range(len(NameList)):
		FindName	=	NameList[str(i)]
		if Message.find(FindName) != -1:
			return True
	return False

#從文字中去除自己的名字
def Cut_Name(Message):
	My_Name = open("data/json/Name.json", "r", encoding="utf-8")
	data			=	json.load(My_Name)
	NameList		=	data["Name"]
	for i in range(len(NameList)):
		FindName	=	NameList[str(i)]
		if Message.find(FindName) != -1:
			Str = Message.split(FindName)[0] + Message.split(FindName)[1]
			return Str
	return Message

#將代號或ID指向默認的名字
def ID_To_Name(Message):
	My_Name = open("data/json/Name.json", "r", encoding="utf-8")
	data			=	json.load(My_Name)
	if Message.find("Rename") != -1:
		return Message
	return Message.replace(bot_ID, data["DefaultName"])
	

def DC_int():
	#連線
	client.run(Token)

DC_int()
