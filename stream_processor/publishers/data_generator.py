from json import dumps

from faker import Faker


class RandomDataGenerator:
    def __init__(self, locale: str) -> None:
        self._fake = Faker(locale)

    def generate_pageview(self) -> bytes:
        webpage = f"www.website.com/{self._fake.uri_path()}.html"
        postcode = self._fake.postcode().split()[0]
        data = {
            "user_id": self._fake.random_int(),
            "postcode": postcode,
            "webpage": webpage,
            "timestamp": self._fake.unix_time(),
        }
        return dumps(data).encode("utf-8")
