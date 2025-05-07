# what is ApiRunning ?
ApiRunning or MenjalanakanApi is a programming code to run API from various llm, can even run llm offline ollama. 

# how to run it ?

clone this git in linux (termux):
- # linux ubuntu:
```
apt-get update -y && apt-get upgrade -y
apt-get install git python
git clone https://github.com/Elang-elang/ApiRunning.git
cd ApiRunning
bash Run.sh
```
- # termux:
```
pkg update -y && pkg upgrade -y
pkg install git python
git clone https://github.com/Elang-elang/ApiRunning.git
cd ApiRunning
bash Run.sh
```

# how to run in other device ?
for windows just adjust it and for other devices !

# how does it work ? 

- # using txt extension file in Logs folder:

ApiRunning Will put a log/history of prompts and answers from ai to a file with the extension txt in the Logs/ folder which will be created when running 'Run.sh'.

- # use py extension files for data such as api key, model, url, and ai system

It does make it difficult but in order not to repeat login when logout, I created a 'Data.py' file to store user interface data, such as api key, model, url, and system ai. I will create a user login sign in if at least 10 people favorite my github. 

# description:

ApiRunning to help someone who does not know how to run his Api key, and for someone who does not want to feel tired to code long with the database. We do not use any database (admint php, mysql and so on), only use a database created using files with the extension '.txt' and '.py'.
