import discord
from collections import defaultdict
import json
import os
from keep_alive import keep_alive
from dotenv import load_dotenv
from quote_command import handle_quote_command
from google_search_command import handle_google_search_command 
from novel_search_command import handle_novel_search_command
from prefix_command import handle_set_prefix_command
from online_status_command import handle_online_status_command
from command_info_command import handle_command_info_command

from bookmark_command import (
    handle_add_bookmark_command,
    handle_remove_bookmark_command,
    handle_view_bookmarks_command,
    handle_view_bookmarks_of_command,
    handle_paste_bookmark_command
)
from list_command import (
    handle_create_list_command,
    handle_add_to_list_command,
    handle_remove_from_list_command,
    handle_vote_command,
    handle_show_list_command,
    handle_show_all_lists_command
)


# Define the intents
intents = discord.Intents.default()
intents.members = True  # Enable the 'members' intent
intents.messages = True  # Enable the 'messages' intent
intents.message_content = True 
intents.dm_messages = True  # Enable the 'dm_messages' intent
intents.guilds = True  # Enable the 'guilds' intent


# Create a new Discord client
client = discord.Client(intents=intents)
#client = discord.Client(intents=discord.Intents.all())

# Load environment variables from .env file
load_dotenv()

# Bot login token
TOKEN = os.getenv('DISCORD_TOKEN')



# Default command prefix
default_command_prefix = '!'
command_prefix = default_command_prefix  # Default prefix initially

# JSON file to store user bookmark data
DATA_FILE = 'user_bookmarks.json'

# Initialize user_bookmarks.json with an empty dictionary if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Load user data from JSON file
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

# Save user data to JSON file
def save_user_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# JSON file to store list data
LISTS_FILE = 'lists.json'

# Initialize lists.json with an empty dictionary if it doesn't exist
if not os.path.exists(LISTS_FILE):
    with open(LISTS_FILE, 'w') as f:
        json.dump({}, f)

# Load list data from JSON file
def load_lists():
    if os.path.exists(LISTS_FILE):
        with open(LISTS_FILE, 'r') as f:
            return json.load(f)
    else:
        return defaultdict(list)

# Save list data to JSON file
def save_lists(data):
    with open(LISTS_FILE, 'w') as f:
        json.dump(data, f)

# Function to send a message with an embed
async def send_embed_message(channel, title, description, color):
    if color is None:
        color = discord.Color.blue()  # Set default color to blue

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    await channel.send(embed=embed)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} - {client.user.id}')
    print("Loading data...")
    global user_data, lists
    user_data = load_user_data()
    lists = load_lists()
    print("Data loaded successfully.")

# Event: Message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global command_prefix

    # Check if message starts with the command prefix
    if not message.content.startswith(command_prefix):
        return

    # Split the message content into command and arguments
    command_args = message.content[len(command_prefix):].split()    
    command = command_args[0]
    args = command_args[1:]

    if command in ['quote', 'q']:
        await handle_quote_command(message, send_embed_message)

    elif command in ['ask_google', 'ag']:
        await handle_google_search_command(message, args, default_command_prefix, send_embed_message)

    elif command in ['novel_search', 'ns']:
        await handle_novel_search_command(message, args, default_command_prefix, send_embed_message)
    
    elif command in ['add_bookmark', 'ab']:
        await handle_add_bookmark_command(message, args, send_embed_message, load_user_data, save_user_data)
    
    elif command in ['remove_bookmark', 'rb']:
        await handle_remove_bookmark_command(message, args, send_embed_message, load_user_data, save_user_data)
    
    elif command in ['view_bookmarks', 'vb']:
        await handle_view_bookmarks_command(message, send_embed_message, load_user_data)
    
    elif command in ['view_bookmarks_of', 'vbo']:
        await handle_view_bookmarks_of_command(message, args, send_embed_message, load_user_data, command_prefix)

    elif command in ['paste_bookmark', 'pb']:
        await handle_paste_bookmark_command(message, args, send_embed_message, load_user_data)
    
    elif command in ['create_list', 'cl']:
        await handle_create_list_command(message, args, send_embed_message, lists, save_lists)

    elif command in ['add_to_list', 'al']:
        await handle_add_to_list_command(message, args, send_embed_message, lists, save_lists)

    elif command in ['remove_from_list', 'rl']:
        await handle_remove_from_list_command(message, args, send_embed_message, lists, save_lists)

    elif command in ['vote', 'v']:
        await handle_vote_command(message, args, send_embed_message, lists, save_lists)

    elif command in ['show_list', 'sl']:
        await handle_show_list_command(message, args, send_embed_message, lists, save_lists)

    elif command in ['show_all_lists', 'sal']:
        await handle_show_all_lists_command(message, send_embed_message, lists)

    elif command in ['set_prefix', 'sp']:
        await handle_set_prefix_command(message, args, send_embed_message, command_prefix)
    
    elif command in ['check_online', 'co']:
        await handle_online_status_command(message, client, send_embed_message)

    elif command in ['commands', 'info', 'help', 'c']:
        await handle_command_info_command(message, send_embed_message, command_prefix)

# Event: Bot is about to shutdown
@client.event
async def on_disconnect():
    print("Bot is shutting down. Saving data...")
    save_lists(lists)
    save_user_data(user_data)
    print("Data saved successfully.")

# Start the Flask server
keep_alive()  

# Run the bot
client.run(TOKEN)

