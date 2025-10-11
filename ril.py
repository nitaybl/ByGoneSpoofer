import discord
import asyncio

# WARNING: Running a self-bot is against Discord's Terms of Service
# and can lead to account termination. Use at your own risk.

# --- Configuration ---
# Replace "YOUR_USER_TOKEN" with your Discord user token.
# Do NOT share this token with anyone.
TOKEN = "YOUR_DISCORD_TOKEN_HERE"  # REMOVED FOR SECURITY

# Replace "YOUR_VOICE_CHANNEL_ID" with the ID of the voice channel you want to join.
VOICE_CHANNEL_ID = 1376952077196197922
# --- End of Configuration ---

class SelfBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        print('Connecting to the voice channel...')
        try:
            channel = self.get_channel(VOICE_CHANNEL_ID)
            if isinstance(channel, discord.VoiceChannel):
                await channel.connect()
                print(f'Successfully joined the voice channel: {channel.name}')
                # Mute the user after joining the channel
                await self.change_voice_state(channel=channel, self_mute=True, self_deaf=False)
                print('User has been muted.')
            else:
                print(f'Error: The channel with ID {VOICE_CHANNEL_ID} is not a voice channel.')
                await self.close()
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.close()

    async def on_voice_state_update(self, member, before, after):
        # This event is triggered when a user's voice state changes.
        # We can use it to ensure the bot stays in the channel if disconnected.
        if member == self.user and before.channel and not after.channel:
            print("Disconnected from the voice channel. Reconnecting...")
            try:
                channel = self.get_channel(VOICE_CHANNEL_ID)
                if isinstance(channel, discord.VoiceChannel):
                    await channel.connect()
                    print(f'Reconnected to the voice channel: {channel.name}')
                    await self.change_voice_state(channel=channel, self_mute=True, self_deaf=False)
                    print('User has been muted again.')
            except Exception as e:
                print(f"Failed to reconnect: {e}")

if __name__ == "__main__":
    if TOKEN == "YOUR_USER_TOKEN" or VOICE_CHANNEL_ID == 123456789012345678:
        print("Please configure the TOKEN and VOICE_CHANNEL_ID in the script.")
    else:
        try:
            client = SelfBot()
            client.run(TOKEN)
        except discord.errors.LoginFailure:
            print("Invalid token provided. Please check your token.")
        except Exception as e:
            print(f"An error occurred while trying to run the bot: {e}")