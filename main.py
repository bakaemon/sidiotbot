import asyncio

import discord
import praw
import random
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix=">", description="Stupid idiot is in your service.")
reddit = praw.Reddit(client_id='q-pUEZDDw-Rnnw',
                     client_secret='scupmEfAMILyXwV1CnE0je8InLaixQ',
                     user_agent='script by u/deadmannotdeadyet',
                     check_for_async=False)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name="Dirty Coding"))


@bot.event
async def on_command_error(ctx, error):
    timeleft = round(error.retry_after, 2);
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Wah, spicy. Stop spamming. Try it again after `{timeleft}` seconds')


@bot.command()
async def talk(ctx, *args):
    message = ""
    if not args:
        quotes = "\"Imagine people have nothing to say\"" + " - Stupid Idiot"
    else:
        for arg in args:
            message += " " + arg
        quotes = "\"" + message + "\"" + " - Stupid Idiot"
    await ctx.channel.send(quotes)


@bot.command()
async def rps(ctx, *args: str):
    message = ""
    if not args:
        message = "I play rock, paper, scissor. Not with `air` you dumbass."
    else:
        message = rps_process(args)
    await ctx.channel.send(message)


def rps_process(args):
    rock = "('rock',)"
    paper = "('paper',)"
    scissor = "('scissor',)"
    poll = [rock, paper, scissor]
    result = random.choice(poll)
    arg = str(args)
    if args:
        if arg == result:
            return "It's a draw! More spicy please."
        elif arg == rock and result == scissor:
            return "It's `Scissor`! Rock! Rocks hard! And the scissor is crushed to piece."
        elif arg == rock and result == paper:
            return "It's `Paper`! What a rock is trying to hit? A paper? Loser."
        elif arg == paper and result == rock:
            return "It's `Rock`! Paper shield is effective to rock. Very realistic, you win."
        elif arg == paper and result == scissor:
            return "It's `Scissor`! Paper's trying to block something sharp? Very dumb loser."
        elif arg == scissor and result == paper:
            return "It's `Paper`! Cut, cut, cut. You ruined paper's life. You win."
        elif arg == scissor and result == rock:
            return "It's `Rock`! Your scissor died trying to cut rock. Unwise."
        else:
            return "I don't take any other than `rock`, `paper`, `scissor`."
    return "I play rock, paper, scissor. Not with `air` you dumbass."


@bot.command()
async def flip(ctx, *args):
    message = ""
    if not args:
        message = "I don't like plaything with nothing. Do it again with either `head` or `tail`"
    else:
        message = fc_process(args)
    await ctx.channel.send(message)


def fc_process(args):
    head = "('head',)"
    tail = "('tail',)"
    poll = [head, tail]
    arg = str(args)
    result = random.choice(poll)
    if args:
        if arg == head or arg == tail:
            if arg == result:
                return "It's " + filtercoin(result) + ". You win!"
            else:
                return "It's " + filtercoin(result) + ". You lose!"
        else:
            return "I suppose you don't know how to flip a coin. Loser. Place a bet before do anything else."
    return "I don't like plaything with nothing. Do it again with either `head` or `tail`"


def filtercoin(text):
    if "head" in text:
        return "head"
    elif "tail" in text:
        return "tail"


@commands.cooldown(1, 14400, commands.BucketType.user)
@bot.command()
async def spicycode(ctx):
    if ctx.channel.is_nsfw():
        fav = ["282618", "213783"]
        choose = random.choice(fav)
        block = await ctx.send(
            "Here the most spicy code: https://nhentai.net/g/" + choose + ". And to not corrupt this place, " +
            "I will only let it exist for 30s.")
        await asyncio.sleep(30)
        await block.edit(content="`This unholy being has been eradicated after time out`")


