from unittest import TestCase, main

from la_headers import generate_random_headers


class TestSystem(TestCase):
    def test_base(self) -> None:
        print(generate_random_headers())
        print(generate_random_headers())
        print(generate_random_headers())
        print(generate_random_headers())
        print(generate_random_headers())
        print(generate_random_headers())
        print(generate_random_headers())


if __name__ == "__main__":
    main()
