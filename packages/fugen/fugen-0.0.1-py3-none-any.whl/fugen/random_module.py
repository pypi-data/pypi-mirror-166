import random
import typing as t
from datetime import timedelta


class RandomModule(random.Random):
    """Custom class for the possibility of extending.
    The class is a subclass of the class :py:class:`random.Random`
    from the module random of the standard library, which provides the custom methods.
    """

    def randints(self, amount: int, a: int = 1, b: int = 10) -> t.List[int]:
        """Generate list of random integers.
        :param amount: Amount of elements.
        :param a: Minimum value of range, default = 1.
        :param b: Maximum value of range, default = 10.
        :return: List of random integers.
        :raises ValueError: if amount less or equal to zero.
        """
        if amount <= 0:
            raise ValueError("Amount out of range.")

        return [int(self.random() * (b - a)) + a for _ in range(amount)]

    @staticmethod
    def generate_date(start, end):
        """
        Returns a random datetime between two datetime objects.
        """
        delta = end - start
        random_day = random.randrange(delta.days)
        return start + timedelta(days=random_day)


random = RandomModule()
