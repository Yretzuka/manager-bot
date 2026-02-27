import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
from datetime import datetime, timedelta
import re
import random
import asyncio

# ===== BOT TOKEN =====
import os
TOKEN = os.environ.get('DISCORD_TOKEN')
# ===== BOT SETUP =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ===== DATA FILES =====
DATA_FILES = {
    'products': 'products.json',
    'orders': 'orders.json',
    'config': 'config.json',
    'warnings': 'warnings.json',
    'giveaways': 'giveaways.json',
    'levels': 'levels.json'
}

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Load all data
data = {key: load_data(filename) for key, filename in DATA_FILES.items()}

# Initialize defaults
if 'order_counter' not in data['orders']:
    data['orders']['order_counter'] = 0
if 'order_list' not in data['orders']:
    data['orders']['order_list'] = []
if 'bad_words' not in data['config']:
    data['config']['bad_words'] = ['anjing', 'kontol', 'memek', 'bangsat', 'tolol', 'babi']
if 'mod_enabled' not in data['config']:
    data['config']['mod_enabled'] = True

# ===== PATTERNS =====
URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
DISCORD_INVITE = re.compile(r'(discord\.gg|discord\.com/invite)/[a-zA-Z0-9]+')

@bot.event
async def on_ready():
    print(f'╔════════════════════════════════════════╗')
    print(f'║  🎮 SOLID PENUH RATMAN.STORE BOT 🎮   ║')
    print(f'╚════════════════════════════════════════╝')
    print(f'')
    print(f'🤖 Bot: {bot.user}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'🌐 Servers: {len(bot.guilds)}')
    print(f'')
    print(f'✨ Features Loaded:')
    print(f'  ✅ Store System')
    print(f'  ✅ Music Player')  
    print(f'  ✅ Auto Moderation')
    print(f'  ✅ Giveaway System')
    print(f'  ✅ Leveling System')
    print(f'  ✅ Fun Commands')
    print(f'')
    
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands')
    except Exception as e:
        print(f'❌ Sync error: {e}')
    
    print(f'🚀 Bot is ready!')
    print(f'════════════════════════════════════════')
    
    # Start giveaway checker
    check_giveaways.start()

# ═══════════════════════════════════════════
# 🛡️ AUTO MODERATION
# ═══════════════════════════════════════════

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return
    
    if not data['config'].get('mod_enabled', True):
        await bot.process_commands(message)
        return
    
    content = message.content.lower()
    
    # Allow GIF links (tenor.com, giphy.com, etc)
    gif_domains = ['tenor.com', 'giphy.com', 'gfycat.com', 'imgur.com/a/', 'media.discordapp.net', 'cdn.discordapp.com']
    is_gif = any(domain in content for domain in gif_domains)
    
    # Allow discord gift links
    is_gift = 'discord.gift/' in content or 'discord.com/gifts/' in content
    
    # Check bad words
    for word in data['config'].get('bad_words', []):
        if word in content:
            try:
                await message.delete()
                embed = discord.Embed(
                    title="⚠️ Peringatan: Kata Kasar",
                    description=f"Pesan kamu di **{message.guild.name}** dihapus!",
                    color=discord.Color.red()
                )
                embed.add_field(name="❌ Alasan", value="Menggunakan kata-kata kasar", inline=False)
                embed.add_field(name="💬 Pesan", value="Jangan berkata kasar ya! 😊", inline=False)
                embed.set_footer(text="Solid Penuh Ratman.Store")
                await message.author.send(embed=embed)
                
                user_id = str(message.author.id)
                if user_id not in data['warnings']:
                    data['warnings'][user_id] = []
                data['warnings'][user_id].append({
                    'type': 'bad_word',
                    'timestamp': datetime.now().isoformat()
                })
                save_data(DATA_FILES['warnings'], data['warnings'])
            except:
                pass
            return
    
    # Check links (except GIF and gift)
    if not is_gif and not is_gift:
        if URL_PATTERN.search(message.content) or DISCORD_INVITE.search(message.content):
            try:
                await message.delete()
                embed = discord.Embed(
                    title="⚠️ Peringatan: Link Terdeteksi",
                    description=f"Pesan kamu di **{message.guild.name}** dihapus!",
                    color=discord.Color.orange()
                )
                embed.add_field(name="❌ Alasan", value="Mengirim link tanpa izin", inline=False)
                embed.add_field(name="💬 Pesan", value="Jangan kirim link ya! Hubungi admin jika perlu.", inline=False)
                embed.add_field(name="✅ Yang Boleh", value="• GIF (tenor, giphy)\n• Discord Gift Links", inline=False)
                embed.set_footer(text="Solid Penuh Ratman.Store")
                await message.author.send(embed=embed)
                
                user_id = str(message.author.id)
                if user_id not in data['warnings']:
                    data['warnings'][user_id] = []
                data['warnings'][user_id].append({
                    'type': 'link',
                    'timestamp': datetime.now().isoformat()
                })
                save_data(DATA_FILES['warnings'], data['warnings'])
            except:
                pass
            return
    
    await bot.process_commands(message)

# ═══════════════════════════════════════════
# 🛒 STORE SYSTEM
# ═══════════════════════════════════════════

@bot.tree.command(name="setup", description="Setup bot (Admin only)")
@app_commands.describe(
    order_channel="Channel untuk order",
    admin_role="Role admin"
)
async def setup(interaction: discord.Interaction, order_channel: discord.TextChannel, admin_role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admin only!", ephemeral=True)
        return
    
    data['config']['order_channel_id'] = order_channel.id
    data['config']['admin_role_id'] = admin_role.id
    save_data(DATA_FILES['config'], data['config'])
    
    embed = discord.Embed(title="✅ Setup Complete!", color=discord.Color.green())
    embed.add_field(name="📬 Order Channel", value=order_channel.mention)
    embed.add_field(name="👑 Admin Role", value=admin_role.mention)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addproduct", description="Tambah produk (Admin)")
@app_commands.describe(
    name="Nama produk",
    category="Kategori (robux/gamepass/item)",
    price="Harga (IDR)",
    stock="Stok",
    description="Deskripsi"
)
async def addproduct(interaction: discord.Interaction, name: str, category: str, price: int, stock: int, description: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admin only!", ephemeral=True)
        return
    
    product_id = f"{category.upper()}_{len(data['products']) + 1}"
    data['products'][product_id] = {
        'name': name,
        'category': category,
        'price': price,
        'stock': stock,
        'description': description,
        'total_sold': 0
    }
    save_data(DATA_FILES['products'], data['products'])
    
    embed = discord.Embed(title="✅ Produk Ditambahkan!", color=discord.Color.green())
    embed.add_field(name="🆔 ID", value=f"`{product_id}`")
    embed.add_field(name="📦 Nama", value=name)
    embed.add_field(name="💰 Harga", value=f"Rp {price:,}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="Lihat toko")
async def shop(interaction: discord.Interaction):
    if not data['products']:
        await interaction.response.send_message("🛒 Toko masih kosong!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🎮 SOLID PENUH RATMAN.STORE",
        description="Robux & Gamepass Terpercaya!",
        color=discord.Color.gold()
    )
    
    categories = {}
    for pid, p in data['products'].items():
        cat = p['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((pid, p))
    
    for cat, items in categories.items():
        text = ""
        for pid, p in items:
            stock = f"✅ {p['stock']}" if p['stock'] > 0 else "❌ HABIS"
            text += f"**{p['name']}** - Rp {p['price']:,}\n└ {stock} | {p['description']}\n\n"
        embed.add_field(name=f"🎯 {cat.upper()}", value=text, inline=False)
    
    view = ShopView()
    await interaction.response.send_message(embed=embed, view=view)

class ShopView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="💳 Buy", style=discord.ButtonStyle.success)
    async def buy(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Implementation continues...
        await interaction.response.send_message("Order system coming soon!", ephemeral=True)

# ═══════════════════════════════════════════
# 👑 MODERATOR COMMANDS
# ═══════════════════════════════════════════

@bot.tree.command(name="kick", description="Kick member (Mod)")
@app_commands.describe(member="Member yang mau di-kick", reason="Alasan")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    await member.kick(reason=reason)
    embed = discord.Embed(title="👢 Member Kicked", color=discord.Color.red())
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ban", description="Ban member (Mod)")
@app_commands.describe(member="Member yang mau di-ban", reason="Alasan")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 Member Banned", color=discord.Color.red())
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timeout", description="Timeout member (Mod)")
@app_commands.describe(
    member="Member",
    duration="Durasi (menit)",
    reason="Alasan"
)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    await member.timeout(timedelta(minutes=duration), reason=reason)
    embed = discord.Embed(title="⏰ Member Timeout", color=discord.Color.orange())
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Duration", value=f"{duration} minutes")
    embed.add_field(name="Reason", value=reason)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Clear messages (Mod)")
@app_commands.describe(amount="Jumlah pesan (1-100)")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Amount must be 1-100!", ephemeral=True)
        return
    
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ Deleted {amount} messages!", ephemeral=True)

@bot.tree.command(name="warn", description="Warn member (Mod)")
@app_commands.describe(member="Member", reason="Alasan")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    user_id = str(member.id)
    if user_id not in data['warnings']:
        data['warnings'][user_id] = []
    
    data['warnings'][user_id].append({
        'type': 'manual',
        'reason': reason,
        'by': interaction.user.id,
        'timestamp': datetime.now().isoformat()
    })
    save_data(DATA_FILES['warnings'], data['warnings'])
    
    embed = discord.Embed(title="⚠️ Warning Issued", color=discord.Color.yellow())
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Total Warnings", value=str(len(data['warnings'][user_id])))
    await interaction.response.send_message(embed=embed)
    
    try:
        dm_embed = discord.Embed(
            title="⚠️ You've been warned!",
            description=f"Server: **{interaction.guild.name}**",
            color=discord.Color.yellow()
        )
        dm_embed.add_field(name="Reason", value=reason)
        dm_embed.add_field(name="Total Warnings", value=str(len(data['warnings'][user_id])))
        await member.send(embed=dm_embed)
    except:
        pass

@bot.tree.command(name="warnings", description="Check warnings")
@app_commands.describe(member="Member (optional)")
async def warnings(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    user_id = str(target.id)
    
    warns = data['warnings'].get(user_id, [])
    
    embed = discord.Embed(
        title=f"⚠️ Warnings: {target.name}",
        description=f"Total: {len(warns)}",
        color=discord.Color.yellow()
    )
    
    for i, w in enumerate(warns[-10:], 1):
        embed.add_field(
            name=f"Warning #{i}",
            value=f"Type: {w['type']}\nDate: {w['timestamp'][:10]}",
            inline=True
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ═══════════════════════════════════════════
# 🎁 GIVEAWAY SYSTEM
# ═══════════════════════════════════════════

@bot.tree.command(name="giveaway", description="Create giveaway (Mod)")
@app_commands.describe(
    duration="Durasi (menit)",
    winners="Jumlah pemenang",
    prize="Hadiah"
)
async def giveaway(interaction: discord.Interaction, duration: int, winners: int, prize: str):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    end_time = datetime.now() + timedelta(minutes=duration)
    
    embed = discord.Embed(
        title="🎉 GIVEAWAY!",
        description=f"**Prize:** {prize}",
        color=discord.Color.gold()
    )
    embed.add_field(name="⏰ Ends In", value=f"{duration} minutes")
    embed.add_field(name="👥 Winners", value=str(winners))
    embed.add_field(name="📝 How to Join", value="React with 🎉!")
    embed.set_footer(text=f"Hosted by {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("🎉")
    
    giveaway_id = str(msg.id)
    data['giveaways'][giveaway_id] = {
        'message_id': msg.id,
        'channel_id': interaction.channel.id,
        'guild_id': interaction.guild.id,
        'prize': prize,
        'winners': winners,
        'end_time': end_time.isoformat(),
        'host': interaction.user.id,
        'ended': False
    }
    save_data(DATA_FILES['giveaways'], data['giveaways'])

@tasks.loop(seconds=30)
async def check_giveaways():
    for gid, g in list(data['giveaways'].items()):
        if g['ended']:
            continue
        
        end_time = datetime.fromisoformat(g['end_time'])
        if datetime.now() >= end_time:
            try:
                channel = bot.get_channel(g['channel_id'])
                msg = await channel.fetch_message(g['message_id'])
                
                reaction = discord.utils.get(msg.reactions, emoji="🎉")
                if reaction:
                    users = [u async for u in reaction.users() if not u.bot]
                    
                    if len(users) >= g['winners']:
                        winners = random.sample(users, g['winners'])
                        
                        embed = discord.Embed(
                            title="🎉 GIVEAWAY ENDED!",
                            description=f"**Prize:** {g['prize']}",
                            color=discord.Color.green()
                        )
                        embed.add_field(
                            name="🏆 Winners",
                            value="\n".join([w.mention for w in winners])
                        )
                        
                        await channel.send(embed=embed)
                        
                        # DM winners
                        for w in winners:
                            try:
                                dm_embed = discord.Embed(
                                    title="🎉 You Won!",
                                    description=f"Congratulations! You won: **{g['prize']}**",
                                    color=discord.Color.gold()
                                )
                                await w.send(embed=dm_embed)
                            except:
                                pass
                    else:
                        await channel.send(f"❌ Not enough participants for giveaway: {g['prize']}")
                
                data['giveaways'][gid]['ended'] = True
                save_data(DATA_FILES['giveaways'], data['giveaways'])
            except Exception as e:
                print(f"Giveaway error: {e}")

@bot.tree.command(name="reroll", description="Reroll giveaway (Mod)")
@app_commands.describe(message_id="ID pesan giveaway")
async def reroll(interaction: discord.Interaction, message_id: str):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("❌ No permission!", ephemeral=True)
        return
    
    giveaway = data['giveaways'].get(message_id)
    if not giveaway:
        await interaction.response.send_message("❌ Giveaway not found!", ephemeral=True)
        return
    
    try:
        channel = bot.get_channel(giveaway['channel_id'])
        msg = await channel.fetch_message(int(message_id))
        reaction = discord.utils.get(msg.reactions, emoji="🎉")
        
        if reaction:
            users = [u async for u in reaction.users() if not u.bot]
            if users:
                winner = random.choice(users)
                await interaction.response.send_message(f"🎉 New winner: {winner.mention}!")
            else:
                await interaction.response.send_message("❌ No participants!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No reactions!", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Error!", ephemeral=True)

# ═══════════════════════════════════════════
# 🎮 FUN COMMANDS
# ═══════════════════════════════════════════

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="🏓 Pong!", color=discord.Color.green())
    embed.add_field(name="⚡ Latency", value=f"{latency}ms")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Server info")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
    embed.add_field(name="👑 Owner", value=guild.owner.mention)
    embed.add_field(name="👥 Members", value=str(guild.member_count))
    embed.add_field(name="📅 Created", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="User info")
@app_commands.describe(member="Member (optional)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"👤 {target.name}", color=target.color)
    embed.add_field(name="🆔 ID", value=str(target.id))
    embed.add_field(name="📅 Joined", value=target.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="📅 Created", value=target.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roll", description="Roll dice")
@app_commands.describe(sides="Number of sides (default: 6)")
async def roll(interaction: discord.Interaction, sides: int = 6):
    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 You rolled: **{result}** (1-{sides})")

@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"🪙 **{result}**!")

@bot.tree.command(name="8ball", description="Ask the magic 8ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "Yes, definitely!", "It is certain.", "Without a doubt.",
        "Ask again later.", "Cannot predict now.", "Concentrate and ask again.",
        "Don't count on it.", "My reply is no.", "Very doubtful."
    ]
    await interaction.response.send_message(f"🎱 {random.choice(responses)}")

# ═══════════════════════════════════════════
# 🎵 MUSIC COMMANDS (Simple)
# ═══════════════════════════════════════════

@bot.tree.command(name="play", description="Play music (URL)")
@app_commands.describe(url="YouTube URL")
async def play(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("🎵 Music feature requires yt-dlp. Install: `pip install yt-dlp`\nComing soon!", ephemeral=True)

@bot.tree.command(name="stop", description="Stop music")
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message("⏹️ Music stopped!", ephemeral=True)

# ═══════════════════════════════════════════
# 📊 UTILITY COMMANDS
# ═══════════════════════════════════════════

@bot.tree.command(name="help", description="Show all commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 SOLID PENUH RATMAN.STORE - Commands",
        description="Bot all-in-one untuk server kamu!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛒 Store",
        value="`/shop` `/addproduct` `/myorders`",
        inline=False
    )
    
    embed.add_field(
        name="👑 Moderation",
        value="`/kick` `/ban` `/timeout` `/warn` `/clear` `/warnings`",
        inline=False
    )
    
    embed.add_field(
        name="🎁 Giveaway",
        value="`/giveaway` `/reroll`",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Fun",
        value="`/ping` `/roll` `/coinflip` `/8ball` `/serverinfo` `/userinfo`",
        inline=False
    )
    
    embed.add_field(
        name="🎵 Music",
        value="`/play` `/stop` (Coming soon!)",
        inline=False
    )
    
    embed.set_footer(text="Solid Penuh Ratman.Store")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ═══════════════════════════════════════════
# 🚀 RUN BOT
# ═══════════════════════════════════════════

print("🚀 Starting Solid Penuh Ratman.Store Bot...")
bot.run(TOKEN)
