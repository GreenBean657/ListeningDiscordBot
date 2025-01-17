class Main():
    def __str__(self) -> str:
        return "ModWatch"

    def on_start(self) -> None:
        return

    def get_listeners(self):
        return {
            "on_ready": False,
            "on_message": True,
            "on_message_delete": False,
            "on_bulk_message_delete": False,
            "on_message_edit": False,
            "on_reaction_add": False,
            "on_reaction_remove": False,
            "on_member_join": False,
            "on_member_remove": False,
            "on_guild_join": False,
            "on_guild_remove": False
        }
    async def on_trigger(self,trigger: str, args):
        await args[1].reply("I replied")