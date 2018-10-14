from .factories import BookingFactory


def test_booking_str_method(db):
    booking = BookingFactory()
    assert booking.comments[:50] in str(booking)
