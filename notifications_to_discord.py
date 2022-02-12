import discord, os, getopt, sys
from random import randint

open_file = " "
class db():
    path = os.path.dirname(__file__)
    path = path.replace('\\' , '/')
    path = path[2:]
    configUser = {}

def main(argv: str) -> None:
    global open_file
    if argv == []:
        print("Don't run this file, it will not do anything by itself")
        os.system('pause')
    else:
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["open=","admin"])
        except getopt.GetoptError:
            print('python post-it.py -o <file to open> -a <run as admin>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-o"):
                news_name = arg
        if news_name == '@multiple':
            send_message('@multiple')
        elif news_name.startswith('repos.'):
            news_name = news_name[5:]
            send_message("repos", news_name)
        elif news_name.startswith('followers.'):
            news_name = news_name[10:]
            send_message("followers", news_name)

def send_message(type: str, news_name: str) -> None:
    path = db.path + '/config.json'
    with open(path, 'r') as file :
        configImport = file.read()
        db.configUser = eval(configImport)
        token = db.configUser["bot_discord_token"]
        channel_for_notifications = db.configUser["id_channel_discord"]
        name = db.configUser["targeted_account"]
    
    color = randint(1,16777215)

    if type == "followers":
        if news_name == '@multiple':
            embed_title = "New followers !"
            embed_description = f"Check it out on [Github](https://github.com/{name}?tab=followers)"
        else:
            embed_title = "New follower !"
            embed_description = f"{news_name} subscribes ! Check out his/her account on [Github](https://github.com/{news_name})"
    elif type == "repos":
        if news_name == '@multiple':
            embed_title = "New repositories detected !"
            embed_description = f"New repositories have been created ! check it out on [Github](https://github.com/{name}?tab=repositories)"
        else:    
            embed_title = "New repository detected !"
            embed_description = f"New repository: `{news_name}`, check it out on [Github](https://github.com/{name}/{news_name})"
    client = discord.Client()
    @client.event
    async def on_ready():
        channel_receiver: discord.TextChannel = client.get_channel(channel_for_notifications)
        embed=discord.Embed(title = embed_title, description = embed_description, color = color)
        await channel_receiver.send(embed=embed)
        exit()
    client.run(token)

if __name__ == "__main__":
    main(sys.argv[1:])