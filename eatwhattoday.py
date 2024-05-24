import tkinter as tk
import tkinter.filedialog as filedialog
import json
import random
import threading
import time
import secrets

# 读取配置文件中的菜谱
def load_recipes(config_file='config.json'):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config['recipes']
    except Exception as e:
        print(f"Error loading recipes: {e}")
        return []

# 从文件中导入菜谱
def import_recipes():
    global recipes
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        recipes = load_recipes(file_path)
        print(f"导入了{len(recipes)}个菜谱")

# 滚动显示菜谱
def scroll_recipes():
    global stop_scrolling
    stop_scrolling = False
    end_time = time.time() + random.randint(3, 5)
    while time.time() < end_time:
        if stop_scrolling:
            break
        random.shuffle(recipes)  # 打乱列表顺序
        selected_recipe = secrets.choice(recipes)
        print(f"抽取中：{selected_recipe}")  # 输出选定的菜谱
        result_label.config(text=f"去吃：{selected_recipe}", font=("Helvetica", 40, "bold"))
        root.update()
        time.sleep(0.1)
    stop_scrolling = True

# 启动滚动和倒计时线程
def start_scroll_and_countdown():
    scroll_thread = threading.Thread(target=scroll_recipes)
    scroll_thread.start()
    root.after(3000, lock_recipe)

# 锁定最终显示的菜谱
def lock_recipe():
    if stop_scrolling:
        selected_recipe = result_label.cget("text")
        result_label.config(text=selected_recipe, font=("Helvetica", 80, "bold"), fg="red")
        print(f"最终选择：{selected_recipe}")  # 输出选定的菜谱
    else:
        root.after(100, lock_recipe)

# 创建主窗口
root = tk.Tk()
root.title("世纪难题：今天吃什么？")
root.geometry("800x300")
root.configure(bg="white")

# 从配置文件加载菜谱
recipes = load_recipes()

# 创建并放置按钮和标签
choose_button = tk.Button(root, text="点击此处开始抽菜", command=start_scroll_and_countdown, font=("Helvetica", 26, "bold"), bg="white", fg="black")
choose_button.pack(pady=10)

import_button = tk.Button(root, text="导入菜谱", command=import_recipes, font=("Helvetica", 16, "bold"), bg="white", fg="black")
import_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 36), bg="lightblue")
result_label.pack(pady=20)

# 运行主循环
root.mainloop()
