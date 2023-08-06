import shutil
import tkinter
import tempfile
from tkinter import filedialog
from tkinter import messagebox


def app_start():
    app.title("Markdown文件转化程序")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    app_width = 500
    app_height = 350

    x = (screen_width - app_width) / 2
    y = (screen_height - app_height) / 2 - 60

    app.geometry("%dx%d+%d+%d" % (app_width, app_height, x, y))


def app_module():
    # 选择按钮
    file_select_button = tkinter.Button(app, text="选择文件", width=20, height=4, command=select_file)
    file_select_button.pack(side=tkinter.TOP, anchor=tkinter.CENTER)

    # 转化按钮
    file_convert_button = tkinter.Button(app, text="转换文件", width=20, height=4, command=convert_file)
    file_convert_button.pack(side=tkinter.TOP, anchor=tkinter.CENTER)

    file_save_button = tkinter.Button(app, text="保存文件", width=20, height=4, command=save_file)
    file_save_button.pack(side=tkinter.TOP, anchor=tkinter.CENTER)


def select_file():
    file_path = filedialog.askopenfilename(title="选择所需转化的Markdown文件")
    if file_path and (not file_path.endswith(".md")):
        messagebox.showwarning("警告", "请选择Markdown文件")
        return
    else:
        global in_file_path
        in_file_path = file_path


def convert_file():
    if in_file_path:
        global out_file_path
        with open(in_file_path, encoding="UTF-8") as f1, open(out_file_path.name, "w", encoding="UTF-8") as f2:
            # 由于 用 Typora 编写 Markdown 时, 会默认给文本之间增加空行，所以只有三行以上的空行出现时，才增加</br>标签
            # 介于 Typora 只会出现奇数情况的空行，所以这里只需要在偶数时增加</br>标签即可
            wrap_flag = False
            for line in f1:
                if line == "\n":
                    if wrap_flag:
                        line = "</br>" + "\n"
                    wrap_flag = not wrap_flag
                else:
                    wrap_flag = False
                f2.write(line)
        out_file_path.close()
        global is_convert
        is_convert= True
        messagebox.showinfo("提示", "转化完成")
    else:
        messagebox.showwarning("警告", "请先选择Markdown文件")
        return


def save_file():
    if is_convert:
        save_path = filedialog.asksaveasfilename(
            title="保存转化后的Markdown文件",
            initialfile="转化后的" + in_file_path.split("/")[-1],
            defaultextension=".md",
            filetypes=[("Markdown文档", "*.md;*.markdown;*.mmd;*.mdwn;*.mdown"), ("所有文件", "")])
    else:
        messagebox.showwarning("警告", "请先转化Markdown文件")
        return

    if save_path:
        shutil.move(out_file_path.name, save_path)
        messagebox.showinfo("提示", "保存完成")


if __name__ == "__main__":
    in_file_path = ""
    out_file_path = tempfile.NamedTemporaryFile(suffix=".md", delete=False)
    is_convert = False

    app = tkinter.Tk()

    app_start()
    app_module()

    app.mainloop()
