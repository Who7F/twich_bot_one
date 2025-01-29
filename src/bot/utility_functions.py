"""Utility functions for the bot."""

def send_message(irc, channel, message):
    """Send a message to the channel."""
    irc.send(f"PRIVMSG #{channel} :{message}\n".encode('utf-8'))
    print(f"INFO: Message Sent to {channel} channel: {message}")
