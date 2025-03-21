"""Utility functions for formatting monetary values and timestamps.

### Functions:
- **`moneyfmt`**: A function to format `Decimal` values as currency strings.
- **`datefmt`**: A function to format ISO 8601 timestamps into a human-readable string.
"""

from datetime import datetime
from decimal import Decimal


def moneyfmt(value, places=2, curr='$', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert a `Decimal` to a money-formatted string.

    #### Parameters:
    - **`value`**: The `Decimal` value to format.
    - **`places`**: Required number of places after the decimal point (default: `2`).
    - **`curr`**: Optional currency symbol before the sign (default: `'$'`).
    - **`sep`**: Optional grouping separator (comma, period, space, or blank) (default: `','`).
    - **`dp`**: Decimal point indicator (comma or period) (default: `'.'`).
    - **`pos`**: Optional sign for positive numbers: `'+'`, space, or blank (default: `''`).
    - **`neg`**: Optional sign for negative numbers: `'-'`, `'('`, space, or blank (default: `'-'`).
    - **`trailneg`**: Optional trailing minus indicator: `'-'`, `')'`, space, or blank (default: `''`).

    #### Returns:
    - A string representing the formatted monetary value.

    #### Examples:
    ```python
    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'
    ```
    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, _next = result.append, digits.pop
    if sign:
        build(trailneg)
    for _ in range(places):
        build(_next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(_next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def datefmt(timestamp: str):
    """Format an ISO 8601 timestamp into a human-readable string.

    #### Parameters:
    - **`timestamp`**: A string representing the ISO 8601 timestamp.

    #### Returns:
    - A string formatted as `"%d de %B de %Y, %H:%M:%S"`.

    #### Examples:
    ```python
    >>> datefmt("2023-03-15T14:30:00")
    '15 de marzo de 2023, 14:30:00'
    ```
    """
    parsed =  datetime.fromisoformat(timestamp)
    return parsed.strftime("%d de %B de %Y, %H:%M:%S")
