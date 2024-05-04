import random
import time
import tqdm

def dostuff():
    bars = [tqdm.tqdm(total=100, desc=f"Bar {i}", position=i+5)for i in range(5)]
    while bars:
        bar = bars[random.randint(0, len(bars) - 1)]
        bar.update()
        if bar.n == 100:
            bars.remove(bar)

        time.sleep(0.05)
