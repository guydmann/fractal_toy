import asyncio
import os
from dotenv import load_dotenv
import discord 
# from discord.ext import commands, tasks
import glob
import functools
import typing
import logging
import subprocess
import sys
from discord.commands import Option
import time

logging.basicConfig(level=logging.INFO)

load_dotenv()

intents = discord.Intents.all()

bot = discord.Bot(debug_guilds=[987960420851666965], intents=intents) # specify the guild IDs in debug_guilds

# discord_key = os.environ["discord_key"]

# async def is_channel_fractal(ctx):
#     return ctx.channel.id == 1001295615508086924

def create_fractal_animation(animation, width, height, color_algorithm, fps):
    # name = str(time.time())
    subprocess.run([sys.executable, 'generate_fractal_image.py', '-A', animation, '-W', width, '-H', height, '-c', color_algorithm, '-fps', fps])
    return

def create_fractal_art(algo, width, height, color_algorithm):
    name = str(time.time())
    subprocess.run([sys.executable, 'generate_fractal_image.py', '-a', algo, '-W', width, '-H', height, '-c', color_algorithm, '-f', name])
    return name

    # os.system("python generate_fractal_image.py -a mandelbrot -A random_phoenix_julia -W 512 -H 512 -c hue_range -fps 12")

def create_phoenix_cyclic():
    os.system("python generate_fractal_image.py -a mandelbrot -A random_phoenix_julia -W 512 -H 512 -c hue_cyclic -fps 12")

def create_julia_range():
    os.system("python generate_fractal_image.py -a mandelbrot -A random_julia -W 512 -H 512 -c hue_range -fps 12")

def create_julia_cyclic():
    os.system("python generate_fractal_image.py -a mandelbrot -A random_julia -W 512 -H 512 -c hue_cyclic -fps 12")

async def run_blocking_animation(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(create_fractal_animation, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await bot.loop.run_in_executor(None, func)

async def run_blocking_art(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(create_fractal_art, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await bot.loop.run_in_executor(None, func)

def del_files(list_of_files):
    for f in list_of_files:
        os.remove(f)
    
async def run_blocking_del(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(del_files, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await bot.loop.run_in_executor(None, func)

@bot.command(description='Create Fractal Animation')
async def fractal_animation(ctx, animation: Option(str, "use /animation_list to get a list of options or see pinned messages", required = True, default = 'random_phoenix_julia'),
    width: Option(str, "Default is 512, experiment with this", required = True, default = '512'), height: Option(str, "Default is 512, experiment with this", required = True, default = '512'), color_algorithm: Option(str, "simple, black_and_white, hue_range, hue_cyclic", required = True, default = 'hue_range'),
    fps: Option(str, "Default is 12, experiment with this", required = True, default = '12')):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and ctx.channel.id == 1001295615508086924:
        userid = ctx.author.id
        await ctx.respond(f"<@{userid}> Starting...", ephemeral=True)
        name = await run_blocking_animation(create_fractal_animation, animation, width, height, color_algorithm, fps)
        list_of_files = glob.glob('images/' + animation + '/*') # * means all if need specific format then *.csv
        my_filename = max(list_of_files, key=os.path.getctime)
        await ctx.respond(content=f"<@{userid}> **animation: {animation}, width: {width}, height: {height}, color_algorith: {color_algorithm}, fps: {fps}**", file=discord.File(my_filename))
        list_of_files = glob.glob('images/' + animation + '/*') # * means all if need specific format then *.csv
        await run_blocking_del(del_files, list_of_files)
    else:
        await ctx.respond(f"**You can only use this command if you have AiFRENS role and are in the fractal-art room**", ephemeral=True)

@bot.command(description='Create Fractal Art')
async def fractal_art(ctx, algo: Option(str, "use /algo_list to get a list of options or see pinned messages", required = True, default = 'mandelbrot'),
    width: Option(str, "Default is 512, experiment with this", required = True, default = '512'), height: Option(str, "Default is 512, experiment with this", required = True, default = '512'), color_algorithm: Option(str, "simple, black_and_white, hue_range, hue_cyclic", required = True, default = 'hue_range'),
    ):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and ctx.channel.id == 1001295615508086924:
        userid = ctx.author.id
        await ctx.respond(f"<@{userid}> Starting...", ephemeral=True)
        name = await run_blocking_art(create_fractal_art, algo, width, height, color_algorithm)
        list_of_files = glob.glob('images/*') # * means all if need specific format then *.csv
        my_filename = max(list_of_files, key=os.path.getctime)
        await ctx.respond(content=f"<@{userid}> **algorithm: {algo}, width: {width}, height: {height}, color_algorith: {color_algorithm}**", file=discord.File(my_filename))
        # list_of_files = glob.glob('images/*') # * means all if need specific format then *.csv
        # await run_blocking_del(del_files, list_of_files)
    else:
        await ctx.respond(f"**You can only use this command if you have AiFRENS role and are in the fractal-art room**", ephemeral=True)

@bot.command(description='Show list of fractal algorithms')
async def algo_list(ctx):
    # role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if ctx.channel.id == 1001295615508086924:
        await ctx.respond("mandelbrot, julia, burning_ship, star, newton, phoenix_mandelbrot, phoenix_julia, cubic_mandelbrot, quartic_mandelbrot, cubic_julia, experimental_cubic_julia, quartic_julia, buddhabrot, buddhabrot_julia")
    else:
        await ctx.respond(f"**You can only use this command if you are in the fractal-art room**", ephemeral=True)

@bot.command(description='Show list of fractal animations')
async def animation_list(ctx):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and ctx.channel.id == 1001295615508086924:
        await ctx.respond("first_hue_rotation, second_hue_rotation, hue_cycle, random_julia, random_cubic_julia, random_phoenix_julia, random_quartic_julia, random_walk_julia")
    else:
        await ctx.respond(f"**You can only use this command if you have AiFRENS role and are in the fractal-art room**", ephemeral=True)

bot.run(os.environ["discord_key"])