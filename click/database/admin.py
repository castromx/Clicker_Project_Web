from . import models
from sqladmin import ModelView


class UserAdmin(ModelView, model=models.User):
    column_list = [models.User.id, models.User.name]


class BoostsAdmin(ModelView, model=models.Boosts):
    column_list = [models.Boosts.user_id, models.Boosts.mine_coint]


class UserScoreAdmin(ModelView, model=models.UserScore):
    column_list = [models.UserScore.user_id, models.UserScore.score]


class ImageAdmin(ModelView, model=models.Image):
    column_list = [models.Image.id, models.Image.clans]


class ClanAdmin(ModelView, model=models.Clan):
    column_list = [models.Clan.id, models.Clan.name]


class ClanScoreAdmin(ModelView, model=models.ClanScore):
    column_list = [models.ClanScore.id, models.ClanScore.score]


class UsersClanAdmin(ModelView, model=models.UsersClan):
    column_list = [models.UsersClan.user_id, models.UsersClan.clan_id]


class UserAchivmentsAdmin(ModelView, model=models.UserAchivments):
    column_list = [models.UserAchivments.user_id, models.UserAchivments.up_50k]


class UserChargesAdmin(ModelView, model=models.UserCharges):
    column_list = [models.UserCharges.user_id, models.UserCharges.charge]