from time import perf_counter

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int, coins: list[int] = COINS) -> dict[int, int]:
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною.")

    remaining = amount
    result: dict[int, int] = {}

    for coin in sorted(coins, reverse=True):
        if remaining == 0:
            break

        count = remaining // coin
        if count:
            result[coin] = count
            remaining -= coin * count

    if remaining != 0:
        raise ValueError("Неможливо видати решту для заданої суми.")

    return result


def find_min_coins(amount: int, coins: list[int] = COINS) -> dict[int, int]:
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною.")

    dp = [0] + [float("inf")] * amount
    last_coin = [0] * (amount + 1)

    for coin in coins:
        for s in range(coin, amount + 1):
            if dp[s - coin] + 1 < dp[s]:
                dp[s] = dp[s - coin] + 1
                last_coin[s] = coin

    if dp[amount] == float("inf"):
        raise ValueError("Неможливо видати решту для заданої суми.")

    result: dict[int, int] = {}
    s = amount

    while s > 0:
        coin = last_coin[s]
        result[coin] = result.get(coin, 0) + 1
        s -= coin

    return dict(sorted(result.items(), reverse=True))


def benchmark(amounts: list[int]) -> list[tuple[int, float, float]]:
    results: list[tuple[int, float, float]] = []

    for amount in amounts:
        start = perf_counter()
        find_coins_greedy(amount)
        greedy_time = perf_counter() - start

        start = perf_counter()
        find_min_coins(amount)
        dp_time = perf_counter() - start

        results.append((amount, greedy_time, dp_time))

    return results


if __name__ == "__main__":
    test_amount = 113
    greedy_result = find_coins_greedy(test_amount)
    dp_result = find_min_coins(test_amount)

    print(f"Сума: {test_amount}")
    print(f"Жадібний алгоритм: {greedy_result}")
    print(f"Динамічне програмування: {dp_result}")

    amounts = [10, 113, 1000, 10_000, 100_000]
    stats = benchmark(amounts)

    print("\nПорівняння часу виконання (секунди):")
    print("Сума\tЖадібний\tДинамічний")
    for amount, greedy_time, dp_time in stats:
        print(f"{amount}\t{greedy_time:.6f}\t{dp_time:.6f}")