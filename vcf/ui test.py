import tkinter as tk
import tkinter.ttk
from tkinter import filedialog
from tkinter import messagebox
from collections import deque

def func(i=0):
    message = str(i)
    text_box.insert(tk.END, message + "\n")  # 메시지를 Text 위젯에 추가
    text_box.see(tk.END)
    i += 1
    if i < 100:
        # 1000ms(1초) 후에 func 함수 호출하도록 스케줄링
        win.after(100, func, i)

def toggle_checkboxes(checkbox):
    # 다른 체크 박스의 선택을 해제합니다.
    if checkbox == checkbox1:
        checkbox2.deselect()
    elif checkbox == checkbox2:
        checkbox1.deselect()

def btnChooseClick():
    alt_filename = filedialog.askopenfilename(title = 'choose alt fa file to load', filetypes=(('*.txt','*txt'),('*.fa','*fa'),))
    entry_file_name.delete(0,tk.END)
    entry_file_name.insert(0,alt_filename)

def btnExeClick():
    # checkbox, cb, file 선택했는지 확인
    if CheckVariety_1.get()==0 and CheckVariety_2.get()==0:
        messagebox.showwarning(title="err",message="choose Sequence Skill")
        return
    
    if entry_file_name.get()=='':
        messagebox.showwarning(title="err",message="upload alt file")
        return
    
    if cb_ref.get()=='':
        messagebox.showwarning(title="err",message="choose ref file")
        return
    
    qPos = deque()
    qRef = deque()
    qAlt = deque()
    qVar = deque()

    ref = ""
    alt = ""

    f = open('input/ref.txt','r')
    ref = f.read()
    print('ref: ', ref)
    f.close()

    print()

    f = open(entry_file_name.get(),'r')
    alt = f.read()
    print('alt: ', alt)
    f.close()

    print()

    m = len(alt)
    n = len(ref)
    dp = [[0] * (n + 1) for _ in range(m + 1)]


    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref[j - 1] == alt[i - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])


    lcs = ""
    i, j = m, n
    while i > 0 and j > 0:
        if ref[j - 1] == alt[i - 1]:
            lcs = ref[j - 1] + lcs
            if i > 0 : i -= 1
            if j > 0 : j -= 1
            if i == 0 and j>1:
                print("POS 1~%d, DEL : %s -> _" % (j, ref[:j]))
                text_box.insert(tk.END, "POS 1~%d, DEL : %s -> _" % (j, ref[:j]) + "\n")  # 메시지를 Text 위젯에 추가
                text_box.see(tk.END)
                qPos.append('1~%d' %(j))
                qRef.append(ref[:j])
                qAlt.append('_')
                qVar.append('DEL')
            if j == 0 and i>1:
                print("POS %d, INS : _ -> %s" % (0, alt[:i]))
                text_box.insert(tk.END, "POS %d, INS : _ -> %s" % (0, alt[:i]) + "\n")  # 메시지를 Text 위젯에 추가
                text_box.see(tk.END)
                qPos.append('0')
                qRef.append('_')
                qAlt.append(alt[:i])
                qVar.append('INS')

        elif dp[i - 1][j] > dp[i][j - 1]: # INS
            print("POS %d, INS : _ -> %c" % (j, alt[i-1]))

            text_box.insert(tk.END, "POS %d\tINS : _ -> %c" % (j, alt[i-1]) + "\n")  # 메시지를 Text 위젯에 추가
            text_box.see(tk.END)
            qPos.append(str(j))
            qRef.append('_')
            qAlt.append(alt[i-1])
            qVar.append('INS')

            if i > 0 : i -= 1
        elif dp[i - 1][j] < dp[i][j - 1]: # DEL
            print("POS %d, DEL : %c -> _" % (j, ref[j-1]))

            text_box.insert(tk.END, "POS %d\tDEL : %c -> _" % (j, ref[j-1]) + "\n")  # 메시지를 Text 위젯에 추가
            text_box.see(tk.END)

            qPos.append(str(j))
            qRef.append(ref[j-1])
            qAlt.append('_')
            qVar.append('DEL')

            if j > 0 : j -= 1
        elif dp[i - 1][j] == dp[i][j - 1]: # SNV
            print("POS %d, SNV : %c -> %c" % (j, ref[j-1], alt[i-1]))

            text_box.insert(tk.END, "POS %d\tSNV : %c -> %c" % (j, ref[j-1], alt[i-1]) + "\n")  # 메시지를 Text 위젯에 추가
            text_box.see(tk.END)

            qPos.append(str(j))
            qRef.append(ref[j-1])
            qAlt.append(alt[i-1])
            qVar.append('SNV')

            if i > 0 : i -= 1
            if j > 0 : j -= 1
    text_box2.insert(tk.END, "POS\tREF\tALT\tVAR\n")
    while (qPos):
        text_box2.insert(tk.END, "%s\t%s\t%s\t%s\n" % (qPos.pop(), qRef.pop(), qAlt.pop(), qVar.pop()))  # 메시지를 Text 위젯에 추가
        text_box2.see(tk.END)


    print()

    print()
    print("n=%d" %(dp[m][n]))
    print("LCS:", lcs)

win = tk.Tk()
win.geometry('1300x700+50+50')
win.title("Variant Call")
photo = tk.PhotoImage(file = 'img/Tmax_logo.png')
win.wm_iconphoto(False, photo)
win.configure(bg='white')

command_frame = tk.LabelFrame(win, text="Command", relief="flat", bd=2, width=500)
label_sequence_skill = tk.Label(command_frame, text="Sequence Skill", width=30)

CheckVariety_1=tk.IntVar()
CheckVariety_2=tk.IntVar()
checkbox1 = tk.Checkbutton(command_frame, text="Single-End", variable=CheckVariety_1, width=20, command=lambda: toggle_checkboxes(checkbox1))
checkbox2 = tk.Checkbutton(command_frame, text="Paired-End", variable=CheckVariety_2, width=20, command=lambda: toggle_checkboxes(checkbox2))

label_upload_file = tk.Label(command_frame, text="Upload File", width=30)
entry_file_name = tk.Entry(command_frame, width=45, state='normal')
button_choose = tk.Button(command_frame, text="Choose", width=10, command=btnChooseClick)

values=['ref1']
label_ref_file = tk.Label(command_frame, text="Reference File", width=30)
cb_ref = tkinter.ttk.Combobox(command_frame, width=45, values=values)
button_exe = tk.Button(command_frame, text="실행", width=15, command=btnExeClick)

label_sequence_skill.grid(row=0, column=0)
checkbox1.grid(row=0, column=1)
checkbox1.select()
checkbox2.grid(row=0, column=2)

label_upload_file.grid(row=1, column=0)
entry_file_name.grid(row=1, column=1)
button_choose.grid(row=1, column=2)

label_ref_file.grid(row=2, column=0)
cb_ref.grid(row=2, column=1)
button_exe.grid(row=3, column=4)

command_frame.place(x=30, y=30)


console_frame = tk.LabelFrame(win, text="Console", relief="flat", bd=2, width=400)
text_box = tk.Text(console_frame, height=30, width=50)
text_box.pack()
console_frame.place(x=900, y=30)

table_frame = tk.LabelFrame(win, text="Table", relief="flat", bd=2, width=800)
text_box2 = tk.Text(table_frame, height=30, width=100)
text_box2.pack()
table_frame.place(x=30, y=200)

#func()

win.mainloop()