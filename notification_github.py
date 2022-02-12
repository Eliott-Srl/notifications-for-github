import requests, os , time
from subprocess import Popen, DEVNULL
 
class db():
    configDefault = {
        "targeted_account": "Eliott-srl",
        "notify_new_repos": "True",
        "notify_new_followers": "True",
        "msg_discord": "True",
        "bot_discord_token": "DEFAULT",
        "id_channel_discord": "DEFAULT",
        "cron_time": 300
        }
    configUser = {}
    path = os.path.dirname(__file__)
    path = path.replace('\\' , '/')
    path = path[2:]
    true = ["True", "true", "TRUE"]

def export_json(what: dict, where: str) -> None:
    path = db.path + '/' + where
    with open(path, 'w') as file :
        file.write(str(what))

def import_json(where: str) -> dict:
    path = db.path + '/' + where
    if not os.path.isfile(path):
        return "wrong path"
    else:
        with open(path, 'r') as file :
            configImport = file.read()
            return eval(configImport)

def init() -> None:
    print("\
 ##   ##    ###     ######   ######  #######   ######    ####      ##     ######   ######    ###    ##   ##   #### \n \
###  ##   ## ##    # ## #     ##     ##  ##     ##     ##  ##    ####    # ## #     ##     ## ##   ###  ##  ##   ## \n \
#### ##  ##   ##     ##       ##     ##         ##    ##         ####      ##       ##    ##   ##  #### ##  ### \n \
## ####  ##   ##     ##       ##     ####       ##    ##        ##  ##     ##       ##    ##   ##  ## ####    ### \n \
##  ###  ##   ##     ##       ##     ##         ##    ##        ######     ##       ##    ##   ##  ##  ###      ### \n \
##   ##   ## ##      ##       ##     ##         ##     ##  ##  ##    ##    ##       ##     ## ##   ##   ##  ##   ## \n \
##   ##    ###      ####    ######  ####      ######    ####   ##    ##   ####    ######    ###    ##   ##   #####")
    print(' for github ;)')
    print()
    if not os.path.exists(f'{db.path}/data'):
        os.makedirs(f'{db.path}/data')
    if import_json('config.json') == "wrong path":
        export_json(db.configDefault, 'config.json')
        print("Fill in the config.json and replace the DEFAULT by your values")
        os.system('pause')
    else:
        db.configUser = import_json('config.json')

def notifications(repo_name: str) -> None:
    for parameters in db.configUser:
        if parameters == "msg_discord" and db.configUser[parameters] in db.true:
            path = db.path + '/' + "notifications_to_discord.py"
            process = Popen(['python', path, "-o", repo_name], stdout=DEVNULL, stderr=DEVNULL)
            print('message send :)')

def newsChecker(what) -> None:
    username = db.configUser["targeted_account"]
    url = f"https://api.github.com/users/{username}/{what}"
    if requests.get(url).status_code == 200:
        user_data = requests.get(url).json()
    else:
        user_data = import_json(f'data/output_{what}.json')
    export_json(user_data, f'data/output_{what}.json')
    outputName = []
    outputId = []
    output = {}

    if what == "followers":
        name_search = "login"
    elif what == "repos":
        name_search = "name"

    for listMain in range(len(user_data)):
        for element in user_data[listMain]:
            if element == "id":
                outputId.append(user_data[listMain][element])
            elif element == name_search:
                outputName.append(user_data[listMain][element])
    for name in range(len(outputName)):
            output[outputName[name]] = outputId[name]

    if import_json(f'data/{what}_save.json') == "wrong path":
        export_json(output, f'data/{what}_save.json')
        last_output = output
    else:
        last_output = import_json(f'data/{what}_save.json')

    if output == last_output:
        pass
    else:
        news = []
        for repositories in output:
            if repositories in last_output:
                pass
            else:
                news.append(repositories)
                print(repositories, 'is new')
        export_json(output, f'data/{what}_save.json')
        if len(news) > 1:
            notifications('@multiple')
        else:
            notifications(f"{what}.{repositories}")

        time.sleep(2)
        print(100*"\n")
        print('scanning for news ...')

def main() -> None:
    init()
    time.sleep(4)
    if db.configUser["msg_discord"] in db.true:
        if db.configUser["bot_discord_token"] == "DEFAULT" or db.configUser["id_channel_discord"] == "DEFAULT":
            print("Fill in the config.json and replace the DEFAULT by your values")
            os.system('pause')
            quit()
    print('scanning for news ...')
    cron_time = db.configUser["cron_time"]
    while True:
        if db.configUser["notify_new_repos"] in db.true:
                newsChecker('repos')
        time.sleep(cron_time/2)
        if db.configUser["notify_new_followers"] in db.true:
                newsChecker('followers')
        time.sleep(cron_time/2)
        
if __name__ == "__main__":
    main()