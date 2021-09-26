from dao import DataDAO
from typing import Any, Union, List
from dto import DataDTO
from models import DataModel


class DataService:
    def __init__(self, data_dao: DataDAO):
        self._data_dao = data_dao

    async def create(self, dto: DataDTO):
        sum = await self._calculate_sum(dto.js)
        await self._data_dao.create(js=dto.js, sum=sum)

    async def get_by_sum(self, sum: int) -> Union[List, DataModel]:
        data = await self._data_dao.get_by_sum(sum=sum)

        return data

    async def _calculate_sum(self, js: Any) -> int:
        res = await self._calculating_helper(chunk=js) % 2**16

        return res

    async def _calculating_helper(self, chunk: Any) -> int:
        sum=0

        if type(chunk) is int:
            sum += chunk
            return sum
        elif isinstance(chunk, dict):
            for key, value in chunk.items():
                sum += await self._calculate_sum(key)
                sum += await self._calculate_sum(value)
        elif isinstance(chunk, list):
            for item in chunk:
                sum += await self._calculate_sum(item)

        return sum
