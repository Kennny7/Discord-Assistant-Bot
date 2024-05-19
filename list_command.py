import discord 

async def handle_create_list_command(message, args, send_embed_message, lists, save_lists):
    # Command to create a new list
    if 'Admin' in [role.name for role in message.author.roles]:
        list_name = ' '.join(args)
        lists[list_name] = []
        await send_embed_message(message.channel, "List Creation",
                                 f"List '{list_name}' created successfully.",
                                 discord.Color.green())
        save_lists(lists)  # Save lists after modification
    else:
        await send_embed_message(message.channel, "List Creation",
                                 "You don't have permission to create a list.",
                                 discord.Color.red())

async def handle_add_to_list_command(message, args, send_embed_message, lists, save_lists):
    # Command to add an item to a list
    if 'Admin' in [role.name for role in message.author.roles]:
        list_name, item = args[0], ' '.join(args[1:])
        if list_name in lists:
            lists[list_name].append({"item": item, "votes": 0})
            await send_embed_message(message.channel, "List Modification",
                                    f"Item '{item}' added to list '{list_name}'.",
                                    discord.Color.green())
            save_lists(lists)  # Save lists after modification
        else:
            await send_embed_message(message.channel, "List Modification",
                                    f"List '{list_name}' does not exist.",
                                    discord.Color.red())
    else:
        await send_embed_message(message.channel, "List Modification",
                                "You don't have permission to add items to a list.",
                                discord.Color.red())

async def handle_remove_from_list_command(message, args, send_embed_message, lists, save_lists):
    # Command to remove an item from a list
    if 'Admin' in [role.name for role in message.author.roles]:
        list_name, item = args[0], ' '.join(args[1:])
        if list_name in lists:
            for i, entry in enumerate(lists[list_name]):
                if entry["item"] == item:
                    lists[list_name].pop(i)
                    await send_embed_message(message.channel, "List Modification",
                                            f"Item '{item}' removed from list '{list_name}'.",
                                            discord.Color.green())
                    save_lists(lists)  # Save lists after modification
                    break
            else:
                await send_embed_message(message.channel, "List Modification",
                                        f"Item '{item}' not found in list '{list_name}'.",
                                        discord.Color.red())
        else:
            await send_embed_message(message.channel, "List Modification",
                                    f"List '{list_name}' does not exist.",
                                    discord.Color.red())
    else:
        await send_embed_message(message.channel, "List Modification",
                                "You don't have permission to remove items from a list.",
                                discord.Color.red())

async def handle_vote_command(message, args, send_embed_message, lists, save_lists):
    # Command to vote for an item in a list
    list_name, item = args[0], ' '.join(args[1:])
    if list_name in lists:
        for entry in lists[list_name]:
            if entry["item"] == item:
                entry["votes"] += 1
                await send_embed_message(message.channel, "Vote",
                                         f"You voted for item '{item}'.",
                                         discord.Color.green())
                save_lists(lists)  # Save lists after modification
                break
        else:
            await send_embed_message(message.channel, "Vote",
                                     f"Item '{item}' not found in list '{list_name}'.",
                                     discord.Color.red())
    else:
        await send_embed_message(message.channel, "Vote",
                                 f"List '{list_name}' does not exist.",
                                 discord.Color.red())

async def handle_show_list_command(message, args, send_embed_message, lists, save_lists):
    # Command to display a list
    list_name = ' '.join(args)
    if list_name in lists:
        sorted_list = sorted(lists[list_name], key=lambda x: x["votes"], reverse=True)
        list_content = '\n'.join([f"{i+1}. {entry['item']} - Votes: {entry['votes']}" for i, entry in enumerate(sorted_list)])
        await send_embed_message(message.channel, "List Display",
                                 f"**{list_name}**\n{list_content}",
                                 discord.Color.blue())
        save_lists(lists)  # Save lists after modification
    else:
        await send_embed_message(message.channel, "List Display",
                                 f"List '{list_name}' does not exist.",
                                 discord.Color.red())

async def handle_show_all_lists_command(message, send_embed_message, lists):
    # Command to display all available lists
    if lists:
        sorted_lists = sorted(lists.items(), key=lambda x: sum(entry['votes'] for entry in x[1]), reverse=True)
        list_info = []
        for list_name, entries in sorted_lists:
            total_elements = len(entries)
            total_votes = sum(entry['votes'] for entry in entries)
            list_info.append(f"**{list_name}** - Total Elements: {total_elements}, Total Votes: {total_votes}")

        list_content = '\n'.join(list_info)
        await send_embed_message(message.channel, "Available Lists (Ranked by Total Votes)",
                                 list_content,
                                 discord.Color.blue())
    else:
        await send_embed_message(message.channel, "Available Lists",
                                 "There are no lists available.",
                                 discord.Color.red())


