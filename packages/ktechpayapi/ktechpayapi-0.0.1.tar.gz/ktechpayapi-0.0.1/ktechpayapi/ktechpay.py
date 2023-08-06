"""Entry point defined here."""
from ktechpayapi.transaction import TestTransaction, ProductionTransaction
from ktechpayapi.base import KtechPayBase


class Kteckpay(KtechPayBase):
    """Base class defined for KtechPay Instance Method."""

    def __init__(self, test_key=None, production_key=None):
        KtechPayBase.__init__(self, test_key=test_key, production_key=production_key)

        self.testTransaction = TestTransaction
        self.productionTransaction = ProductionTransaction
