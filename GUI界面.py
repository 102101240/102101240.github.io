import tkinter as tk
from tkinter import filedialog
import os

difficulties = ["题解","入门","普及−","普及","普及+","提高+","省选","NOI"]

# 创建主窗口
window = tk.Tk()
window.title("洛谷题库爬取")
window.geometry("500x500")

# 创建关键字标签和输入框
keyword_label = tk.Label(window, text="关键字:")
keyword_label.pack()
keyword_entry = tk.Entry(window)
keyword_entry.pack()

# 创建难度值标签和下拉菜单
difficulty_label = tk.Label(window, text="难度:")
difficulty_label.pack()
selected_difficulty = tk.StringVar()
difficulty_menu = tk.OptionMenu(window, selected_difficulty, *difficulties)
difficulty_menu.pack()

# 创建搜索按钮点击事件处理函数
def search_folder():
    folder_path = filedialog.askdirectory()  # 选择文件夹
    if folder_path:
        keyword = keyword_entry.get()  # 获取关键字输入
        difficulty = selected_difficulty.get()
        if difficulty in difficulties:
            file_list.delete(0, tk.END)  # 清空列表框内容

            # 搜索文件夹
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # 处理每个文件
                    file_path = os.path.join(root, file)
                    file_name = os.path.basename(file_path)  # 提取文件名

                    # 使用字符串的startswith()和endswith()方法来匹配难度值
                    if keyword in file_name and file_name.endswith(difficulty+'.md'):
                        file_list.insert(tk.END, file_name)
        else:
            # 处理无效的难度值
            print("无效的难度值")

# 创建搜索按钮
button = tk.Button(window, text="选择文件夹并搜索", command=search_folder)
button.pack()

# 创建结果标签
file_list = tk.Listbox(window)
file_list.pack()

# 进入主循环
window.mainloop()
