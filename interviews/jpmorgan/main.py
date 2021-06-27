# coding: utf-8

"""
Float type was chosen just for simplicity's sake. If we want more
accurate calculations we could use Decimals or treat all prices as
integers multiplied by some big multiplier (let's say 1e6 for
example).
"""

import random
import datetime
import typing
import dataclasses
import collections
import math


TYPE_COMMON = "common"
TYPE_PREFERRED = "preferred"


@dataclasses.dataclass
class StockEntry:
    symbol: str
    type: str
    last_dividend: int
    fixed_dividend: typing.Optional[int]
    par_va  lue: int

    def dividend_yield(self, market_price):
        assert market_price > 0

        if self.type == TYPE_COMMON:
            return self.last_dividend / market_price
        else:
            return self.fixed_dividend * self.par_value / market_price

    def pe_ratio(self, market_price):
        assert market_price > 0

        # I'm not sure that this should be calculated in this way, I
        # don't know what the difference between last and fixed
        # dividend.

        if not self.last_dividend:
            return None

        return market_price / self.last_dividend


TRADE_DIRECTION_BUY = "buy"
TRADE_DIRECTION_SELL = "sell"


@dataclasses.dataclass
class Trade:
    symbol: str
    direction: str
    timestamp: datetime.datetime
    price: int
    volume: int

    def __post_init(self):
        assert self.direction in (TRADE_DIRECTION_BUY, TRADE_DIRECTION_SELL)
        assert self.price > 0
        assert self.volume > 0

    def __str__(self):
        return f"[{self.symbol} {self.direction} {self.timestamp:%H:%M} price={self.price} volume={self.volume}]"


class Trades:
    """
    Symbol to trades info. Maintain only last 15 minutes history from
    last trade.

    If we need to store the whole trade history than implementation of
    get_last_15_min_weighted_price must be adopted.
    """

    def __init__(self):
        self.trades = collections.defaultdict(lambda: {
            "trades": collections.deque(),
            "last_15_min_volume": 0,
            "last_15_min_priced_volume": 0,  # price multiplied by volume
        })

    def get_last_15_min_weighted_price(self, symbol):
        if symbol not in self.trades:
            return 0

        trades_info = self.trades[symbol]
        return trades_info["last_15_min_priced_volume"] / trades_info["last_15_min_volume"]

    def add_trade(self, symbol, timestamp, trade_direction, price, volume):
        """Add new trade info and store data only for 15 before last trade"""

        new_trade = Trade(
            symbol=symbol,
            direction=trade_direction,
            timestamp=timestamp,
            price=price,
            volume=volume,
        )

        trades_info = self.trades[symbol]

        trades = trades_info["trades"]
        if trades:
            # we should use heap if we want to allow non-monotonic timestamp sequences
            assert trades[-1].timestamp <= timestamp, "non-monotonic timestamp"

        # remove stale trades
        stale_ts = timestamp - datetime.timedelta(minutes=15)
        while trades and trades[0].timestamp < stale_ts:
            trade = trades.popleft()
            trades_info["last_15_min_priced_volume"] -= trade.price * trade.volume
            trades_info["last_15_min_volume"] -= trade.volume

        # add a new one trade
        trades.append(new_trade)
        trades_info["last_15_min_priced_volume"] += new_trade.price * new_trade.volume
        trades_info["last_15_min_volume"] += new_trade.volume


def gbce_index(data):
    """
    Actually it's not obvious from doc what is exactly *GBCE All Share
    Index* and when I'm trying to google it I'm meeting only solutions
    for this task. X_X

    I intentionally didn't clarified what exactly this means because
    this isn't a *real-world* program and I don't want to postpone
    the solution on one more week (right now it's weekends, and I don't
    want to spend time on this task during my working days).

    So I made just a simple function which should accept prices and
    return geometric mean.

    Implementation notes: logarithmic implementation is slower than
    naive, but it prevents floats overflow.

    data - list of prices.
    """

    log_sum = .0
    for d in data:
        # this could be optimized: it's not necessary to calculate log
        # on *each* step
        log_sum += math.log(d)

    return math.exp(log_sum / len(data))


def main():
    # Some test data
    db = {
        args[0]: StockEntry(*args) for args in (
            ("TEA", TYPE_COMMON, 0, None, 100),
            ("POP", TYPE_COMMON, 8, None, 100),
            ("ALE", TYPE_COMMON, 23, None, 60),
            ("GIN", TYPE_PREFERRED, 8, 2, 100),
            ("JOE", TYPE_COMMON, 13, None, 250),
        )
    }

    print("### Dividend yield, PE ratio ###")
    price = 10
    for v in db.values():
        print("{symbol}\tdividend yield: {dividend_yield}\tPE ratio: {pe_ratio}".format(
            symbol=v.symbol,
            dividend_yield=v.dividend_yield(price),
            pe_ratio=v.pe_ratio(price),
        ))

    print("\n\n")
    print("### Volume Wieghted Stock Price ###")

    trades = Trades()
    symbol = "JPM"
    ts = datetime.datetime.now()
    for step in range(10):
        trades.add_trade(
            symbol=symbol,
            timestamp=ts,
            trade_direction=TRADE_DIRECTION_BUY if random.random() > .5 else TRADE_DIRECTION_SELL,
            price=random.randint(1, 11),
            volume=random.randint(1, 5),
        )

        trades_info = trades.trades[symbol]  # just to debug
        print("{}. Price: {} Trades: {}".format(
            step+1,
            trades.get_last_15_min_weighted_price(symbol),
            " ".join(map(str, trades_info["trades"])),
        ))

        ts += datetime.timedelta(minutes=random.randint(1, 10))

    print("\n\n")
    print("### Some Strange *GBCE All Share Index* ###")
    print(gbce_index(list(range(1, 1000000))))


if __name__ == "__main__":
    main()
