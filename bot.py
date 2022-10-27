import argparse
import asyncio
import os
from dotenv import load_dotenv
import discord
import glob
import functools
import typing
import logging
import subprocess
import sys
from discord import option
import time
from generate_fractal_image import main as generate_fractal, add_arguments_to_parser

logging.basicConfig(level=logging.INFO)

load_dotenv()

intents = discord.Intents.all()

bot = discord.Bot(debug_guilds=[987960420851666965], intents=intents) # specify the guild IDs in debug_guilds

# discord_key = os.environ["discord_key"]


def is_channel_fractal(ctx):
    return int(ctx.channel.id) == int(os.environ["channel_id"])


def create_fractal_animation(animation, width, height, color_algorithm, fps):
    # name = str(time.time())
    subprocess.run([sys.executable, 'generate_fractal_image.py', '-A', animation, '-W', width, '-H', height, '-c', color_algorithm, '-fps', fps])
    return


def create_fractal_art(algo, width, height, color_algorithm):
    name = "images/{time}".format(time=time.time())
    #subprocess.run([sys.executable, 'generate_fractal_image.py', '-a', algo, '-W', width, '-H', height, '-c', color_algorithm, '-f', name])
    parser = argparse.ArgumentParser(add_help=True)
    parser = add_arguments_to_parser(parser)
    argument_list = [
        '--fractal_algorithm', algo,
        '--width', str(width),
        '--height', str(height),
        '--color_algorithm', color_algorithm,
        '--filename', name,
        '--real_constant', '-0.844',
        '--imaginary_constant', '0.2',
    ] + "--viewport_left -1 --viewport_right 1 --viewport_top 1 --viewport_bottom -1 ".split()

    print(argument_list)
    #-cr -0.844 -ci 0.2
    arguments = parser.parse_args(argument_list)
    generate_fractal(arguments)
    return f"{name}.png"


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
@option(
    "animation",
    description="the animation algorithm to use",
    required=True,
    default="random_phoenix_julia",
    choices=["first_hue_rotation", "second_hue_rotation", "hue_cycle", "random_julia", "random_cubic_julia", "random_phoenix_julia", "random_quartic_julia", "random_walk_julia"]
)
@option("width", description="The width of the image. Default is 512", required=True, default=512)
@option("height", description="The height of the image. Default is 512", required=True, default=512)
@option(
    "color_algorithm",
    description="the coloring algorithm to use",
    required=True,
    default="simple",
    choices=["simple", "black_and_white", "hue_range", "hue_cyclic"])
@option(
    "fps",
    description="The number of frames per second in the animation. Default is 12",
    required=True,
    default=12)
async def fractal_animation(
        ctx,
        animation: str,
        width: int,
        height: int,
        color_algorithm: str,
        fps: int
):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and is_channel_fractal(ctx):
        userid = ctx.author.id
        await ctx.respond(f"<@{userid}> Starting...", ephemeral=True)
        name = await run_blocking_animation(create_fractal_animation, animation, width, height, color_algorithm, fps)
        list_of_files = glob.glob(f'images/{animation}/*')     # "*" means all if need specific format then *.csv
        my_filename = max(list_of_files, key=os.path.getctime)
        await ctx.respond(content=f"<@{userid}> **animation: {animation}, width: {width}, height: {height}, color_algorith: {color_algorithm}, fps: {fps}**", file=discord.File(my_filename))
        list_of_files = glob.glob(f'images/{animation}/*') # * means all if need specific format then *.csv
        await run_blocking_del(del_files, list_of_files)
    else:
        await ctx.respond(
            "**You can only use this command if you have AiFRENS role and are in the fractal-art room**",
            ephemeral=True)


@bot.slash_command(description='Create Fractal Art')
@option(
    "algo",
    description="the algorithm to use",
    required=True,
    choices=["mandelbrot", "julia", "burning_ship", "star", "newton", "phoenix_mandelbrot", "phoenix_julia", "cubic_mandelbrot", "quartic_mandelbrot", "cubic_julia", "experimental_cubic_julia", "quartic_julia", "buddhabrot", "buddhabrot_julia"]
)
@option("width", description="The width of the image. Default is 512", required=True, default=512)
@option("height", description="The height of the image. Default is 512", required=True, default=512)
@option(
    "color_algorithm",
    description="the coloring algorithm to use",
    required=True,
    default="simple",
    choices=["simple", "black_and_white", "hue_range", "hue_cyclic"])
async def fractal_art(
        ctx: discord.ApplicationContext,
        algo: str,
        width: int,
        height: int,
        color_algorithm: str,
    ):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and is_channel_fractal(ctx):
        userid = ctx.author.id
        await ctx.respond(f"<@{userid}> Starting...", ephemeral=True)
        name = await run_blocking_art(create_fractal_art, algo, width, height, color_algorithm)
        await ctx.respond(content=f"<@{userid}> **algorithm: {algo}, width: {width}, height: {height}, color_algorith: {color_algorithm}**", file=discord.File(name))
    else:
        await ctx.respond(
            "**You can only use this command if you have AiFRENS role and are in the fractal-art room**",
            ephemeral=True)


bot.run(os.environ["discord_key"])
