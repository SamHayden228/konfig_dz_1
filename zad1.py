import tkinter as tk
import tarfile as tar
import os
import shutil
from os.path import curdir



class UnixConsoleApp:
    def __init__(self, defDir):
        self.defDir=defDir
        self.curDir=self.defDir
        # Стилизация окна как Unix-консоли

        # Приветственное сообщение
        self.defPromt=f"user:~#"
        self.prompt = self.defPromt



    def getDir(self, file):
        cur=self.curDir.split()
        de=self.defDir.split()

        if os.path.exists(f"{self.curDir}/{file}"):
            return f"{self.curDir}/{file}"
        if os.path.exists(f"{self.defDir}/{file}"):
            return f"{self.defDir}/{file}"
        return None
    def process_command(self, command_line):
        """Обработка команды после нажатия Enter"""
        # Получаем текущую строку с командой



        # Выполняем команду

        if command_line.split()[0] == "ls":
            res=""
            d=self.curDir if len(command_line.split())==1 else( f"{self.curDir}/{command_line.split()[1]}")

            try:
                for item in os.listdir(self.curDir if len(command_line.split())==1 else( f"{self.curDir}/{command_line.split()[1]}")):
                    res+=item+" "
                # Добавляем каждый элемент в tar архив
            except Exception as _ex:

                if not(os.path.exists(d)):
                    res="No such directory/file"
                else:
                    res=self.curDir.split("/")[-1] if len(command_line.split())==1 else command_line.split()[1].split("/")[-1]
            print( f"{res}")

        elif command_line.split()[0] == "cd":
            if len(command_line.split())==1:
                self.curDir=self.defDir
                self.prompt = f"user:~#"

            else:

                d=self.getDir( command_line.split()[1])

                if not(d ) or not(os.path.isdir(d)):
                    print( f"No such directory")


                else:
                    self.curDir=d

                    self.prompt=f"user:{self.curDir[self.curDir.find('/',self.curDir.find('/')+1) + 1:]}#"

        elif command_line.split()[0] == "mv":
            if (len(command_line.split())>2):
                d=self.getDir(command_line.split()[-1])
                if not (d):

                    print(os.path.exists(command_line.split()[-1]))

                    p = self.getDir(command_line.split()[1])
                    print(p[:p.rfind("/")]+"/"+command_line.split()[-1])
                    os.rename(p,p[:p.rfind("/")]+"/"+command_line.split()[-1])
                elif (os.path.isdir(d)):

                    for file in command_line.split()[1:-1]:

                        p=self.getDir(file)


                        if os.path.exists(p) and not os.path.exists(f"{d}/{file}"):
                            shutil.move(p,d)
                else:


                    p=self.getDir(command_line.split()[1])


                    if os.path.exists(p) and not os.path.exists(f"{self.defDir}/{command_line.split()[1]}"):
                        shutil.move(p,self.defDir)

        elif command_line.split()[0] == "tac":
            if (len(command_line.split())>1):
                d = self.getDir(command_line.split()[1])
                if not (os.path.exists(d)):
                    print( f"No such directive")
                else:
                    if (os.path.isfile(d)):
                        res=""
                        f = open(d)
                        mas = []
                        for line in f:
                            mas.append(line)
                        mas.reverse()
                        for i in mas:

                            print( i.replace("\n",""))

        else:
            print( f"Command not found: {command_line}")

        # Добавляем новое приглашение


        # Блокируем дальнейший ввод
        return "break"



# Создаем главное окно приложения


if not(os.path.exists("papka")):
    os.mkdir("papka")
if os.path.exists("Konfig.ini"):
    f=open("Konfig.ini")
else:
    f=open("C:/Users/vlaso_n8/PycharmProjects/pythonProject/Konfig.ini")
file=f.readline()

with tar.open(file, 'r') as t:
    t.extractall("papka/")
    app = UnixConsoleApp(f"papka/{t.getnames()[0]}" )
    t.close()

# Запускаем главный цикл приложения
while (True):
    print(app.prompt, end=" ")
    inp = input()
    if inp.split()[0] == "exit":
        break
    app.process_command(inp)
with tar.open(file, 'w') as t:
    for item in os.listdir("papka/"):
        item_path = os.path.join("papka/", item)
        # Добавляем каждый элемент в tar архив
        t.add(item_path, arcname=item)
shutil.rmtree("papka")

