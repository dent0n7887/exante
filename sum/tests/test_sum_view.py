from mockito import unstub, when
from tests import conftest
from views import SumView
from http import HTTPStatus


class TestSumView:
    def teardown(self):
        unstub()

    def test_get_sum_success(self, loop, f_test_client, f_data_model):
        async def do_test():
            async def set_result():
                return f_data_model

            when(conftest.DataDAO).get_by_sum(...).thenReturn(set_result())
            resp = await f_test_client.get(f'{SumView.endpoint}?sum=2')
            assert resp.status == HTTPStatus.OK
            body = await resp.json()
            assert body == [f_data_model[0].as_dict()]

        loop.run_until_complete(do_test())

    def test_create_sum_success(self, loop, f_test_client, f_data_model):
        async def do_test():
            async def set_result():
                return f_data_model
            when(conftest.DataDAO).create(...).thenReturn(set_result())
            resp = await f_test_client.post(f'{SumView.endpoint}', json={'js': 1})
            assert resp.status == HTTPStatus.CREATED

        loop.run_until_complete(do_test())

    def test_get_sum_bad_request(self, loop, f_test_client):
        async def do_test():
            resp = await f_test_client.get(f'{SumView.endpoint}?sum=abc')
            assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY

        loop.run_until_complete(do_test())

    def test_create_sum_bad_request(self, loop, f_test_client):
        async def do_test():
            resp = await f_test_client.post(f'{SumView.endpoint}', json={'jss': 'Wrong parameter'})
            assert resp.status == HTTPStatus.BAD_REQUEST

        loop.run_until_complete(do_test())