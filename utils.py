def dollar_formatter(x, use_decimals=True):
    """Format a number as a dollar value.

    Args:
        x (float): The number to be formatted.
        use_decimals (bool): Whether to use two decimal places or not.

    Returns:
        str: The formatted dollar string.
    """
    if use_decimals:
        return f'${x:.2f}'
    else:
        return f'${int(round(x)):,}'


def dollar_formatter_wrapper(x, pos=None):
    return dollar_formatter(x, use_decimals=False)
