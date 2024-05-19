# quote_command.py
import discord
import requests

async def handle_quote_command(message, send_embed_message):
    try:
        response = requests.get('https://api.quotable.io/random')
        if response.status_code == 200:
            data = response.json()
            quote = data['content'] + " - " + data['author']
            await send_embed_message(message.channel, "Quote", f'**Quote:** {quote}', discord.Color.blue())
        else:
            await send_embed_message(message.channel, "Quote", "Failed to fetch a quote. Please try again later.", discord.Color.red())
    except Exception as e:
        print("Error fetching quote:", e)
        await send_embed_message(message.channel, "Quote", "Failed to fetch a quote. Please try again later.", discord.Color.red())
