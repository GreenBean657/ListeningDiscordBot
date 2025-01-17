import importlib
import os
from json import JSONDecodeError
from warnings import catch_warnings

import discord
import json

runners = {
    "on_ready": [],
    "on_message": [],
    "on_message_delete": [],
    "on_bulk_message_delete": [],
    "on_message_edit": [],
    "on_reaction_add": [],
    "on_reaction_remove": [],
    "on_member_join": [],
    "on_member_remove": [],
    "on_guild_join": [],
    "on_guild_remove": []
}

try:
    with open(file="./config.json", mode='r') as file:
        prefix = json.load(file)["prefix"]
except Exception:
    print("WARNING: Failed to load prefix. Defaulting.")
    prefix = "$"

class MyClient(discord.Client):
    async def on_ready(self):
        for event in runners["on_ready"]:
            try:
                await event.on_trigger("on_message", {})
            except Exception as exception:
                pass

    async def on_message(self, message):
        if (message.author.id != self.user.id):
            for event in runners["on_message"]:
                try:
                    await event.on_trigger("on_message", [prefix, message])
                except Exception as exception:
                    pass

    async def on_message_delete(self, message):
        for event in runners["on_message_delete"]:
            try:
                await event.on_trigger("on_message_delete", [prefix, message])
            except Exception as exception:
                pass

    async def on_bulk_message_delete(self, messages):
        for event in runners["on_bulk_message_delete"]:
            try:
                await event.on_trigger("on_bulk_message_delete", [prefix, messages])
            except Exception as exception:
                pass

    async def on_message_edit(self, message_before, message_after):
        for event in runners["on_message_edit"]:
            try:
                await event.on_trigger("on_message_edit", [prefix, message_before, message_after])
            except Exception as exception:
                pass

    async def on_reaction_add(self, reaction, user):
        for event in runners["on_reaction_add"]:
            try:
                await event.on_trigger("on_reaction_add", [prefix, reaction, user])
            except Exception as exception:
                pass

    async def on_reaction_remove(self, reaction, user):
        for event in runners["on_reaction_remove"]:
            try:
                await event.on_trigger("on_reaction_remove", [prefix, reaction, user])
            except Exception as exception:
                pass

    async def on_member_join(self, user):
        for event in runners["on_member_join"]:
            try:
                await event.on_trigger("on_member_join", [prefix, user])
            except Exception as exception:
                pass

    async def on_member_remove(self, user):
        for event in runners["on_member_remove"]:
            try:
                await event.on_trigger("on_member_remove", [prefix, user])
            except Exception as exception:
                pass

    async def on_guild_join(self, guild):
        for event in runners["on_guild_join"]:
            try:
                await event.on_trigger("on_guild_join", [prefix, guild])
            except Exception as exception:
                pass

    async def on_guild_remove(self, guild):
        for event in runners["on_guild_remove"]:
            try:
                await event.on_trigger("on_guild_remove", [prefix, guild])
            except Exception as exception:
                pass

intents = discord.Intents.default()
intents.message_content = True

def setup_listeners() -> None:
    for filename in os.listdir("./Modules"):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f'Modules.{module_name}')
                if hasattr(module, 'Main'):
                    module_instance = module.Main()  # Create an instance
                    for event, callback in runners.items():
                        try:
                            if module_instance.get_listeners()[event]:
                                callback.append(module_instance)
                        except (AttributeError, KeyError):
                            pass
                    try:
                        module_instance.on_start()
                    except Exception:
                        pass

            except Exception as exception:
                print(f"Failed to start module '{module_name}' - {str(exception)}")

def run() -> None:
    try:
        with open(file="./config.json", mode='r') as file:
            client = MyClient(intents=intents)
            client.run(json.load(file)["token"])
    except discord.errors.LoginFailure as exception:
        print("Unable to connect: " + str(exception))
        return
    except (JSONDecodeError, FileNotFoundError, PermissionError):
        print("Failed to open JSON file.")

setup_listeners()
run()