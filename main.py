import os

import discord


class OurClient(discord.Client):
    """***SOVIET THEME SONG PLAYS***"""
    async def close(self, *args, **kwargs):
        """UwU daddy, I'll clean you up oWo"""
        super().close(*args, **kwargs)
        for vc in self.voice_clients:
            await vc.disconnect()

    async def on_ready(self):
        print("hi")

    async def on_message(self, message):
        # messages are guaranteed to not just be whitespace
        argv = message.content.split(" ")
        if not argv[0].lower().startswith("bgm"):
            return

        author: discord.abc.User = message.author

        if not isinstance(author, discord.Member):
            # not able to query voice channels
            return

        if author.bot:
            return

        voice_state = author.voice
        if voice_state is None or voice_state.channel is None:
            return

        # get the voice client for the channel
        curr_vc = None
        for vc in self.voice_clients:
            if vc.channel.id == voice_state.channel.id:
                curr_vc = vc

        if curr_vc is None:
            # not connected, connect
            curr_vc = await voice_state.channel.connect()

            await curr_vc.play(discord.FFmpegPCMAudio("Suteki Meppou.mp3"))
            return

        # we're connected
        if len(argv) == 1:
            if curr_vc.is_playing():
                return

            await vc.play(discord.FFmpegPCMAudio("Suteki Meppou.mp3"))

        what = argv[1].lower()
        if what == "stop":
            curr_vc.stop()
            return

        if what == "pause":
            curr_vc.pause()
            return

        if what == "resume":
            curr_vc.resume()
            return

        if what == "play":
            if curr_vc.is_playing():
                return

            if curr_vc.is_paused():
                curr_vc.resume()
                return

            await vc.play(discord.FFmpegPCMAudio("Suteki Meppou.mp3"))
            return


if __name__ == "__main__":
    client = OurClient()
    client.run(os.environ["TOKEN"])
    """ the hard way
    try:
        client.loop.run_until_complete(
            client.start(os.environ["TOKEN"]))
    except (KeyboardInterrupt, SystemExit):
        client.loop.run_until_complete(client._trap())
    finally:
        client.loop.close()
    """
