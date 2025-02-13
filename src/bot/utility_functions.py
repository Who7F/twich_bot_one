"""Utility functions for the bot."""
import asyncio

running_tasks = set()

def send_message(irc, channel, message):
    """Send a message to the channel."""
    irc.send(f"PRIVMSG #{channel} :{message}\n".encode('utf-8'))
    print(f"INFO: Message Sent to {channel} channel: {message}")


async def delayed_response(irc, channel_name, response, delay):
    print('syo')
    await asyncio.sleep(1)
    print('f')
    send_message(irc, channel_name, response)


async def make_response(irc, username, channel_name, bot_username, command, commands):
    """This function makes a response to the chat commands."""
    for cmd, data in commands["chatCommands"].items():
        if command == cmd or command in data.get("aliases", []):
            response = data["response"].replace("{BOT_USERNAME}", bot_username)
            response = data["response"].replace("{username}", username)
            
            delay = data.get("sleeptime", 0) 
            if delay > 0 and delay < 10:

                task = asyncio.create_task(delayed_response(irc, channel_name, response, delay))
                
                #asyncio.create_task(delayed_response(irc, channel_name, response, delay))
                running_tasks.add(task)
                task.add_done_callback(running_tasks.discard) 
                
                
            else:
                send_message(irc, channel_name, response)
