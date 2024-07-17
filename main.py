import os
import discord
import json
import requests
import random 
from replit import db
import numpy as np
from keep_alive import keep_alive

my_token = os.environ['token']
client = discord.Client()

sad_words = ["sad","depressed","unhappy","angry","depressing","miserable"]

starter_encouragements = [
  "YOLO!",
  "Cheer up!",
  "Hang in there"

]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  print(json_data)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else :
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index :
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  
  if "encouragements" in db.keys():
    options = np.concatenate((options, db["encouragements"]))

  if db["responding"]:
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouring message added")
  
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split('$del',1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")

keep_alive()
client.run(my_token)