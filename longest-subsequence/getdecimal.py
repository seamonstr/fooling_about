def get_decimal(numerator, denominator):
    ret = str(numerator // denominator)
    remainder = numerator % denominator
    digits = ""
    recurring = ""

    seen = {}

    while True:
        if remainder == 0:
            break
        if remainder in seen:
            recurring = f"({digits[seen[remainder]:]})"
            digits = digits[: seen[remainder]]
            break
        seen[remainder] = len(digits)

        remainder *= 10
        digits += str(remainder // denominator)
        remainder %= denominator

    if len(digits) or len(recurring):
        ret += "."
    if len(digits):
        ret += f"{digits}"
    if len(recurring):
        ret += recurring
    return ret
