def saveLog(
    logPrompt: str,
    logAnswer: str
):
    save=f"""
{"="*50}
Log:
{"="*50}
• Prompt: 
{"="*50}
{logPrompt}
{"="*50}
• Answer: 

{logAnswer}

"""
    return save

def line():
    hasil=""
    while True:
        prompt = input("... ")
        if prompt == '\"\"\"':
            return hasil
        hasil=f"{hasil}\n{prompt}"

def Check(prompt, Models, Api, Type, System, Url=""):
    from Class import chatAI
    if not Url:
        Type="ollama"
    if Type=="ollama":
        try:
            hasil=chatAI.OllamaChat(Models, prompt, System)
            return hasil
        except Exception as e:
            print(f"Error: {str(e)}")
    elif Type=="requests":
        try:
            hasil = chatAI.HttpChat(Api, Models, Url, prompt, System)
            return hasil
        except Exception as e:
            print(f"Error: {str(e)}")
    elif Type=="openai":
        try:
            client=chatAI.openaiClient(Url, Api)
            chatAI.openaiChat(client, Models, prompt, System)
            return hasil
        except Exception as e:
            print(f"Error: {str(e)}")

def System_AI():
    print()
    print("     Enter system for your AI")
    print()
    while True:
        prompt = input(">>> ")
        if not prompt:
            continue
        elif prompt == '\"\"\"':
            prompt=line()
            return prompt
        if prompt.startswith("./"):
            prompt=prompt.replace("./", "")
            with open(prompt, 'r') as f:
                isi = f.read()
            return isi

def helpme():
    print()
    print("    /new            : reset API, model, and URL")
    print()
    print("    /sys            : set AI system. Start with './' to use a .txt file")
    print()
    print("    /load </file>   : load your log file")
    print()
    print("    /install </pkg> : install required libraries")
    print()
    print("    Required Libs    : requests, openai, ollama")
    print()
    print("    Ctrl + D        : exit")
    print()
    print("    \"\"\"             : multi-line prompt")
    print()

def RunInd(System="", Api=""):
    import os
    os.system("clear")
    try:
        if Api=="ollama":
            from Data import Models, Type
            try:
                from Data import System
            except ImportError:
                System=""
            Api=""
            Url=""
        else:
            from Data import Api, Models, Url, Type
            try:
                from Data import System 
            except ImportError:
                System=""
    except (FileNotFoundError, ImportError):
        with open('Data.py', 'w') as f:
            print()
            print()
            print("   requests : online AI using requests library")
            print()
            print("   openai   : online AI using openai library")
            print()
            print("   ollama   : offline AI using ollama library")
            print()
            while True:
                Type=input("[Type]>>> ")
                if Type.lower() not in ('requests', 'openai', 'ollama'):
                    continue
                elif Type.lower() == "ollama":
                    print("     Ollama setup")
                    models = input("[Models]>>> ")
                    print("     Is the model installed?")
                    kondisi = input("[Y/N]>>> ").lower()
                    if kondisi=="n":
                        import ollama 
                        try:
                            ollama.pull(models)
                        except Exception as e:
                            print(f"Error: {str(e)}")
                    print("     Model installed")
                    f.write(f"Models='{models}'\nType='ollama'")
                    break
                    pass
                api = input("[Api]>>> ")
                models = input("[Models]>>> ")
                url = input("[Url]>>> ")
                f.write(f"Api='{api}'\nModels='{models}'\nUrl='{url}'\nType='{Type.lower()}'")
                break
        try:
            if Type.lower()=="ollama":
                from Data import Models, Type
                Api=""
                Url=""
                try:
                    from Data import System as SyS 
                    System = SyS
                except ImportError:
                    System=""
            else:
                from Data import Api, Models, Url, Type
                try:
                    from Data import System as SyS 
                    System = SyS
                except ImportError:
                    System=""
        except Exception:
            import os
            os.system("python IndR.py")
    print()
    print("     /? or /help : help")
    print()
    save=""
    sendLog=""
    while True:
        try:
            prompt = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            print()
            print("     /see   : view logs")
            print()
            print("     Do you not want to save your logs? [y/n] ")
            print()
            while True:
                try:
                    prompt=input(">>> ")
                    if prompt.startswith("/"):
                        prompt=prompt.replace("/", "")
                        if prompt == "see":
                            print("\n\"\"\""+sendLog+"\"\"\"\n")
                        else:
                            print("\n     Invalid system function\n")
                    elif prompt.lower() == "y":
                        print("\n     Enter log name (end with .txt)\n")
                        prompt=input("[Name]>>> ")
                        if not prompt.endswith(".txt"):
                            prompt=prompt+".txt"
                        print()
                        print(f"     Saved to: './logs/{prompt}'")
                        print()
                        print("     Use '/load <FileName>' to load logs")
                        print()
                        break
                    elif prompt.lower() == "n":
                        import os
                        os.system("clear")
                        print()
                        chatAI.ident()
                        print()
                        exit()
                    else:
                        continue
                    try:
                        with open(f"Logs/{prompt}", "a") as f:
                            f.write(save)
                    except FileNotFoundError:
                        with open(f"Logs/{prompt}", "w") as f:
                            f.write(save)
                except (KeyboardInterrupt, EOFError):
                    import os
                    os.system("clear")
                    print()
                    chatAI.ident()
                    print()
                    exit()
            import os
            os.system("clear")
            print()
            chatAI.ident()
            print()
            exit()
        if not prompt:
            continue
        if prompt.startswith("/"):
            prompt=prompt.replace("/", "")
            if prompt.lower() in ("h", "help", "?"):
                helpme()
            elif prompt.lower().startswith("load"):
                prompt=prompt.split(" ")
                if not prompt[1].endswith(".txt"):
                    print()
                    print("     Invalid file: must be .txt")
                    print()
                else:
                    try:
                        with open(f"Logs/{prompt[1]}", "r") as f:
                            isi=f.read()
                            System=System+isi
                    except FileNotFoundError:
                        print()
                        print("     Log directory './logs' not found")
                        print()
            elif prompt.lower() == "sys":
                with open('Data.py', 'a') as file:
                    SYS=System_AI()
                    file.write(f"\nSystem='''{SYS}'''")
                    break
                RunInd(System=SYS, Api=Api)
            elif prompt.lower()=="new":
                with open('Data.py', 'w') as file:
                    file.write("")
                print()
                print("     Restart this file")
                print()
                break
                exit()
            elif prompt.lower().startswith("install"):
                prompt=prompt.split(" ")
                if prompt[1].lower() not in ('requests', 'openai', 'ollama'):
                    continue
                else:
                    import os
                    try:
                       os.system(f"pip install {prompt[1].lower()}")
                    except Exception as e:
                        print(f"Install error: {str(e)}")
            else:
                print()
                print("     Unknown system function")
                print()
            prompt=""
        elif prompt == "\"\"\"":
            prompt=line()
            jawaban=Check(prompt, Models, Api, Type, System, Url)
            print()
            print(jawaban)
            print()
            save=f"\n{saveLog(prompt, jawaban)}\n"
            sendLog=sendLog+save
        else:
            jawaban=Check(prompt, Models, Api, Type, System, Url)
            print()
            print(jawaban)
            print()
            save=f"\n{saveLog(prompt, jawaban)}\n"
            sendLog=sendLog+save
        System=System+sendLog
while True:
    print()
    print("     /? or /help : help")
    print()
    RunInd()
