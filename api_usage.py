import discord
import requests
import json



#joke
def get_joke():
  data = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit")
  tt = json.loads(data.text)
  joke = tt["setup"] + "\n" + tt["delivery"]
  return joke


#quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n" + "\t" + "\t" + " -" + json_data[0]['a']
    return(quote)

#meme
def get_meme():
  url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"

  querystring = {"top":"Top Text","bottom":"Bottom Text","meme":"Condescending-Wonka","font_size":"50","font":"Impact"}

  headers = {
      'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
      'x-rapidapi-key': "SIGN-UP-FOR-KEY"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)
  return(response)