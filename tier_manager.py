from exceptions import InvalidQuantityError, InvalidTierError, TierSoldOutError


class TierManager:
    def __init__(self, tiers):
        self.tiers = tiers

    def resolve(self, request):
        qty = request.quantity
        if not isinstance(qty, int) or isinstance(qty, bool):
            raise InvalidQuantityError(
                f"quantity for {request.tier_name} must be an int, got {type(qty).__name__}"
            )
        if qty <= 0:
            raise InvalidQuantityError(
                f"quantity for {request.tier_name} must be positive, got {qty}"
            )

        tier = self.tiers.get(request.tier_name)
        if tier is None:
            available = ", ".join(sorted(self.tiers)) or "none configured"
            raise InvalidTierError(
                f"'{request.tier_name}' isn't a valid tier, options are: {available}"
            )

        if qty > tier.seats_left:
            raise TierSoldOutError(
                f"{tier.name} only has {tier.seats_left} seat(s) left, asked for {qty}"
            )

        return tier