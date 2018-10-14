from datetime import datetime, timedelta

import factory
import factory.fuzzy
import pytz

from ..models import Booking

now = datetime.now(pytz.utc)
three_years_later = now + timedelta(weeks=52 * 3)


class BookingFactory(factory.django.DjangoModelFactory):
    start_date = factory.fuzzy.FuzzyDateTime(now, three_years_later)
    end_date = factory.lazy_attribute(lambda b: b.start_date + timedelta(days=7))
    comments = factory.fuzzy.FuzzyText()
    booker = factory.SubFactory("apps.users.tests.factories.UserProfileFactory")
    housing = factory.SubFactory("apps.housing.tests.factories.HousingFactory")

    class Meta:
        model = Booking
