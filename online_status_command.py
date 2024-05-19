import discord
import subprocess

async def handle_online_status_command(message, client, send_message):
    if message.content.startswith('!check_online'):
        user = message.mentions[0] if message.mentions else None
        if user:
            member = message.guild.get_member(user.id)
            if member:
                if member.status != discord.Status.offline:
                    await send_message(message.channel, f"Pinging {user.name}...")
                    try:
                        ip_address = await get_user_ip(client, member)
                        output = ping(ip_address)
                        await send_message(message.channel, f"Ping response for {user.name}: {output}")
                    except Exception as e:
                        await send_message(message.channel, f"An error occurred: {e}")
                else:
                    await send_message(message.channel, f"{user.name} is offline.")
            else:
                await send_message(message.channel, "User not found in this server.")
        else:
            await send_message(message.channel, "Please mention a user.")

async def get_user_ip(client, member):
    user_data = await client.http.get_user(member.id)
    ip_address = user_data.get('connected_accounts', {}).get('voice', {}).get('address')
    return ip_address

def ping(ip_address):
    try:
        output = subprocess.check_output(["ping", "-c", "1", ip_address])
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Failed to ping {ip_address}: {e}"
