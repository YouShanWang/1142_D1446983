from tkinter import *
import random
import time

# 遊戲控制變數
current_round = 0       # 目前回合
total_rounds = 0        # 玩家設定回合
score = 0               # 玩家分數
time_left = 0           # 每題倒數
running = False         # 避免重複計時

difficulty = "Normal"
start_time = 0
total_chars = 0

word_bank = {
    "Normal":[
        "apple",
        "banana",
        "keyboard"
    ],
    "Hard":[
        "binary search",
        "linked list",
        "cloud storage"
    ],
    "Nightmare":[
        "Practice makes perfect.",
        "Accuracy is more important than speed."
    ]
}

def set_difficulty(level):
    global difficulty
    difficulty = level
    lb5.config(text=f"Difficulty: {level}", fg="purple")

# 開始遊戲
def start_game():
    global total_rounds, current_round, score, running, start_time, total_chars
    # 抓回合數
    try:
        total_rounds = int(entry1.get())
    except:
        lb5.config(text="請輸入有效的回合數", fg="red")
        return
    # 重置遊戲
    current_round = 0
    score = 0
    running = True
    total_chars = 0
    start_time = time.time()
    
    lb5.config(text="")        # 清除提示
    entry2.delete(0, END)      # 清除輸入框
    next_round()

# 進入下一回合    
def next_round():
    global current_round, running, time_left
    if current_round >= total_rounds:     # 遊戲結束
        end_game()
        return
    # 更新回合
    current_round += 1
    # 抽新題目
    new_word = random.choice(word_bank[difficulty])
    lb3.config(text=new_word)
    
    if difficulty == "Nightmare":
        time_left = 15
    else:
        time_left = 10
        
    update_time()
    
    # 清空輸入框
    entry2.delete(0, END)
    entry2.config(state=NORMAL)
    entry2.focus()
    lb5.config(text=f"第 {current_round}/{total_rounds} 回合", fg="black")

# 倒數計時
def update_time():
    global time_left, running
    if not running:
        return
    lb4.config(text=f"Time: {time_left:.1f}")
    if time_left <= 0:
        # 時間到 → 自動判斷錯誤 & 換下一題
        entry2.config(state=DISABLED)
        check_answer(timeout=True)
        return
    time_left -= 0.1
    root.after(100, update_time)   # 每 0.1 秒更新一次

# 判斷玩家輸入正確或錯誤
def check_answer(timeout=False):
    global score, total_chars
    correct_word = lb3.cget("text")
    user_input = entry2.get()
    if timeout:
        lb5.config(text=f"時間到！正確答案是：{correct_word}", fg="red")
    else:
        if user_input == correct_word:
            score += 1
            total_chars += 1
            lb5.config(text="Correct!", fg="green")
        else:
            lb5.config(text=f"Wrong! 正解：{correct_word}", fg="red")
    # 延遲 1 秒後進入下一題
    root.after(1000, next_round)

# 玩家按下 Enter → 檢查答案
def on_enter(event):
    check_answer()

# 遊戲結束
def end_game():
    global running
    running = False
    percent = int((score / total_rounds) * 100)
    elapsed = time.time() - start_time
    minutes = elapsed / 60
    if minutes > 0:
        wpm = int((total_chars / 5) / minutes)
    else:
        wpm = 0
    lb3.config(text="GAME OVER", bg="#ffaaaa")
    lb5.config(
        text=f"Final Score: {score}/{total_rounds} ({percent}%) | WPM: {wpm}",
        fg="blue"
    )
    entry2.config(state=DISABLED)



# UI 介面
if __name__ == "__main__":
    root = Tk()
    root.title("Speed Typing Challenge")
    root.geometry("600x500+100+50")
    
    lb1 = Label(root, font=("Arial", 20, "bold"),
                text="Speed Typing Challenge", justify=CENTER)
    lb1.pack(pady=20)
    
    round_frame = Frame(root)
    round_frame.pack(pady=20)
    
    lb2 = Label(round_frame, font=("Arial", 14, "bold"),
                text="Round: ", justify=CENTER)
    lb2.pack(side="left")
    
    entry1 = Entry(round_frame, font=("Times New Roman", 14, "bold"), 
                   width=5, bg="#3072b5",fg="white", justify=CENTER)
    entry1.pack(side="left")
    
    difficulty_frame = Frame(root)
    difficulty_frame.pack(pady=5)

    btn_Normal = Button(difficulty_frame, text="Normal", command=lambda:set_difficulty("Normal")).pack(side="left", padx=5)
    btn_Hard = Button(difficulty_frame, text="Hard", command=lambda:set_difficulty("Hard")).pack(side="left", padx=5)
    btn_Nightmare = Button(difficulty_frame, text="Nightmare", command=lambda:set_difficulty("Nightmare")).pack(side="left", padx=5)
    
    btn1 = Button(root, font=("Arial", 14, "bold"), 
                  text="Start Game", command=start_game)
    btn1.pack(pady=20)
    
    lb3 = Label(root, font=("Arial", 26, "bold"), 
                text="",width=15,height=2, bg="#ffccaa", justify=CENTER)
    lb3.pack(pady=10)
    
    lb4 = Label(root, font=("Arial", 14, "bold"), 
                text="Time: ", justify=CENTER)
    lb4.pack(pady=10)
    
    entry2 = Entry(root, font=("Arial", 20, "bold"), 
                   width=10, bg="#3072b5", fg="white", justify=CENTER)
    entry2.pack()
    
    lb5 = Label(root, font=("Arial", 8, "bold"),
                text="", justify=CENTER)
    lb5.pack()
    
    entry2.bind("<Return>", on_enter)
    
    root.mainloop()