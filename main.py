import importlib
import os
from json import JSONDecodeError
from warnings import catch_warnings

import discord
import json

runners = {
    "on_ready":[],
    "on_message":[],
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