import pytest


@pytest.mark.parametrize('js,expected_result', [
    (4, 4),
    ([2], 2),
    ({"z": [1, "a", 0.5, 1], "": True}, 2),
    ({"1": [1, "a", 0.5, 70000], "": True}, 4465),
    ({"z": ['1', "a", 0.5]}, 0),
    ({"z": ['1', "a", 65536]}, 0)
])
async def test_calculate_sum(js, expected_result, f_data_service):
    result = await f_data_service._calculate_sum(js=js)

    assert result == expected_result
