from gino import Gino
from aiohttp import web
from datetime import datetime


password = ''
base = ''

PG_DSN = f'postgres://postgres:{password}@127.0.0.1:5432/{base}'


app = web.Application()
db = Gino()



class AdvertisementModel(db.Model):
    __tablename__ = 'advertisement_new'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    header = db.Column(db.String(100))
    definition = db.Column(db.Text)
    created_on = db.Column(db.DateTime(), default=datetime.now)

    def to_dict(self):
        user_data = super().to_dict()
        user_data['created_on'] = user_data['created_on'].strftime('%d.%m.%Y %I:%M')
        return user_data



class Advertisement(web.View):

    async def post(self):
        advertisement_data = await self.request.json()
        advertisement = await AdvertisementModel.create(**advertisement_data)
        return web.json_response(advertisement.to_dict())


    async def get(self):
        advertisement_id = self.request.match_info['advertisement_id']
        advertisement = await AdvertisementModel.get(int(advertisement_id))
        return web.json_response(advertisement.to_dict())


    async def delete(self):
        advertisement_id = self.request.match_info['advertisement_id']
        advertisement = await AdvertisementModel.get(int(advertisement_id))
        await advertisement.delete()
        return web.json_response(advertisement.to_dict())


    async def patch(self):
        advertisement_id = self.request.match_info['advertisement_id']
        advertisement = await AdvertisementModel.get(int(advertisement_id))
        advertisement_data = await self.request.json()
        await advertisement.update(**advertisement_data).apply()
        new_advertisement = await AdvertisementModel.get(int(advertisement_id))
        return web.json_response(new_advertisement.to_dict())


async def init_orm(app):
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close



app.add_routes([web.get('/advertisement/{advertisement_id}', Advertisement)])
app.add_routes([web.post('/advertisement', Advertisement)])
app.add_routes([web.delete('/advertisement/{advertisement_id}', Advertisement)])
app.add_routes([web.patch('/advertisement/{advertisement_id}', Advertisement)])

app.cleanup_ctx.append(init_orm)

web.run_app(app, port=8080)