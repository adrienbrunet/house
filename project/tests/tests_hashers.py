from .hashers import DummyHasher


def test_hasher():
    dummy_hasher = DummyHasher()
    assert dummy_hasher._load_library() is None
    assert dummy_hasher.safe_summary("dummy_hasher$foo") == {
        "algorithm": "dummy_hasher",
        "hash": "foo",
    }
