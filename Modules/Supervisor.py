class Main():
    def __str__(self) -> str:
        return "ModWatch"

    def on_start(self) -> None:
        return

    def get_listeners(self):
        return {
            "on_ready":True,
            "on_message":False
        }
    async def on_trigger(self,trigger: str, args):
        print("Bot started!")