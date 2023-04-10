import math

DICE_SIDES = set([4, 6, 8, 10, 12, 20, 100])


def factors(number: int):
    output = set([])
    for i in range(2, number):
        if number % i == 0:
            output.add(i)

    return output


def is_square(number: int):
    x = number // 2
    seen = set([x])
    while x * x != number:
        x = (x + (number // x)) // 2
        if x in seen:
            return False
        seen.add(x)
    return True


def is_perfect_power(number: int):
    for m in factors(number):
        for k in range(1, int(math.log(number, 2))):
            if m ** k == number:
                return (m, k)


def find_dice_roll(number: int):
    """Find what dice to roll to give a range of 1-number."""

    if number in DICE_SIDES:
        """Is it simply a single dice roll?"""
        return f'd{number}'

    if parts := is_perfect_power(number):
        return f'd{parts[0]}' * parts[1]

    # usable_dice = factors(number)

    for dice in sorted(DICE_SIDES):
        if number in factors(dice):
            divisor = dice // number
            return f'd{dice} / {divisor}'

    for dice in sorted(DICE_SIDES):
        if number < dice:
            return f'd{dice} > {number}'


if __name__ == "__main__":
    assert find_dice_roll(4) == 'd4'
    assert find_dice_roll(6) == 'd6'
    assert find_dice_roll(8) == 'd8'
    assert find_dice_roll(10) == 'd10'
    assert find_dice_roll(12) == 'd12'
    assert find_dice_roll(20) == 'd20'
    assert find_dice_roll(36) == 'd6d6'
    assert find_dice_roll(3) == 'd6 / 2'
    assert find_dice_roll(7) == 'd8 > 7'
    assert find_dice_roll(14) == 'd20 > 14'
