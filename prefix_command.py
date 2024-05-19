# prefix_command.py
import discord

async def handle_set_prefix_command(message, args, send_embed_message, command_prefix):
    # Function to handle the !set_prefix command
    if len(args) != 1:
        await send_embed_message(message.channel, "Custom Command",
                                 f'**Usage:** {command_prefix}set_prefix [new_prefix]',
                                 discord.Color.gold())

    else:
        command_prefix = args[0]  # Change the command prefix
        await send_embed_message(message.channel, "Custom Command",
                                 f"Command prefix changed to '{args[0]}'",
                                 discord.Color.green())
