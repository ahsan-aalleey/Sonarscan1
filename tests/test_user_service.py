from src.user_service import hash_password


def test_hash_password_is_deterministic():
    assert hash_password("abc") == hash_password("abc")
