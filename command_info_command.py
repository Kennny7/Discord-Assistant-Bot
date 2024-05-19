# command_info_command.py
import discord

async def handle_command_info_command(message, send_embed_message, command_prefix):
    # Command to display all available commands categorized
    command_categories = {
        "Bookmark Commands": [
            f'**{command_prefix}add_bookmark <name> [source_link]** - Add a bookmark',
            f'**{command_prefix}remove_bookmark <name>** - Remove a bookmark',
            f'**{command_prefix}view_bookmarks** - View your bookmarks',
            f'**{command_prefix}view_bookmarks_of @user** - View someone else\'s bookmarks'
            f'**{command_prefix}paste_bookmark** - Paste the source link of a bookmark'
        ],
        "List Commands": [
            f'**{command_prefix}create_list <name>** - Create a list',
            f'**{command_prefix}add_to_list <list_name> <item>** - Add an item to a list',
            f'**{command_prefix}remove_from_list <list_name> <item>** - Remove an item from a list',
            f'**{command_prefix}vote <list_name> <item>** - Vote for an item in a list',
            f'**{command_prefix}show_list <list_name>** - Display a list with votes',
            f'**{command_prefix}show_all_lists** - Display all available lists'
        ],
        "Other Commands": [
            f'**{command_prefix}quote** - Get a random quote',
            f'**{command_prefix}novel_search <novel_name> <number_of_results(max=5)>** - Search for novels',
            f'**{command_prefix}ask_google <prompt>** - Get a response from Google',
            f'**{command_prefix}set_prefix <new_prefix>** - Change the command prefix',
            #f'**{command_prefix}check_online <username>** - Checks if the user is online',
            f'**{command_prefix}commands/info/help** - Show all available commands'
        ],
        "Notes:": [
            f'**[+]** You can also use command initials to trigger them',
            f'**[+]** If the bot is not responding or malfunctions, it is always your fault'
        ] # type: ignore
        # Add more categories and commands here as needed
    }

    for category, commands in command_categories.items():
        description = "\n".join(commands)
        await send_embed_message(message.channel, f"{category}", description, discord.Color.blue())
