from fastapi import FastAPI
import httpx
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1516574621577646200/1wS2jWUKZ_gB50b2mLfITXJ-tfGE4TVN9EbK7apvbs9ULmc9op5omhJ3pWTSlMzGRtD_"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/CreativePlots")
async def submit_CreativePlots(mcUser: str, dcUser: str, description: str):
        discordMessage = {"content": f"CreativePlots Form Submission:\nMinecraft Username: {mcUser}\nDiscord Username: {dcUser}\nDescription: {description}"}

        async with httpx.AsyncClient() as client:
            r = await client.post(WEBHOOK_URL, json=discordMessage)
            
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code}
@app.post("/TinySurvival")
async def submit_TinySurvival(mcUser: str, dcUser: str, description: str):
        discordMessage = {"content": f"TinySurvival Form Submission:\nMinecraft Username: {mcUser}\nDiscord Username: {dcUser}\nDescription: {description}"}

        async with httpx.AsyncClient() as client:
            r = await client.post(WEBHOOK_URL, json=discordMessage)
        
        return {"message": "Form submitted successfully", "data": {"mcUser": mcUser, "dcUser": dcUser, "description": description},
                "discord_status_code": r.status_code}

