"""
Ind.py - A script untuk berinteraksi dengan berbagai model AI.
"""

import os
import importlib.util
import sys
from Class import chatAI  # Import utama di atas untuk menghindari import berulang
chatAI.ident()
# ------------------------- Fungsi Bantuan -------------------------
def save_log(log_prompt: str, log_answer: str) -> str:
    """Membuat format log yang rapi."""
    return f"""
{"="*50}
Log:
{"="*50}
• Prompt: 
{"="*50}
{log_prompt}
{"="*50}
• Jawaban: 

{log_answer}

"""

def line_input() -> str:
    """Menerima input multi-line hingga pengguna memasukkan \"\"\"."""
    hasil = []
    while True:
        prompt = input("... ")
        if prompt == '\"\"\"':
            return '\n'.join(hasil)
        hasil.append(prompt)

# ------------------------- Fungsi Utama -------------------------
def check(prompt: str, model: str, api_key: str, ai_type: str, system: str, url: str = "") -> str:
    """Mengirim permintaan ke model AI berdasarkan jenis yang ditentukan."""
    try:
        if ai_type == "ollama":
            return chatAI.OllamaChat(model, prompt, system)
        elif ai_type == "requests":
            return chatAI.HttpChat(api_key, model, url, prompt, system)
        elif ai_type == "openai":
            client = chatAI.openaiClient(url, api_key)
            return chatAI.openaiChat(client, model, prompt, system)
        else:
            raise ValueError(f"Tipe AI tidak valid: {ai_type}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return ""

def item_from(module_name: str, file_path: str) -> str:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    config = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = config
    spec.loader.exec_module(config)
    return config

def setup_system() -> str:
    """Mengambil input system prompt dari pengguna atau file."""
    print("Masukkan system untuk AI Anda (awali dengan './' untuk membaca dari file):")
    while True:
        prompt = input(">>> ").strip()
        if not prompt:
            continue
        if prompt == '"""':
            return line_input()
        if prompt.startswith("./"):
            file_path = prompt[2:]
            try:
                with open(file_path, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                print(f"File {file_path} tidak ditemukan!")
        return prompt

def show_help():
    """Menampilkan menu bantuan."""
    print("\nDaftar Perintah:")
    print("    /new            : Reset API, model, dan URL")
    print("    /sys            : Set system prompt (gunakan './' untuk baca dari file)")
    print("    /load <file>    : Muat log dari file")
    print("    /install <pkg>  : Install package (requests, openai, ollama)")
    print("    /clear          : Untuk menghapus berpesan dengan ai di tampilan")
    print("    Ctrl + D        : Keluar dari program\n")
    print("\n    \"\"\"             : Untuk input multi-line (mengawali/mengakhiri)\n")

# ------------------------- Setup & Konfigurasi -------------------------
def setup_environment():
    """Mempersiapkan environment dengan membuat file Data.py jika belum ada."""
    if not os.path.exists('Data.py'):
        print("\nKonfigurasi awal diperlukan:")
        print("Pilih tipe AI (requests/openai/ollama):")
        
        ai_type = ""
        while ai_type not in ("requests", "openai", "ollama"):
            ai_type = input("[Type]>>> ").lower()
        
        model = input("[Model]>>> ")
        api_key = ""
        url = ""
        
        if ai_type == "ollama":
            print("Pastikan model sudah terinstall!")
            confirm = input("[Y/N]>>> ").lower()
            if confirm == "n":
                try:
                    import ollama
                    ollama.pull(model)
                except Exception as e:
                    print(f"Gagal menginstall model: {str(e)}")
        else:
            api_key = input("[API Key]>>> ")
            url = input("[URL]>>> ")
        
        os.system("touch Data.py")
        with open('Data.py', 'w') as f:
            f.write(f"API = '{api_key}'\n")
            f.write(f"MODEL = '{model}'\n")
            f.write(f"URL = '{url}'\n")
            f.write(f"TYPE = '{ai_type}'\n")
            f.write("SYSTEM = ''\n")

def load_config():
    """Memuat konfigurasi dari Data.py."""
    try:
        from Data import API, MODEL, URL, TYPE
        try:
            from Data import SYSYEM
        except ImportError:
            SYSTEM=""
    except ImportError:
        os.remove("Data.py")
        main_loop()
    return {
        "api": API,
        "model": MODEL,
        "url": URL,
        "type": TYPE,
        "system": SYSTEM
    }

# ------------------------- Loop Utama -------------------------
def main_loop():
    """Loop interaksi utama dengan pengguna."""
    setup_environment()
    config = load_config()
    system_prompt = config["system"]
    log_history = []
    
    os.system('cls' if os.name == 'nt' else 'clear')
    chatAI.ident()
    print("\nSelamat datang! Ketik /help untuk bantuan\n")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if not user_input:
                continue
                
            # Perintah khusus
            if user_input.startswith("/"):
                cmd = user_input[1:]
                cmd_list = cmd.split(" ")
                if cmd.lower() in ("?", "help", "h"):
                    show_help()
                elif cmd.lower() == "clear":
                     os.system('cls' if os.name == 'nt' else 'clear')
                elif cmd.lower() == "new":
                    os.remove("Data.py")
                    print("\nKonfigurasi direset. Silakan restart program.")
                    return
                elif cmd.lower() == "sys":
                    new_system = setup_system()
                    with open('Data.py', 'a') as f:
                        f.write(f"\nSYSTEM = '''{new_system}'''")
                    print("\nSystem prompt diperbarui!")
                elif cmd.lower().startswith("load"):
                    if not cmd_list[1].endswith(".txt"):
                        cmd_list[1]=cmd_list[1]+".txt"
                    with open(cmd_list[1], "r") as f:
                        isi=f.read()
                        log_history.append(isi)
                    print(f"\nBerhasil diload file: {cmd_list[1]}\n")
                elif cmd.lower().startswith("install"):
                    try:
                        os.system(f"pip install  {TYPE}")
                    except Exception as e:
                        print(f"Error karena: {str(e)}")
                else:
                    print("\nPerintah tidak dikenali!\n")
                    
            elif user_input == '"""':
                full_prompt = line_input()
                response = check(full_prompt, config["model"], config["api"], 
                                 config["type"], system_prompt, config["url"])
                print(f"\n{response}\n")
                log_history.append(save_log(full_prompt, response))
            else:
                response = check(user_input, config["model"], config["api"], 
                                config["type"], system_prompt, config["url"])
                print(f"\n{response}\n")
                log_history.append(save_log(user_input, response))
                
        except EOFError:
            print()
            handle_exit(log_history)
        except KeyboardInterrupt:
            handle_exit(log_history)

def handle_exit(logs: list):
    """Menangani proses keluar dan penyimpanan log."""
    print("\nSimpan log? (y/n)\n")
    while True:
        try:
            choice = input(">>> ").lower()
            if choice == "y":
                print("\nNama file (akhiri dengan .txt)\n")
                filename = input(">>> ").strip()
                if not filename.endswith(".txt"):
                    filename += ".txt"
                
                os.makedirs("Logs", exist_ok=True)
                with open(f"Logs/{filename}", "w") as f:
                    new_logs="\n".join(logs)
                    f.write(new_logs)
                print()
                print(f"Log disimpan di: Logs/{filename}")
                print()
                break
            elif choice == "n":
                break
            else:
                continue
        except (EOFError, KeyboardInterrupt):
            os.system('cls' if os.name == 'nt' else 'clear')
            chatAI.ident()
            print("Terimakasih Telah mencoba karya saya")
            print()
        break
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    chatAI.ident()
    print("Terimakasih Telah mencoba karya saya")
    print()
    exit()

if __name__ == "__main__":
    main_loop()