@bot.command(aliases=['nuclearcode', 'nc', 'ncode'])
async def _nuclearcode(ctx):
    if ctx.channel.is_nsfw():
        message = "Launching..."
        block = await ctx.send(message)

        for i in range(100):
            message = "Processing `" + str(i + 1) + "` codes..."
            raw_code = generateCode()
            r = requests.get("https://nhentai.net/g/" + raw_code, timeout=4)
            await asyncio.sleep(2)
            await block.edit(content=message)
            if i == 100:
                message = "I can't find any code, sorry."
                break
            else:
                if r.ok:
                    message = "I found the code `" + raw_code + "` in 100 codes. Here your sauce: " \
                                                                "https://nhentai.net/g/" + raw_code
                    break
        await block.edit(content=message)
    else:
        await ctx.send("This command is for NSFW channel only. Stop spice thing up everywhere.")


def generateCode():  # function generates a random 6 digit number
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    return code


@bot.command()
async def get(ctx, *, keywords):
    global block, embed
    sub = ['funny', 'memes', 'showerthoughts', 'jokes', 'antijokes',
           'memeeconomy', 'dankmeme', 'surrealmeme']
    i = ""
    if keywords:
        if keywords == "list":
            message = ""
            for i in sub:
                message += "`"+i + "`, "
            await ctx.send("Available subreddit: "+message)
            return
        elif keywords not in sub:
            await ctx.send("Sub-reddit doesn't exist. use `>get list` to get available subreddits.")
            return
        block = await ctx.send(f"Fetching {keywords}...")
        for count in range(1, 5):
            await block.edit(content=f"Fetching r/{keywords}...`{str(count)}/5`")
            count += 1
        subreddit = reddit.subreddit(keywords)
        all_subs = []

        top = subreddit.top(limit=50)

        for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url
        text = random_sub.selftext
        embed = discord.Embed(title=name, color=discord.Color.green(), description=text)
        embed.set_image(url = url)
        embed.set_footer(text=f"Content from r/{keywords}")
        await block.edit(content= "Completed: `5/5`", embed=embed)



@bot.command()
async def kill(ctx, member: discord.Member):  # This command will be named kill and will take two arguments: ctx (which is always needed) and the user that was mentioned
    kill_messages = [
        f'{ctx.message.author.display_name} killed {member.display_name} with a baseball bat',
        f'{ctx.message.author.display_name} killed {member.display_name} with a frying pan',
        f'{member.display_name} died from over aroused.',
        f'{member.display_name} tried to git gud on Dark Souls and died.',
        f'{member.display_name} forgot to breath and suffocated.',
        f'{member.display_name} tried to raid area 51 and got molested by aliens, hence too shameful and they committed suicide.',
        f'{member.display_name} drown in bathroom while sleeping.',
        f'{member.display_name} got bit by a strange spider, but this is reality so they died instead of being a superhero.',
        f'{member.display_name} realised {member.display_name} is not real. So {member.display_name} died from existential crisis.',
        f'{member.display_name} ate without table. Too frustrated and died.',
        f'{ctx.message.author.display_name} throw {member.display_name} into microwave. It exploded and kill both of them.',
        f'{member.display_name} is robbed, shot, groped by Dank Memer.',
        f'Dank Memer and Stupid bot join and killed {member.display_name}'
    ]  # This is where you will have your kill messages. Make sure to add the mentioning of the author (ctx.message.author.mention) and the member mentioning (member.mention) to it
    await ctx.send(random.choice(kill_messages))

@bot.command(aliases=['8ball'])
async def randomball(cxt, *args):
    if args:
        responses = ["no?",
                     "the stars tell you it's a no",
                     "certainly, no",
                     "how's about no?",
                     "yes, whatever",
                     "yup, why not",
                     "i give you it's a yes for fun",
                     "sure sure",
                     "i can tell you almost certainly, no",
                     "nope",
                     "like hell it's a yes, no",
                     "no, bother someone else",
                     "yes, cool?",
                     "do not know it is a no?",
                     "yes, I don't care",
                     "idk, just yes",
                     "hell no",
                     "yes, probably",
                     "no answer"]
    else:
        responses = ["idk what are you talking about, no",
                     "are you asking me?",
                     "too busy for your kind",
                     "can you not??",
                     "i'm 8ball, not fball",
                     "look like you are blind, cuz no question there."]
    await cxt.send(random.choice(responses))
bot.run('ODI0MjQ5Njg4OTY5OTY5Njg1.YFsoVw.tSNTj3XzoIV18WTSf1QqDQCw7p8')
