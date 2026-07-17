def min_cost(end_city, max_routes, max_budget, routes):
    """
    默认从城市 1 出发，在不超过 max_routes 条路线的情况下到达 end_city。

    routes[i] = [起点城市, 终点城市, 花费]
    如果最低花费不超过 max_budget，则返回最低花费，否则返回 -1。
    """
    if end_city == 1:
        return 0

    city_count = end_city
    for from_city, to_city, _ in routes:
        city_count = max(city_count, from_city, to_city)

    infinity = float("inf")#无穷大
    costs = [infinity] * (city_count + 1)
    costs[1] = 0
    # 1保证终点到达 2保证路线数 3保证最低花费
    # 第 i 轮结束后，costs 中保存使用不超过 i 条路线的最低花费。
    # 外层循环是路线数
    for _ in range(max_routes):
        next_costs = costs.copy()

        #遍历所有路线
        for from_city, to_city, route_cost in routes:
            if costs[from_city] == infinity:
                continue

            new_cost = costs[from_city] + route_cost
            if new_cost < next_costs[to_city]:
                next_costs[to_city] = new_cost

        costs = next_costs

    result = costs[end_city]
    return result if result <= max_budget else -1


if __name__ == "__main__":
    test_routes = [
        [1, 2, 10],
        [1, 3, 3],
        [3, 2, 2],
        [2, 4, 5],
        [3, 4, 12],
    ]

    # 1->4
    # 1->2->4
    # 1->3->4
    # 1->2->3->4



    # 1 -> 3 -> 2 -> 4，共 3 条路线，最低花费为 10。
    print(min_cost(4, 3, 10, test_routes))  # 10

    # 最多只能走 2 条路线，预算 12，无法满足条件。
    print(min_cost(4, 2, 12, test_routes))  # -1
