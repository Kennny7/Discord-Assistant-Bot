# google_search_command.py
import discord
import requests
from googlesearch import search
from bs4 import BeautifulSoup


async def handle_google_search_command(message, args, default_command_prefix, send_embed_message):
    # Function to handle the !ask_google command
    if len(args) < 1:
        await send_embed_message(message.channel, "Google Search",
                                 f'**Usage:** {default_command_prefix}ask_google [question]', discord.Color.blue())
    else:
        question = " ".join(args)
        try:
            # Perform Google search
            search_results = list(search(question, num=1, stop=1, pause=2))
            if search_results:
                # Get the URL of the first search result
                url = search_results[0]
                
                # Fetch the webpage
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract the description text from the webpage
                description_tag = soup.find('meta', attrs={'name': 'description'})
                if description_tag:
                    description = description_tag['content']
                    await send_embed_message(message.channel, "Google Search Result", description, discord.Color.blue())
                else:
                    await send_embed_message(message.channel, "Google Search",
                                             "No description found for the search result.", discord.Color.blue())
            else:
                await send_embed_message(message.channel, "Google Search",
                                         "No search results found.", discord.Color.blue())
        except Exception as e:
            await send_embed_message(message.channel, "Google Search",
                                     f"An error occurred: {str(e)}", discord.Color.blue())
