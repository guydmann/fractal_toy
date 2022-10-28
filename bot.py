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

logging.basicConfig(level=logging.INFO)

load_dotenv()

intents = discord.Intents.all()

bot = discord.Bot(debug_guilds=[987960420851666965], intents=intents) # specify the guild IDs in debug_guilds


def is_channel_fractal(ctx):
    return int(ctx.channel.id) == int(os.environ["channel_id"])


def create_fractal_animation(animation, width, height, color_algorithm, fps):
    # name = str(time.time())
    subprocess.run([sys.executable, 'generate_fractal_image.py', '-A', animation, '-W', width, '-H', height, '-c', color_algorithm, '-fps', fps])
    return


def create_fractal_art(fractal_args):
    name = "images/{time}".format(time=time.time())
    argument_list = [sys.executable, 'generate_fractal_image.py', '--filename', name]
    for key, value in fractal_args.items():
        argument_list.append(f"--{key}")
        argument_list.append(str(value))
    print(argument_list)
    subprocess.run(argument_list)
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
    default="random_phoenix_julia",
    choices=["first_hue_rotation", "second_hue_rotation", "hue_cycle", "random_julia", "random_cubic_julia", "random_phoenix_julia", "random_quartic_julia", "random_walk_julia"]
)
@option("width", description="The width of the image. Default is 512", default=512)
@option("height", description="The height of the image. Default is 512", default=512)
@option(
    "color_algorithm",
    description="the coloring algorithm to use",
    default="simple",
    choices=["simple", "black_and_white", "hue_range", "hue_cyclic"])
@option(
    "fps",
    description="The number of frames per second in the animation. Default is 12",
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
    "fractal_algorithm",
    description="the algorithm to use",
    default="mandelbrot",
    choices=["mandelbrot", "julia", "burning_ship", "star", "newton", "phoenix_mandelbrot", "phoenix_julia", "cubic_mandelbrot", "quartic_mandelbrot", "cubic_julia", "experimental_cubic_julia", "quartic_julia", "buddhabrot", "buddhabrot_julia"]
)
@option("width", description="The width of the image. Default is 512", default=512)
@option("height", description="The height of the image. Default is 512", default=512)
@option(
    "color_algorithm",
    description="the coloring algorithm to use",
    default="simple",
    choices=["simple", "black_and_white", "hue_range", "hue_cyclic"])
@option(
    "image_filtering",
    default="none",
    description="applies specific filters to the image for different visual effects",
    choices=['none', 'basic', 'glow_takeover', 'additive_glow', 'blur'])
@option("viewport_left", description="coordinate of left edge of view port", required=False)
@option("viewport_right", description="coordinate of right edge of view port", required=False)
@option("viewport_top", description="coordinate of top edge of view port", required=False)
@option("viewport_bottom", description="coordinate of bottom edge of view port", required=False)
@option("real_constant", description="the real portion of the constant in Julia type calculations.", required=False)
@option("imaginary_constant", description="the imaginary portion of the constant in Julia type calculations.", required=False)
@option("precision", description="The precision to be used in the fractal calculations", required=False)
@option("hue_start_degree", description="use to define hue range for hue_range amd hue_cyclic color algorithms", required=False)
@option("hue_end_degree", description="use to define hue range for hue_range color algorithm", required=False)
@option("hue_step_shift", description="use to define hue steps to take in the hue_cyclic color algorithm", required=False)
@option("color_count", description="use to define the number of colors to cycle through in the cyclic color algorithms", required=False)
async def fractal_art(
        ctx: discord.ApplicationContext,
        fractal_algorithm: str,
        width: int,
        height: int,
        color_algorithm: str,
        image_filtering: str,
        viewport_left: float,
        viewport_right: float,
        viewport_top: float,
        viewport_bottom: float,
        real_constant: float,
        imaginary_constant: float,
        precision: int,
        hue_start_degree: int,
        hue_end_degree: int,
        hue_step_shift: int,
        color_count: int,
):
    role = discord.utils.get(ctx.guild.roles, name="AiFREN")
    if role in ctx.author.roles and is_channel_fractal(ctx):
        userid = ctx.author.id
        await ctx.respond(f"<@{userid}> Starting...", ephemeral=True)
        fractal_args = {
            "fractal_algorithm": fractal_algorithm,
            "color_algorithm": color_algorithm,
            "width": width,
            "height": height,
        }
        if viewport_left:
            fractal_args["viewport_left"] = viewport_left
        if viewport_right:
            fractal_args["viewport_right"] = viewport_right
        if viewport_top:
            fractal_args["viewport_top"] = viewport_top
        if viewport_bottom:
            fractal_args["viewport_bottom"] = viewport_bottom
        if real_constant:
            fractal_args["real_constant"] = real_constant
        if imaginary_constant:
            fractal_args["imaginary_constant"] = imaginary_constant
        if precision:
            fractal_args["precision"] = precision
        if hue_start_degree:
            fractal_args["hue_start_degree"] = hue_start_degree
        if hue_end_degree:
            fractal_args["hue_end_degree"] = hue_end_degree
        if hue_step_shift:
            fractal_args["hue_step_shift"] = hue_step_shift
        if color_count:
            fractal_args["color_count"] = color_count
        if image_filtering:
            fractal_args["image_filtering"] = image_filtering
        print(fractal_args)
        name = await run_blocking_art(create_fractal_art, fractal_args)
        await ctx.respond(content=f"<@{userid}> **algorithm: {fractal_algorithm}, width: {width}, height: {height}, color_algorith: {color_algorithm}**", file=discord.File(name))
    else:
        await ctx.respond(
            "**You can only use this command if you have AiFRENS role and are in the fractal-art room**",
            ephemeral=True)


bot.run(os.environ["discord_key"])
