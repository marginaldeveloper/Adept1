import os
import subprocess
import ctypes
import sys
import time
from tqdm import tqdm
from colorama import Fore, Style
import speech_recognition as sr
import pyttsx3
import shutil
import tkinter as tk
from tkinter import simpledialog
import asyncio
import aiohttp
import datetime
import os
# SAVE FILE
def save_results_to_file(username, found_accounts):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{username}_{timestamp}.txt"
    file_path = os.path.join(os.getcwd(), filename)  
    with open(file_path, "w", encoding="utf-8") as f:
        if found_accounts:
            f.write(f"Результаты поиска для юзернейма '{username}':\n\n")
            for account in found_accounts:
                f.write(f"{account}\n")
        else:
            f.write(f"Аккаунты для юзернейма '{username}' не найдены.\n")
    print(f"Результаты сохранены в файл: {file_path}")


# Copy of sherlock... but be silent :3
async def search_usernames(username):
    urls = [
        ("Instagram", f"https://www.instagram.com/{username}", "📷"),
        ("TikTok", f"https://www.tiktok.com/@{username}", "🎵"),
        ("Twitter", f"https://twitter.com/{username}", "🐦"),
        ("Facebook", f"https://www.facebook.com/{username}", "📘"),
        ("YouTube", f"https://www.youtube.com/@{username}", "▶️"),
        ("SoundCloud", f"https://soundcloud.com/{username}", "🎶"),
        ("Telegram", f"https://t.me/{username}", "📱"),
        ("VK", f"https://vk.com/{username}", "🔵"),
        ("Roblox", f"https://www.roblox.com/user.aspx?username={username}", "🎮"),
        ("Twitch", f"https://www.twitch.tv/{username}", "🎥"),
        ("Pinterest", f"https://www.pinterest.com/{username}", "📌"),
        ("GitHub", f"https://www.github.com/{username}", "💻"),
        ("Reddit", f"https://www.reddit.com/u/{username}/", "❓"),
    ]

    found_accounts = []
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url, timeout=10) for _, url, _ in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for (resource_name, url, emoji), response in zip(urls, responses):
            if isinstance(response, aiohttp.ClientResponse) and response.status == 200:
                found_accounts.append(f"{emoji} {resource_name}: {url}")
    return found_accounts
def get_username_from_gui():
    root = tk.Tk()
    root.withdraw()  
    username = simpledialog.askstring("Поиск юзернейма", "Введите юзернейм для поиска:")
    return username
