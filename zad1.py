import tkinter as tk
import tarfile as tar
import os
import shutil
from os.path import curdir


# путь относительно текущего скрипта


class UnixConsoleApp:
    def __init__(self, root,defDir):
        self.root = root
        self.root.title("Console")
        self.defDir=defDir
        self.curDir=self.defDir


        # Приветственное сообщение
        self.defPromt=f"user:~#"
        self.prompt = self.defPromt

        # Стилизация окна как Unix-консоли
        self.text_area = tk.Text(root, bg="black", fg="white", insertbackground="green",
                                 wrap=tk.WORD, width=80, height=24, font=("Courier", 12))
        self.text_area.pack(expand=True, fill='both')

        # Устанавливаем ввод текста доступным
        self.text_area.bind("<Return>", self.process_command)
        self.text_area.bind("<Key>", self.check_input)
        self.text_area.bind("<BackSpace>", self.prevent_backspace)  # Блокируем удаление текста
        self.text_area.config(state=tk.NORMAL)



        self.append_prompt()

        # Устанавливаем фокус на текстовое поле для ввода
        self.text_area.focus_set()


    def append_prompt(self):
        """Добавляем приглашение командной строки"""
        self.text_area.insert(tk.END, self.prompt)
        self.text_area.mark_set(tk.INSERT, tk.END)  # Перемещаем курсор в конец
        self.text_area.see(tk.END)  # Автопрокрутка вниз


    def prevent_backspace(self, event):
        """Блокируем удаление предыдущего текста"""
        if self.text_area.index(tk.INSERT).split('.')[1] == str(
                len(self.prompt)):  # Проверяем, что не удаляется приглашение
            return "break"

    def getDir(self, file):
        cur = self.curDir.split()
        de = self.defDir.split()

        if os.path.exists(f"{self.curDir}/{file}"):
            return f"{self.curDir}/{file}"
        if os.path.exists(f"{self.defDir}/{file}"):
            return f"{self.defDir}/{file}"
        return None

    def process_command(self, event=None):
        """Обработка команды после нажатия Enter"""
        # Получаем текущую строку с командой
        command_line = self.text_area.get(f"{self.text_area.index(tk.INSERT).split('.')[0]}.{len(self.prompt)}",
                                          tk.END).strip()



        # Выполняем команду
        if command_line.split()[0] == "exit":
            self.root.quit()
        elif command_line.split()[0] == "ls":
            res=""
            d = self.curDir if len(command_line.split()) == 1 else (self.getDir(command_line.split()[1]))

            try:
                if (d):
                    for item in os.listdir(d):
                        res += item + " "
                # Добавляем каждый элемент в tar архив
            except Exception as _ex:
                print(_ex)
                if not(d):
                    res="No such directory/file"
                else:
                    res=self.curDir.split("/")[-1] if len(command_line.split())==1 else command_line.split()[1].split("/")[-1]
            self.text_area.insert(tk.END, f"\n{res}\n")

        elif command_line.split()[0] == "cd":
            if len(command_line.split())==1:
                self.curDir=self.defDir
                self.prompt = f"user:~#"
                self.text_area.insert(tk.END, f"\n")

            else:

                d=self.getDir( command_line.split()[1])

                if not(d ) or not(os.path.isdir(d)):

                    self.text_area.insert(tk.END, f"\nNo such directory\n")


                else:
                    self.curDir=d

                    self.prompt=f"user:{self.curDir[self.curDir.find('/',self.curDir.find('/')+1) + 1:]}#"
                    self.text_area.insert(tk.END, f"\n")

        elif command_line.split()[0] == "mv":
            if (len(command_line.split()) > 2):
                d = self.getDir(command_line.split()[-1])
                if not (d):



                    p = self.getDir(command_line.split()[1])

                    os.rename(p, p[:p.rfind("/")] + "/" + command_line.split()[-1])
                elif (os.path.isdir(d)):

                    for file in command_line.split()[1:-1]:

                        p = self.getDir(file)

                        if os.path.exists(p) and not os.path.exists(f"{d}/{file}"):
                            shutil.move(p, d)
                else:

                    p = self.getDir(command_line.split()[1])

                    if os.path.exists(p) and not os.path.exists(f"{self.defDir}/{command_line.split()[1]}"):
                        shutil.move(p, self.defDir)
            self.text_area.insert(tk.END, f"\n")
        elif command_line.split()[0] == "tac":
            if (len(command_line.split())>1):
                d = f"{self.curDir}/{command_line.split()[1]}"
                if not (os.path.exists(d)):
                    self.text_area.insert(tk.END, f"\nNo such file\n")
                else:
                    if (os.path.isfile(d)):
                        res=""
                        f = open(d)
                        mas = []
                        for line in f:
                            mas.append(line)
                        mas.reverse()
                        for i in mas:

                            self.text_area.insert(tk.END, f"\n{i}")
            else:
                self.text_area.insert(tk.END, f"\n")
        else:
            self.text_area.insert(tk.END, f"\nCommand not found: {command_line}\n")

        # Добавляем новое приглашение
        self.append_prompt()

        # Блокируем дальнейший ввод
        return "break"

    def check_input(self, event):
        """Запрещаем ввод текста до приглашения командной строки"""
        cursor_position = self.text_area.index(tk.INSERT).split('.')
        if cursor_position[1] == "0":
            return "break"

# Создаем главное окно приложени
if __name__ == "__main__":
    root = tk.Tk()
    from pathlib import Path

    script_path = str(Path( __file__ ).absolute())


    if not(os.path.exists("papka")):
        os.mkdir("papka")
    if os.path.exists("Konfig.ini"):
        f=open("Konfig.ini")
    else:
        f=open(script_path[:-12]+"Konfig.ini")
    file=f.readline()

    with tar.open(file, 'r') as t:
        t.extractall("papka/")
        app = UnixConsoleApp(root,f"papka/{t.getnames()[0]}" )
        print(app.defDir)
        t.close()

    # Запускаем главный цикл приложения

    root.mainloop()
    with tar.open(file, 'w') as t:
        for item in os.listdir("papka/"):
            item_path = os.path.join("papka/", item)
            # Добавляем каждый элемент в tar архив
            t.add(item_path, arcname=item)
    shutil.rmtree("papka")






