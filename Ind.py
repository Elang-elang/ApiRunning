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
• Jawaban: 

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
            print(f"Error karena: {str(e)}")
    elif Type=="requests":
        try:
            hasil = chatAI.HttpChat(Api, Models, Url, prompt, System)
            return hasil
        except Exception as e:
            print(f"Error karena: {str(e)}")
    elif Type=="openai":
        try:
            client=chatAI.openaiClient(Url, Api)
            chatAI.openaiChat(client, Models, prompt, System)
            return hasil
        except Exception as e:
            print(f"Error karena: {str(e)}")

def System_AI():
    print()
    print("     Masukan system untuk ai anda")
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
        return prompt

def helpme():
    print()
    print("    /new            : untuk memasukan ulang api, model, dan url")
    print()
    print("    /sys            : untuk menyetel system ai. Berawalan './' untuk menyetel system ai lewat file.txt")
    print()
    print("    /load </file>   : untuk memuat file logs anda")
    print()
    print("    /install </pkg> : untuk menginstall library yang dibutuhkan untuk menjalankan ai")
    print()
    print("    Nama Lib/Pkg    : requests, openai, dan ollama")
    print()
    print("    Ctrl + D        : untuk keluar")
    print()
    print("    \"\"\"             : untuk prompt line")
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
            print("   requests : requests, ai dijalankan secara online dan menggunakan library requests")
            print()
            print("   openai   : openai, ai dijalankan secara online dan menggunakan library openai")
            print()
            print("   ollama   : ollama, ai dijalankan secara offline dan menggunakan library ollama")
            print()
            while True:
                Type=input("[Type]>>> ")
                if Type.lower() not in ('requests', 'openai', 'ollama'):
                    continue
                elif Type.lower() == "ollama":
                    print("     Masuk dibagian Ollama")
                    models = input("[Models]>>> ")
                    print("     Apakah model telah terinstall ?")
                    kondisi = input("[Y/N]>>> ").lower()
                    if kondisi=="n":
                        import ollama 
                        try:
                            ollama.pull(models)
                        except Exception as e:
                            print(f"Error karena: {str(e)}")
                    print("     Model telah terinstall")
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
    print("     /? atau /help : untuk bantuan")
    print()
    save=""
    sendLog=""
    while True:
        try:
            prompt = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            print()
            print("     /see   : untuk lihat logs")
            print()
            print("     Apakah Tidak Ingin Di Save Logs Anda ? [y/n] ")
            print()
            while True:
                try:
                    prompt=input(">>> ")
                    if prompt.startswith("/"):
                        prompt=prompt.replace("/", "")
                        if prompt == "see":
                            print("\n\"\"\""+sendLog+"\"\"\"\n")
                        else:
                            print("\n     Maaf Fungsi Sistem yang kamu panggil salah atau bukan dari fungsi ini\n")
                    elif prompt.lower() == "y":
                        print("\n     Berikan nama untuk logs anda (berakhiran txt)\n")
                        prompt=input("[Nama]>>> ")
                        if not prompt.endswith(".txt"):
                            prompt=prompt+".txt"
                        print()
                        print(f"     Saya telah menyimpan file: '{prompt}' Anda di direktori: './logs/'. Lebih tepatnya: './logs/{prompt}'")
                        print()
                        print("     Untuk membuka log agar termuat maka gunakan Fungsi Sistem '/load <Nama_File>' untuk memuatkannya ")
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
                    print("     Maaf File harus berakhiran .txt, file tidak valid")
                    print()
                else:
                    try:
                        with open(f"Logs/{prompt[1]}", "r") as f:
                            isi=f.read()
                            System=System+isi
                    except FileNotFoundError:
                        print()
                        print("     Maaf File tidak ada direktori './log', buat saja dulu logNya")
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
                print("     Jalankan Ulang Lagi File ini")
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
                        print(f"Penginstallan Error karena: {str(e)}")
            else:
                print()
                print("     Fungsi Sistem Tidak Dikenali : Anomali")
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
    print("     /? atau /help : untuk bantuan")
    print()
    RunInd()
