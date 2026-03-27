from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import template

register = template.Library()


@register.filter
def comma0(value):
    """
    Format numeric values with commas and no decimals.
    Example: 425000 -> '425,000'
    """
    if value in (None, ""):
        return ""
    try:
        number = Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return f"{int(number):,}"
    except (InvalidOperation, ValueError, TypeError):
        return value
