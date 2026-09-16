from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from exceptions import InvalidConfigurationError

PAISA = Decimal("0.01")
ROUNDING = ROUND_HALF_UP


def to_money(value):
    if isinstance(value, float):
        raise InvalidConfigurationError(
            f"don't pass floats for money, got {value!r}, use Decimal or str"
        )
    try:
        amt = Decimal(value)
    except InvalidOperation:
        raise InvalidConfigurationError(f"can't convert {value!r} to Decimal")
    return amt.quantize(PAISA, rounding=ROUNDING)