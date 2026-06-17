from fastapi import FastAPI
import httpx
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1516892408305029161/LCUST8Rh_dndrN9uat0M_CSTWVR_WcClUpbVMJLddY4QMnB09RqUojNCLIEjDozIqFEP"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/CreativePlots")
async def submit_CreativePlots(mcUser: str, dcUser: str, description: str):
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
            r = await client.post(WEBHOOK_URL, json=discordMessage)
            
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code}
@app.post("/TinySurvival")
async def submit_TinySurvival(mcUser: str, dcUser: str, description: str):
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
            r = await client.post(WEBHOOK_URL, json=discordMessage)
        
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code}

