class Main():
    def __str__(self) -> str:
        return "ModWatch"

    def on_start(self) -> None:
        return

    def get_listeners(self):
        return {
            "on_ready":False,
            "on_message":True
        }
    async def on_trigger(self,trigger: str, args):
        await args[1].reply("I replied")