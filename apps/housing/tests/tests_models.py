from ..models import Housing
from .factories import HousingFactory


def test_housing_str():
    house_name = "My first house"
    new_house = House(name=house_name)
    assert str(new_house) == house_name
