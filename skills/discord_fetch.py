import discord

# Make sure to replace this with your actual bot token
TOKEN = 'your-api-key'

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

async def fetch_messages_from_server(server):
    await client.wait_until_ready()
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name.lower() == server:
                try:
                    messages = await channel.history(limit=10).flatten()
                    print(f"--- Messages from {channel.name} in {guild.name} ---")
                    for message in messages:
                        print(f"{message.author.name}: {message.content}")
                    return
                except discord.errors.Forbidden:
                    print(f"Cannot access messages in {channel.name} of {guild.name}. Missing permissions.")
    print("Channel 'Roblox' not found in any server the bot is in.")

@client.event
async def on_ready(query):
    print(f'Logged in as {client.user.name}')
    await fetch_messages_from_server(query)
    await client.close()

client.run(TOKEN)