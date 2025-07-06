import discord
from discord.ext import commands
from discord import Embed, Color
from discord import app_commands
import asyncio
from datetime import datetime
import random
import signal
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from core.config import config

# Initialize
console = Console()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class BotState:
    def __init__(self):
        self.ai_enabled = True
        self.shutting_down = False
        self.ai_personality = "neutral"
        self.primary_location = "Chouf, Baakline, Lebanon"

bot.state = BotState()

# ======================
# Core Functionality
# ======================

def generate_ai_response(message_content: str, mood: str) -> str:
    """Generate dynamic responses based on mood"""
    prompts = {
        "angry": [
            f"WHAT DO YOU WANT? '{message_content}'? HOW ABOUT NO.",
            "I SWEAR TO GOD IF YOU KEEP PINGING ME...",
            "BOLD WORDS COMING FROM SOMEONE IN BAN RANGE."
        ],
        "neutral": [
            f"You said: '{message_content}'. Interesting.",
            "I'm processing your request... slowly.",
            "PeteSeek acknowledges your message."
        ],
        "friendly": [
            f"Hey friend! I heard you say '{message_content}'!",
            "I'd love to chat about that!",
            "PeteSeek is happy to help!"
        ]
    }
    return random.choice(prompts[mood])

async def update_status():
    """Update the status embed"""
    status = "🟢 ONLINE" if bot.state.ai_enabled else "🟠 DISABLED"
    embed = Embed(
        title=f"PeteSeek Status: {status}",
        description=f"```Location: {bot.state.primary_location}\nMood: {bot.state.ai_personality.upper()}```",
        color=Color.green() if bot.state.ai_enabled else Color.orange()
    )
    
    try:
        channel = bot.get_channel(config.status_channel)
        if channel:
            message = await channel.fetch_message(config.status_message_id)
            await message.edit(embed=embed)
    except Exception as e:
        console.print(f"[red]Status update failed: {e}[/red]")

# ======================
# Commands
# ======================

@bot.hybrid_command(name="petestatus", description="Show system diagnostics")
async def petestatus(ctx: commands.Context):
    """System status command"""
    embed = Embed(title="PeteSeek Status", color=Color.blue())
    embed.add_field(
        name="System",
        value=f"```🟢 Operational\n📍 {bot.state.primary_location}```",
        inline=False
    )
    embed.add_field(
        name="AI Mode",
        value=f"```{'🟢 ENABLED' if bot.state.ai_enabled else '🔴 DISABLED'}```",
        inline=True
    )
    await ctx.send(embed=embed)

@bot.hybrid_command(name="petetoggle", description="Toggle AI responses")
async def petetoggle(ctx: commands.Context):
    """Toggle AI with status updates"""
    bot.state.ai_enabled = not bot.state.ai_enabled
    await update_status()
    status = "ENABLED ✅" if bot.state.ai_enabled else "DISABLED ❌"
    await ctx.send(f"AI response system has been {status}", ephemeral=True)

@bot.hybrid_command(name="petemood", description="Change AI personality")
@app_commands.choices(mood=[
    app_commands.Choice(name="Angry", value="angry"),
    app_commands.Choice(name="Neutral", value="neutral"),
    app_commands.Choice(name="Friendly", value="friendly")
])
async def petemood(interaction: discord.Interaction, mood: app_commands.Choice[str]):
    """Change AI personality (slash command)"""
    bot.state.ai_personality = mood.value
    await interaction.response.send_message(
        f"Personality set to **{mood.value.upper()}**", 
        ephemeral=True
    )

# ======================
# Event Handlers
# ======================

@bot.event
async def on_ready():
    """Bot startup handler"""
    console.print(Panel.fit(
        f"[bold green]PeteSeek Online as {bot.user.name}[/]",
        border_style="blue"
    ))
    
    # Signal handling
    signal.signal(signal.SIGINT, lambda *_: asyncio.create_task(shutdown()))
    signal.signal(signal.SIGTERM, lambda *_: asyncio.create_task(shutdown()))
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        console.print(f"[green]✓ Synced {len(synced)} commands[/green]")
    except Exception as e:
        console.print(f"[red]Command sync failed: {e}[/red]")
    
    await update_status()

@bot.event
async def on_message(message):
    """Handle message events"""
    if not bot.state.ai_enabled or message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            clean_content = message.content.replace(f"<@{bot.user.id}>", "").strip()
            response = generate_ai_response(clean_content, bot.state.ai_personality)
            await message.reply(response)
    
    await bot.process_commands(message)

async def shutdown():
    """Graceful shutdown procedure"""
    if not bot.state.shutting_down:
        bot.state.shutting_down = True
        console.print("[yellow]Shutting down gracefully...[/yellow]")
        await bot.close()

# ======================
# Execution
# ======================

if __name__ == "__main__":
    try:
        console.print(Panel(
            "[bold]Starting PeteSeek...",
            subtitle="Ctrl+C to exit",
            border_style="green"
        ))
        
        # Load token from .env (secure)
        from dotenv import load_dotenv
        import os
        
        load_dotenv()  # Load .env file
        token = os.getenv("DISCORD_TOKEN")
        
        # Validate token format
        if not token or not token.startswith("MT"):
            console.print("[red]Invalid or missing token![/red]")
            console.print("[yellow]Ensure .env exists with DISCORD_TOKEN=your_token[/yellow]")
            sys.exit(1)
            
        bot.run(token)
        
    except KeyboardInterrupt:
        console.print("[yellow]Shutdown initiated[/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
    finally:
        asyncio.run(shutdown())