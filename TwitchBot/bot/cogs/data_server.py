from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from bot import Bot
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from twitchio.ext import commands
import aiosqlite


log_file_path = "bot.log"
DATABASE_PATH = "database.sqlite3"

if os.path.exists(log_file_path):
    os.remove(log_file_path)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger(__name__)
app = FastAPI()
app.mount("/assets", StaticFiles(directory="../browser/highscore/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@ app.get("/", response_class=FileResponse)
def dashboard_endpoint() -> FileResponse:
    """
    HTTP endpoint to serve the Dashboard
    :param request: HTTP Request from Client
    :return: Returns the associated web files to the requesting client
    """
    return FileResponse(r"..\browser\highscore\index.html")

@ app.get("/user/{user_name}")
async def get_user(user_name: str):
    logger.info(f"User endpoint accessed for user: {user_name}")
    async with aiosqlite.connect(DATABASE_PATH) as db:
        query="SELECT * FROM user_economy WHERE username = ?"
        async with db.execute(query, (user_name,)) as cursor:
            user=await cursor.fetchone()
            if user:
                return {
                    "username": user[0],
                    "credits": user[1],
                    "points": user[2],
                    "level": user[3]
                }
            return {"error": "User not found"}


@app.get("/users")
async def get_all_users():
    logger.info("All users endpoint accessed")
    async with aiosqlite.connect(DATABASE_PATH) as db:
        query = "SELECT * FROM user_economy"
        async with db.execute(query) as cursor:
            users = await cursor.fetchall()
            user_list = [
                {
                    "username": user[0],
                    "credits": user[1],
                    "points": user[2],
                    "level": user[3]
                }
                for user in users
            ]
            return {"users": user_list}


class FastAPIServer(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot=bot

    @ commands.Cog.event()
    async def event_ready(self):
        print(f"Logged in as {self.bot.nick}")

# Prepare function to add the cog and start the FastAPI app


def prepare(bot: Bot):
    bot.add_cog(FastAPIServer(bot))

    import uvicorn
    from threading import Thread

    def run_server():
        uvicorn.run(app, host="localhost", port=8000)

    server_thread=Thread(target=run_server, daemon=True)
    server_thread.start()
