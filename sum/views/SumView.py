from http import HTTPStatus
from dto import DataDTO
from webargs.aiohttpparser import use_args
from webargs import fields
from aiohttp import web
from consts import DATA_SERVICE


class SumView(web.View):
    endpoint = '/data'

    async def post(self):
        data = await self.request.json()
        dto = DataDTO(**data)
        print(dto)
        await self.request.app[DATA_SERVICE].create(dto)

        return web.json_response(status=HTTPStatus.CREATED)

    @use_args({'sum': fields.Int(required=True)}, location='query')
    async def get(self, args):
        sum = args.get('sum')
        models = await self.request.app[DATA_SERVICE].get_by_sum(sum)
        data = [data.as_dict() for data in models]

        return web.json_response(status=HTTPStatus.OK, data=data)