def launch_username_search_gui():
    username = get_username_from_gui()
    if not username:
        print("Юзернейм не введен.")
        return

    print(f"Ищу юзернейм: {username}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    found_accounts = loop.run_until_complete(search_usernames(username))

    if found_accounts:
        print("Найденные аккаунты:")
        for account in found_accounts:
            print(account)
    else:
        print("Аккаунты не найдены.")
    save_results_to_file(username, found_accounts)

def launch_username_search_console():
    username = input("Введите юзернейм для поиска: ").strip()
    if not username:
        print("Юзернейм не введен.")
        return

    print(f"Ищу юзернейм: {username}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    found_accounts = loop.run_until_complete(search_usernames(username))

    if found_accounts:
        print("Найденные аккаунты:")
        for account in found_accounts:
            print(account)
    else:
        print("Аккаунты не найдены.")
    save_results_to_file(username, found_accounts)


def launch_username_search(engine, r):
    print_gradient_text("Выберите способ ввода: терминал или графическое окно.")
    engine.runAndWait()

    print("Выберите способ ввода:")
    print("1. Графическое окно")
    print("2. Терминал")

    choice = input("Ваш выбор (1 или 2): ").strip()
    if choice == "1":
        launch_username_search_gui()
    elif choice == "2":
        launch_username_search_console()
    else:
        print("Неверный выбор.")  
# BANNER
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
          _,.
        ,` -.)
       ( _/-\\-._
      /,|`--._,-^|            ,
      \_| |`-._/||          ,'|
        |  `-, / |         /  /
        |     || |        /  /
         `r-._||/   __   /  /
     __,-<_     )`-/  `./  /
    '  \   `---'   \   /  /
        |           |./  /
        /           //  /
    \_/' \         |/  /
     |    |   _,^-'/  /
     |    , ``  (\/  /_
      \,.->._    \X-=/^
      (  /   `-._//^`
       `Y-.____(__}
        |     {__)       
 _______  ______   _______  _______ _________              __       _______ 
(  ___  )(  __  \ (  ____ \(  ____ )\__   __/    |\     /|/  \     (  __   )
| (   ) || (  \  )| (    \/| (    )|   ) (       | )   ( |\/) )    | (  )  |
| (___) || |   ) || (__    | (____)|   | |       | |   | |  | |    | | /   |
|  ___  || |   | ||  __)   |  _____)   | |       ( (   ) )  | |    | (/ /) |
| (   ) || |   ) || (      | (         | |        \ \_/ /   | |    |   / | |
| )   ( || (__/  )| (____/\| )         | |         \   /  __) (_ _ |  (__) |
|/     \|(______/ (_______/|/          )_(          \_/   \____/(_)(_______)
    """)
    print_gradient_text("""Приветствую, Монолит.
    """)

# pretty  TEXT
def print_gradient_text(text):
    red = 255  
    green = 0 
    step = max(1, 255 // len(text))
    
    for char in text:
        color_code = f"\033[38;2;{red};{green};0m"
        print(f"{color_code}{char}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.05)
        
        if red > 0 and green < 255:
            red -= step
            green += step
    print()

def show_progress_bar(task_name, duration):
    print(f"\n{task_name}")
    for _ in tqdm(range(100), desc=task_name, ncols=70, colour="yellow"):
        time.sleep(duration / 100)

# trigger WORDS
spotifwords = {"спотик", "спотифай", "включи спотик", "spotify", "spotik", "spotik spotik", "включи spotik", "спотифайка", "включи музыку", "слушай спотик", "включи spotify", "спотик музыка", "музыка spotify", "включи плейлист", "плейлист спотик", "слушать спотик", "включи спотифай", "спотифай музыка"}
discordwords = {"дискорд", "включи дискорд", "открой дискорд", "включи discord", "discord", "дискорд дискорд", "discord discord", "диск", "открой диск", "включи дискорд канал", "открой discord", "включи сервер", "дискорд сервер", "дискод"}
gmodwords = {"гмод", "гаррис", "гаррис мод", "включи гмод", "включи гаррис мод", "gmod", "включи гаррис", "гмодик", "играть в гмод", "запусти гмод", "игра гаррис мод", "гмод сервер", "гмод игра", "запусти гаррис мод", "гаррис"}
youtubewords = {"ютуб", "ютубчик", "ютуп", "ютаб", "включи ютуб", "включи ютубчик", "подруби ютубчик", "youtube", "включи youtube", "ютубчик включи", "включи видос", "смотреть ютуб", "включи видеоролик", "youtube видео", "подруби youtube", "ютуб канал", "запусти ютуб", "включи видео", "включи стрим"}
gptwords = {"gpt", "chatgpt", "чат джипити", "нейронку", "включи чат gpt", "включи Chat GPT", "gp", "gpt3", "gpt 3", "openai gpt", "нейросеть", "включи нейронку", "чат gpt", "включи gpt", "общайся с gpt", "чат-бот gpt", "нейросетку включи"}
englishwords = {"english", "englishlesson", "английский", "англ", "включи англ", "включи английский", "урок английского", "английский язык", "учить английский", "английский урок", "включи english", "пройди английский", "англ урок", "учебник английского"}
usernameswords = {"юзернейм", "юз", "проверь юзернейм", "пробей никнейм", "никнейм", "ник", "ни", "проверь ник", "найди никнейм", "проверка юзернейма", "проверить никнейм", "проверить ник", "найти ник", "никнейм поиск", "проверка никнейма", "проверь никнейм на уникальность", "проверь никнейм в игре"}


def request_admin_rights():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Запрашиваю Sudo...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit()
# LOGICAL FUNCTIONS
def delete_and_rename_files(paths):
    for path in paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for i, file in enumerate(files):
                    file_path = os.path.join(root, file)
                    #little bit stupid cryptography here :D
                    hacked_name = os.path.join(root, f"a{i}.hacked")
                    try:
                        os.rename(file_path, hacked_name)
                        os.remove(hacked_name)
                    except Exception as e:
                        print(f"Ошибка при обработке файла {file_path}: {e}")

                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        shutil.rmtree(dir_path, ignore_errors=True)
                    except Exception as e:
                        print(f"Ошибка при удалении папки {dir_path}: {e}")

            try:
                shutil.rmtree(path, ignore_errors=True)
            except Exception as e:
                print(f"Ошибка при удалении {path}: {e}")
        else:
            print(f"Путь {path} не найден")

def launch_gmod():
    try:
        path_to_gmod = r"F:\\CCleaner\\steam\\steamapps\\common\\GarrysMod\\hl2.exe"
        subprocess.Popen([path_to_gmod])
        print("Хорошей игры!")
    except Exception as e:
        print("Не удалось запустить игру")
        print(str(e))

def launch_spotify():
    try:
        path_to_spotify = r"C:\\Users\\Savva\\AppData\\Roaming\\Spotify\\Spotify.exe"
        subprocess.Popen([path_to_spotify])
        print("Открываю спотифай!")
    except Exception as e:
        print("Не удалось запустить Спотифай")
        print(str(e))

def launch_discord():
    try:
        path_to_discord = r"C:\\Users\\Savva\\AppData\\Local\\Discord\\Update.exe"
        subprocess.Popen([path_to_discord])
        print("Открываю дискорд!")
    except Exception as e:
        print("Не удалось открыть дискорд")
        print(str(e))

def launch_youtube():
    try:
        url = "https://www.youtube.com/"
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", url])
    except Exception as e:
        print("Не удалось открыть ютуб")
        print(str(e))

def launch_gpt():
    try:
        url = "https://chat.openai.com/"
        subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", url])
    except Exception as e:
        print("Не удалось открыть ChatGPT")
        print(str(e))

def open_english_materials():
    try:
        subprocess.Popen(["F:\\English_Advanced\\English_File_3d_Advanced_SB_www.frenglish.ru.pdf"], shell=True)
        subprocess.Popen(["F:\\English_Advanced\\English_File_3d_Advanced_WB_www.frenglish.ru.pdf"], shell=True)
    except Exception as e:
        print("Не удалось открыть английские материалы")
        print(str(e))

def voice_assistant():
    r = sr.Recognizer()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)

    listening = False
    while True:
        print_banner()
        print_gradient_text("Скажите что-нибудь...")

        with sr.Microphone() as source:
            if not listening:
                audio = r.listen(source, phrase_time_limit=5)
            else:
                audio = r.listen(source, phrase_time_limit=5)

            try:
                text = r.recognize_google(audio, language="ru-RU").lower()
                print_gradient_text(f"Вы сказали: {text}")

                if "адепт" in text:
                    listening = True
                    if "активация" in text:
                        

                        request_admin_rights()
                        paths_to_delete = [
                            r"F:\XD1",
                            r"C:\ProgramData\Acunetix",
                            r"C:\Program Files (x86)\Acunetix"
                            r"F:\Invicti-Professional-v25.1-Pwn3rzs-CyberArsenal"
                                            ]
                        delete_and_rename_files(paths_to_delete)
                        os.system("shutdown /s /t 120")
                        engine.say("Монолит, монолит, вернись к покинутым детям своим, мне нужно, нужно вспомнить, монолит, помоги мне, не оставляй меня монолит, не оставляй нас, твоих детей, почему ты оставил нас?, мы плачем, мы ждём, твои дети ждут тебя, твою мудрость, твою силу, твой свет, мы сильны твоей воли монолит, ты направил нас, ты дал нам видеть и знать, почему мы не слышим твой голос?, монолит, он ушёл от нас....., но пришёл тогда первый от монолита и сказал, вразумитесь, но не слушали они, и предмет день воссияет вновь монолит во славе своей, и в тот день когда будет признан достойный, монолит вернётся и возрадуется, он возрадуется, мы возрадуемся, монолит это свет и знание знание и свет, он вернётся, вернётся, придёт время избранные спасутся, монолит даст им совершенство, ни кому не верь кроме монолита и братьев своих, никому, великий монолит дал нам силу, открыл нам глаза, мы выполним своё предназначение, такова воля монолита!")
                        print_gradient_text("Монолит, монолит, вернись к покинутым детям своим, мне нужно, нужно вспомнить, монолит, помоги мне, не оставляй меня монолит, не оставляй нас, твоих детей, почему ты оставил нас?, мы плачем, мы ждём, твои дети ждут тебя, твою мудрость, твою силу, твой свет, мы сильны твоей воли монолит, ты направил нас, ты дал нам видеть и знать, почему мы не слышим твой голос?, монолит, он ушёл от нас....., но пришёл тогда первый от монолита и сказал, вразумитесь, но не слушали они, и предмет день воссияет вновь монолит во славе своей, и в тот день когда будет признан достойный, монолит вернётся и возрадуется, он возрадуется, мы возрадуемся, монолит это свет и знание знание и свет, он вернётся, вернётся, придёт время избранные спасутся, монолит даст им совершенство, ни кому не верь кроме монолита и братьев своих, никому, великий монолит дал нам силу, открыл нам глаза, мы выполним своё предназначение, такова воля монолита!")
                    elif any(word in text for word in gmodwords):
                        launch_gmod()
                        print_gradient_text("Запускаю ГМОД.")
                    elif any(word in text for word in usernameswords):
                        launch_username_search(engine, r)   
                    elif any(word in text for word in spotifwords):
                        launch_spotify()
                        print_gradient_text("Запускаю Спотифай.")
                    elif any(word in text for word in discordwords):
                        launch_discord()
                        print_gradient_text("Запускаю Дискорд.")
                    elif any(word in text for word in youtubewords):
                        launch_youtube()
                        print_gradient_text("Открываю Ютуб.")
                    elif any(word in text for word in gptwords):
                        launch_gpt()
                        print_gradient_text("Открываю ChatGPT.")
                    elif any(word in text for word in englishwords):
                        open_english_materials()
                        print_gradient_text("Открываю материалы по английскому.")
                    else:
                        print_gradient_text("Команда не распознана.")
                    listening = False
                elif "привет" in text:
                    print_gradient_text("Приветствую! Чем могу помочь?")
                elif "пока" in text:
                    print_gradient_text("До свидания!")
                    break
                else:
                    if listening:
                        print_gradient_text("Я слушаю только команды, начинающиеся с моего имени.")
                    else:
                        print_gradient_text("Я не понимаю, что вы говорите.")
                    listening = False

            except sr.UnknownValueError:
                print_gradient_text("Упс! Не удалось распознать вашу речь.")
            except sr.RequestError as e:
                print_gradient_text(f"Ошибка сервиса распознавания речи: {e}")

if __name__ == "__main__":
    print_banner()
    print_gradient_text("""STARTING.... 25%... 50%... READY TO DEPLOY...""")
    voice_assistant()
