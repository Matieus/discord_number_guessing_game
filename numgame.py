import sys
import discord
import random
import asyncio
from math import log2
from discord.ext import commands


class Numgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["nug", "nrg"])
    async def numgame(self, ctx, maximum: int = 100):
        if 10000 < maximum or maximum < 10:
            return

        number = random.randint(1, maximum)
        guess = int(log2(maximum)//1)
        embed = discord.Embed(
                colour=discord.Colour.from_rgb(203, 75, 27),
                timestamp=ctx.message.created_at)
        embed.set_footer(
                text=f"{ctx.author}",
                icon_url=ctx.author.avatar)

        console_start = sys.version.split(" ")[0]
        embed.description = "```Python\n"
        embed.description += f"Python {console_start} shell\n"

        embed.description += f">>> numgame(max={maximum})\n"
        embed.description += f"Odgadnij liczbę od 1 do {maximum}!\n>>> ```"
        mes = await ctx.send(embed=embed)
        while guess != 0:
            try:
                msg = await self.bot.wait_for(
                    'message', check=check(
                            ctx.author, ctx.channel), timeout=30)
                attempt = int(msg.content)
            except asyncio.TimeoutError:
                embed.description = embed.description[:-3]
                embed.description += "\nZa długi czas oczekiwania\n```"
                await mes.edit(embed=embed)
                break

            embed.description = embed.description[:-3]
            embed.description += f"{attempt}\n```"
            await mes.edit(embed=embed)
            guess -= 1

            embed.description = embed.description[:-3]
            variant = conjugation(guess)
            if attempt > number and guess != 0:
                embed.description += f"Too many! {variant}\n>>> ```"

            elif attempt < number and guess != 0:
                embed.description += f"Not enough! {variant}\n>>> ```"

            elif attempt == number:
                embed.description += "Well done you! ```"
                guess = 0

            elif attempt != number and guess == 0:
                embed.description += "Nie udało Ci się! ```"
                guess = 0

            await mes.edit(embed=embed)

        await asyncio.sleep(1)
        embed.description = embed.description[:-3]
        embed.description += f"To {number}!```"
        await mes.edit(embed=embed)


def setup(bot):
    bot.add_cog(Numgame(bot))


def check(author, channel):
    def inner_check(message):
        if message.author != author:
            return False
        elif message.channel != channel:
            return False
        try:
            int(message.content)
            return True
        except ValueError:
            return False
    return inner_check


def conjugation(guess: int) -> str:
    if guess > 1:
        return f"{guess} tries left"

    elif guess > 1 and guess % 10 < 5:
        return f"{guess} try left"
