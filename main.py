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

app.add_middleware( # allow all requests
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/CreativePlots")
@limiter.limit("5/minute") # limit to 5 requests per minute
async def submit_CreativePlots(request: Request, mcUser: str, dcUser: str, description: str): # dont change these names, api gets its input via a link that has these names in it, if you change them the api will break
        discordMessage = {
              "embeds": [
                {
                "author": {"name": "Form Submission"},
                  "title": "Creative Plots Form Submission",
                  "color":  9983179,
                  "fields": [
                    {"name": "Minecraft Username", "value": mcUser, "inline": False},
                    {"name": "Discord Username", "value": dcUser, "inline": False},
                    {"name": "Describe who you are and what makes you interested in Creative plots!", "value": description, "inline": False}
                  ]
                }
              ]
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(WEBHOOK_URL, json=discordMessage) # send message to discord webhook
            
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code} #api response
@app.post("/TinySurvival")
@limiter.limit("5/minute") # limit to 5 requests per minute
async def submit_TinySurvival(request: Request, mcUser: str, dcUser: str, description: str): # dont change these names, api gets its input via a link that has these names in it, if you change them the api will break
        discordMessage = {
              "embeds": [
                {
                "author": {"name": "Form Submission"},
                  "title": "TinySurvival Form Submission",
                  "color":  9983179,
                  "fields": [
                    {"name": "Minecraft Username", "value": mcUser, "inline": False},
                    {"name": "Discord Username", "value": dcUser, "inline": False},
                    {"name": "Describe who you are and what makes you interested in Tiny Survival!", "value": description, "inline": False}
                  ]
                }
              ]
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(WEBHOOK_URL, json=discordMessage) # send discord message to webhook
        
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code} #api response
@app.post("/BuildComp")
@limiter.limit("5/minute") # limit to 5 requests per minute
async def submit_BuildComp(request: Request, mcUser: str): # dont change these names, api gets its input via a link that has these names in it, if you change them the api will break
        discordMessage = {
              "embeds": [
                {
                "author": {"name": "Form Submission"},
                  "title": "Build Competition Form Submission",
                  "color":  9983179,
                  "fields": [
                    {"name": "Minecraft Username(s)", "value": mcUser, "inline": False},
                  ]
                }
              ]
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(WEBHOOK_URL, json=discordMessage) # send message to discord webhook
            
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser},
                "discord_status_code": r.status_code} #api response

