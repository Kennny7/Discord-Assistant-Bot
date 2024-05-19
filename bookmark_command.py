import discord

async def handle_add_bookmark_command(message, args, send_embed_message, load_user_data, save_user_data):
    
    if len(args) < 1:
        await send_embed_message(message.channel, "Error", "Please provide a name for the bookmark.", discord.Color.red())
        return
    # Function to handle the !add_bookmark command
    bookmark_name = args[0]
    source_link = args[1] if len(args) > 1 else None

    # Load user data
    user_data = load_user_data()
    user_id = str(message.author.id)

    # Create a new list if the user doesn't have one
    if user_id not in user_data:
        user_data[user_id] = []

    # Add the new bookmark
    user_data[user_id].append({'name': bookmark_name, 'source': source_link})
    save_user_data(user_data)

    await send_embed_message(message.channel, "Bookmark Added",
                             f"Bookmark '{bookmark_name}' added successfully.",
                             discord.Color.green())

async def handle_remove_bookmark_command(message, args, send_embed_message, load_user_data, save_user_data):
    # Function to handle the !remove_bookmark command
    bookmark_name = args[0]

    # Load user data
    user_data = load_user_data()
    user_id = str(message.author.id)

    # Remove the bookmark if it exists
    if user_id in user_data:
        user_data[user_id] = [b for b in user_data[user_id] if b['name'] != bookmark_name]
        save_user_data(user_data)
        await send_embed_message(message.channel, "Bookmark Removed",
                                 f"Bookmark '{bookmark_name}' removed successfully.",
                                 discord.Color.green())
    else:
        await send_embed_message(message.channel, "Bookmark Removal Error",
                                 "You don't have any bookmarks to remove.",
                                 discord.Color.red())

async def handle_view_bookmarks_command(message, send_embed_message, load_user_data):
    # Function to handle the !view_bookmarks command
    user_data = load_user_data()
    user_id = str(message.author.id)

    # Get user bookmarks
    bookmarks = user_data.get(user_id, [])

    if bookmarks:
        bookmark_list = '\n'.join([f"- {b['name']}: {b['source']}" for b in bookmarks])
        await send_embed_message(message.channel, "Your Bookmarks",
                                 f"**Your Bookmarks:**\n{bookmark_list}",
                                 discord.Color.blue())
    else:
        await send_embed_message(message.channel, "Your Bookmarks",
                                 "You don't have any bookmarks yet.",
                                 discord.Color.blue())

async def handle_view_bookmarks_of_command(message, args, send_embed_message, load_user_data, command_prefix):
    # Command to view bookmarks of another user
    if len(message.mentions) != 1:
        await send_embed_message(message.channel, "View Bookmarks",
                                 f"Usage: {command_prefix}view_bookmarks_of @user",
                                 discord.Color.red())
        return

    target_user = str(message.mentions[0].id)
    user_data = load_user_data()

    # Get user bookmarks
    bookmarks = user_data.get(target_user, [])

    if bookmarks:
        bookmark_list = '\n'.join([f"- {b['name']}: {b['source']}" for b in bookmarks])
        await send_embed_message(message.channel, f"Bookmarks of {message.mentions[0].display_name}",
                                 f"**Bookmarks of {message.mentions[0].display_name}:**\n{bookmark_list}",
                                 discord.Color.blue())
    else:
        await send_embed_message(message.channel, f"Bookmarks of {message.mentions[0].display_name}",
                                 "This user doesn't have any bookmarks yet.",
                                 discord.Color.blue())

async def handle_paste_bookmark_command(message, args, send_embed_message, load_user_data):
    # Command to paste a bookmark link
    if not args:
        await send_embed_message(message.channel, "Paste Bookmark Error",
                                 "Usage: ?paste_bookmark <bookmark_name>",
                                 discord.Color.red())
        return

    bookmark_name = " ".join(args)

    # Load user data
    user_data = load_user_data()
    user_id = str(message.author.id)

    # Search for the bookmark name in user's bookmarks
    bookmark = next((b for b in user_data.get(user_id, []) if b['name'] == bookmark_name), None)

    if bookmark:
        await message.channel.send(f"Source link for '{bookmark_name}': {bookmark['source']}")
                
    else:
        await send_embed_message(message.channel, "Bookmark Paste Error",
                                 f"No bookmark found with the name '{bookmark_name}'.",
                                 discord.Color.red())
