class PricingEngineError(Exception):
    """Base exception for pricing engine errors."""
    pass


class PricingError(PricingEngineError):
    pass


class InvalidTierError(PricingEngineError):
    pass


class InvalidQuantityError(PricingEngineError):
    pass


class TierSoldOutError(PricingEngineError):
    pass


class InvalidConfigurationError(PricingEngineError):
    pass