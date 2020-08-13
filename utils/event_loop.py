import config


class Sleep:
    def __await__(self):
        return (yield self)

    def __init__(self, seconds):
        self.seconds = seconds


async def sleep(amount_of_ticks):
    for _ in range(amount_of_ticks):
        await Sleep(config.TIC_TIMEOUT)
