from fastapi import FastAPI, Request
import httpx
from fastapi.middleware.cors import CORSMiddleware 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv

load_dotenv() # get secrets from .env file

limiter = Limiter(key_func=get_remote_address) #limit per ip address
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore


WEBHOOK_URL = os.environ["API_KEY"] # get webhook url from environment variable

app.add_middleware( # allow only form submissions
		CORSMiddleware,
		allow_origins=["*"],
		allow_methods=["POST"],
		allow_headers=["MOONDUST_FORM_SUBMISSION"],
)

@app.post("/submit")
@limiter.limit("5/minute") # limit to 5 requests per minute per ip address
async def submit(request: Request, type: str, username: str, handle: str, description: str):
	discordMessages = {
		"creativePlots":{
			"embeds": [
				{
					"author": {"name": "Form Submission"},
					"title": "Creative Plots Form Submission",
					"color":  9983179,
					"fields": [
						{"name": "Minecraft Username", "value": username, "inline": False},
						{"name": "Discord Username", "value": handle, "inline": False},
						{"name": "Describe who you are and what makes you interested in Creative plots!", "value": description, "inline": False}
					]
				}
			]
		},
		"tinySurvival":{
			  "embeds": [
				{
					"author": {"name": "Form Submission"},
					"title": "TinySurvival Form Submission",
					"color":  9983179,
					"fields": [
						{"name": "Minecraft Username", "value": username, "inline": False},
						{"name": "Discord Username", "value": handle, "inline": False},
						{"name": "Describe who you are and what makes you interested in Tiny Survival!", "value": description, "inline": False}
					]
				}
			]
		},
		"buildComp":{
        "embeds": [
        {
          "author": {"name": "Form Submission"},
          "title": "Build Comp Form Submission",
          "color":  9983179,
          "fields": [
            {"name": "Minecraft Username(s)", "value": username, "inline": False}]
        }
        ]
    }
  }

	if discordMessages[type] != None:
		async with httpx.AsyncClient() as client:
			r = await client.post(WEBHOOK_URL, json=discordMessages[type]) # send message to discord webhook
			return {"message": "Form submitted successfully", "data": {"username": username, "handle": handle, "description": description}, "discord_status_code": r.status_code} #api response

