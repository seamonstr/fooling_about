import asyncio


async def part1(arg: int) -> str:
    print(f"Running part 1; waiting for {arg} seconds.")
    await asyncio.sleep(arg)
    return f"Done part 1 with {arg}"


async def part2(arg, p1: int) -> str:
    print(f"Running part 2 with {arg} seconds and p1 {p1}")
    await asyncio.sleep(arg)
    return f"Done part 2 with {arg} seconds and p1 {p1}"


async def chain(arg: int) -> None:
    print(f"Starting chaing for {arg}")
    p1 = await part1(arg)
    p2 = await part2(arg, p1)
    print(f"Done chain with result {p2}")


async def main(*args) -> None:
    await asyncio.gather(*[chain(a) for a in args])


asyncio.run(main(1, 2, 3))
