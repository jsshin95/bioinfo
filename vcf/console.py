import tkinter as tk
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("실시간 콘솔 메시지")

        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        # 외부 프로세스 실행 및 메시지 표시 함수
        def display_console_output():
            process = subprocess.Popen(["python vcf.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.text_area.insert("end", output.strip() + "\n")
                    self.text_area.see("end")
            process.stdout.close()

        # 쓰레드를 이용하여 외부 프로세스 실행과 동시에 GUI 업데이트
        import threading
        thread = threading.Thread(target=display_console_output)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()