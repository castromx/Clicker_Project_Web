from sqladmin import Admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database.admin import UserAdmin, BoostsAdmin, UserScoreAdmin, ImageAdmin, ClanAdmin, \
    ClanScoreAdmin, UsersClanAdmin, UserAchivmentsAdmin, UserChargesAdmin
from routers.user_routers import router as user_router
from routers.clan_routers import router as clan_router
from routers.user_activity_routers import router as activity_router

app = FastAPI()
admin = Admin(app, engine)


app.include_router(user_router)
app.include_router(clan_router)
app.include_router(activity_router)

admin.add_view(UserAdmin)
admin.add_view(BoostsAdmin)
admin.add_view(UserScoreAdmin)
admin.add_view(ImageAdmin)
admin.add_view(ClanAdmin)
admin.add_view(ClanScoreAdmin)
admin.add_view(UsersClanAdmin)
admin.add_view(UserAchivmentsAdmin)
admin.add_view(UserChargesAdmin)


# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok"}
