"""Script used to define the paystack Transaction class."""

from ktechpayapi.base import KtechPayBase


class TestTransaction(KtechPayBase):
    """docstring for Transaction."""

    @classmethod
    def initialize(cls, **kwargs):
        """
        Initialize transaction.

        Args:
            amount: amount
            email: email address

        Returns:
            Json data from ktechpay API.
        """

        return cls().requests.post("test/payments/", data=kwargs)

    @classmethod
    def list(cls):
        """
        List transactions.

        Args:
            No argument required.

        Returns:
            Json data from ktechpay API.
        """
        return cls().requests.get("test/payments/")

    @classmethod
    def verify(cls, reference):
        """
        Verify transactions.

        Args:
            reference: a unique value needed for transaction.

        Returns:
            Json data from ktechpay API.
        """
        return cls().requests.get(f"test/payments/{reference}")


class ProductionTransaction(KtechPayBase):
    """docstring for Transaction."""

    @classmethod
    def initialize(cls, **kwargs):
        """
        Initialize transaction.

        Args:
            amount: amount
            email: email address

        Returns:
            Json data from ktechpay API.
        """

        return cls().requests.post("production/payments/", data=kwargs)

    @classmethod
    def list(cls):
        """
        List transactions.

        Args:
            No argument required.

        Returns:
            Json data from ktechpay API.
        """
        return cls().requests.get("production/payments/")

    @classmethod
    def verify(cls, reference):
        """
        Verify transactions.

        Args:
            reference: a unique value needed for transaction.

        Returns:
            Json data from ktechpay API.
        """
        return cls().requests.get(f"production/payments/{reference}")
