# novel_search_command.py
import discord
from googlesearch import search

async def handle_novel_search_command(message, args, command_prefix, send_embed_message):
    # Function to handle the !novel_search command
    if len(args) < 1:
        await send_embed_message(message.channel, "Novel Search",
                                 f'**Usage:** {command_prefix}novel_search [novel_name] (number_of_results)', discord.Color.blue())
    else:
        novel_name = " ".join(args)
        num_results = 1  # Default to 1 result
        if len(args) > 1:
            num_results = min(int(args[-1]), 5)  # Limit to maximum of 5 results

        try:
            search_results = search(f"{novel_name} novel")
            top_results = list(search_results)[:num_results]  
            if top_results:
                await send_embed_message(message.channel, "Novel Search Result", "", discord.Color.blue())
                for result in top_results:
                    await message.channel.send(result)  
            else:
                await send_embed_message(message.channel, "Novel Search",
                                         "No search results found for the novel.", discord.Color.blue())
        except Exception as e:
            await send_embed_message(message.channel, "Novel Search",
                                     f"An error occurred: {str(e)}", discord.Color.red())
