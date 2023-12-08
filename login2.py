import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button
from PIL import ImageTk,Image
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pygame import *



class FaceRecognitionApp:
    def __init__(self):
        self.confirm = False
        self.user_data_path = "data"
        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)

        self.screen = tk.Tk()
        self.screen.geometry("1280x720")
        self.screen.title("anhtruongncc")
    def register_face1(self):
        username = self.register_username_entry.get()
        if os.path.exists(f"data/{username}.jpg"):
            messagebox.showinfo("Đăng ký", "Tên đăng nhập đã tồn tại. Hãy chọn tên đăng nhập khác.")
            return
        user_path = os.path.join(self.user_data_path, username)

        if os.path.exists(user_path):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác.")
            return

        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            cv2.imshow('Press space to capture', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break
        cv2.destroyWindow('Press space to capture')
        capture.release()

        cv2.imwrite(f"data/{username}.jpg", frame)
        messagebox.showinfo("Đăng ký", "Đăng ký thành công.")
        self.screen4.destroy()

    def login_verify1(self):
        username = self.login_username_entry.get()
        if not os.path.exists(f"data/{username}.jpg"):
            messagebox.showinfo("Đăng nhập", "Tên đăng nhập không tồn tại.")
            return

        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            cv2.imshow('Press space to capture', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                break
        cv2.destroyWindow('Press space to capture')
        capture.release()

        known_image = face_recognition.load_image_file(f"data/{username}.jpg")
        unknown_image = frame

        known_face_encodings = face_recognition.face_encodings(known_image)

        if not known_face_encodings:
            messagebox.showinfo("Đăng nhập", "Không tìm thấy khuôn mặt trong ảnh đã đăng ký.")
            return

        known_face_encoding = known_face_encodings[0]

        unknown_face_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_face_encodings:
            messagebox.showinfo("Đăng nhập", "Không tìm thấy khuôn mặt trong ảnh vừa chụp.")
            return

        unknown_face_encoding = unknown_face_encodings[0]

        results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)

        if results[0]:
            messagebox.showinfo("Đăng nhập", "Đăng nhập thành công.")
            self.confirm = True
            self.screen.destroy()
        else:
            messagebox.showinfo("Đăng nhập", "Xác thực không thành công.")
            self.screen3.destroy()

    def register_face(self):
        self.screen4 = Toplevel(self.screen3)
        self.screen4.geometry("720x360")
        tk.Label(self.screen4, text="Tên đăng nhập:").place(x=270,y=160)
        self.register_username_entry = Entry(self.screen4)
        self.register_username_entry.place(x=270,y=180)
        Button(self.screen4, text="Đăng ký", command=self.register_face1).place(x=270,y=215)

    def window_log_face(self):
        self.screen3 = Toplevel(self.screen)
        self.screen3.geometry("640x360")
        tk.Label(self.screen3, text="Tên đăng nhập:").place(x=270, y=180)
        self.login_username_entry = Entry(self.screen3)
        self.login_username_entry.place(x=270, y=210)
        username = self.login_username_entry
        log1 = Button(self.screen3, text="Đăng nhập", command=self.login_verify1)
        log1.place(x=270, y=235)
        reg1 = Button(self.screen3, text="Đăng ký", command=self.register_face)
        reg1.place(x=270, y=265)

    def send_registration_email(self, username, email):
        sender_email = "us88.betting.game@gmail.com"
        sender_password = "qrffziarailtcisr"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Đăng ký thành công"

        body = f"Chào mừng bạn, {username}! Bạn đã đăng ký thành công."
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())

    def login_verify(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        user_path = os.path.join(self.user_data_path, username)
        if username not in os.listdir(self.user_data_path) or not os.path.isfile(
                os.path.join(user_path, "password.txt")):
            messagebox.showerror("Lỗi", "Tên đăng nhập không tồn tại. Đăng nhập thất bại.")
        else:
            with open(os.path.join(user_path, "password.txt"), "r") as f:
                stored_password = f.read().strip()

            if password == stored_password:
                messagebox.showinfo("Thông báo", "Đăng nhập thành công.")
                self.confirm = True
                self.screen.destroy()
            else:
                messagebox.showerror("Lỗi", "Mật khẩu không đúng. Đăng nhập thất bại.")
                self.screen2.destroy()


    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        email = self.register_email_entry.get()

        user_path = os.path.join(self.user_data_path, username)
        if os.path.exists(f"data/{username}.jpg"):
            messagebox.showinfo("Đăng ký", "Tên đăng nhập đã tồn tại. Hãy chọn tên đăng nhập khác.")
            return

        if os.path.exists(user_path):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác.")
        else:
            os.makedirs(user_path)
            with open(os.path.join(user_path, "password.txt"), "w") as f:
                f.write(password)

            self.send_registration_email(username, email)
            messagebox.showinfo("Thông báo", "Đăng ký thành công")
            self.screen1.destroy()

    def window_register(self):
        self.screen1 = Toplevel(self.screen2)
        self.screen1.geometry("640x360")
        Label(self.screen1, text="Tên đăng nhập * ").pack()
        self.register_username_entry = tk.Entry(self.screen1)
        self.register_username_entry.pack(pady=10)
        Label(self.screen1, text="").pack()
        Label(self.screen1, text="Mật khẩu * ").pack()
        self.register_password_entry = tk.Entry(self.screen1, show="*")
        self.register_password_entry.pack(pady=10)
        Label(self.screen1, text="").pack()
        Label(self.screen1, text="email *").pack()
        self.register_email_entry = tk.Entry(self.screen1)
        self.register_email_entry.pack(pady=10)

        Button(self.screen1, text="Đăng ký", width=10, height=1, command=self.register).pack()

    def window_log_normal(self):
        self.screen2 = Toplevel(self.screen)
        Label(self.screen2, text="Tên đăng nhập:").pack()
        self.screen2.geometry("640x360")
        self.login_username_entry = Entry(self.screen2)
        self.login_username_entry.pack(pady=10)
        Label(self.screen2, text="Mật khẩu:").pack()
        self.login_password_entry = Entry(self.screen2)
        self.login_password_entry.pack(pady=10)

        Button(self.screen2, text="Đăng nhập", width=10, height=1, command=self.login_verify).pack()
        Button(self.screen2, text="Đăng ký", width=10, height=1, command=self.window_register).pack()

    def main_screen(self):
        bg = ImageTk.PhotoImage(file="392087-PCH79B-499.jpg")
        bg_image = Label(self.screen, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        login1_but = Button(text="Đăng nhập với mật khẩu" ,height="2", width="30" ,command=self.window_log_normal)
        login1_but.place(x=350, y=550)
        login2_but = Button(text="Đăng nhập với nhận diện khuôn mặt", height="2", width="30", command=self.window_log_face)
        login2_but.place(x=700, y=550)

        self.screen.mainloop()

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.main_screen()