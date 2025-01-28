def send_message(irc, channel, message):
    irc.send(f"PRIVMSG #{channel} :{message}\n".encode('utf-8'))
