import db
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import customtkinter as ctk
from dashboard import Dashboard
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
TITLE_FONT = ("Segoe UI", 30, "bold")

HEADING_FONT = ("Segoe UI", 22, "bold")

TEXT_FONT = ("Segoe UI", 15)

BUTTON_FONT = ("Segoe UI", 15, "bold")
class Aquaguard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = db.Database()
        self.configure(fg_color="#F4F7FA")
        self.title("Aquaguard")
        self.geometry("1800x900")
        self.minsize(1000, 650)
        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=6)
        self.grid_rowconfigure(0,weight=1)
        self.maincard = ctk.CTkFrame(self, width = 2000, height = 1800, corner_radius=25, border_width=2, fg_color="#FFFDF6", border_color="#EBCB8B")
        self.maincard.place(relx = 0.5, rely =0.5 ,anchor = "center")
        self.maincard.grid_propagate(False)
        self.leftframe = ctk.CTkFrame(self.maincard,fg_color="transparent")
        self.leftframe.configure(width=500, height=500)
        self.leftframe.pack(side = "left", padx = 60, pady = 40)
        self.rightframe = ctk.CTkFrame(self.maincard,fg_color="transparent")
        self.rightframe.pack(side = "right", padx = (20,50), pady = 40, fill = "both", expand = True)
        self.left_image = ctk.CTkImage(
        light_image=Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/water.jpg"),
        dark_image=Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/water.jpg"),
        size=(500, 500))
        self.left_image_label = ctk.CTkLabel(
        self.leftframe,
        image=self.left_image,
        text=""
        )
        self.left_image_label.pack( 
            pady = 40
        )
        self.project_title = ctk.CTkLabel(
        self.leftframe,
        text="AquaGuard",
        font=TITLE_FONT,
        text_color="#1565C0"
        )
        self.project_title.pack()
        self.subtitle = ctk.CTkLabel(
        self.leftframe,
        text="Water Quality Analytics\n& Decision Support System",
        font=TEXT_FONT,
        justify="center",
        text_color="gray40"
        )
        self.subtitle.pack(pady=(10, 0))
        self.loginframe = ctk.CTkFrame(self.rightframe, fg_color="transparent")
        # self.loginframe.pack(pady=40, padx=40, fill="both", expand=True)
        self.loginheading = ctk.CTkLabel(self.loginframe,text = "Login...",font = HEADING_FONT)
        self.loginheading.pack(pady = (10,30))
        self.userlabel = ctk.CTkLabel(self.loginframe,text = "Enter username or email...",anchor = "w", font = TEXT_FONT)
        self.userlabel.pack(pady = (5,5), fill = "x")
        self.login_username_var = ctk.StringVar()
        self.login_username_entry = ctk.CTkEntry(self.loginframe, corner_radius=10,width=420,height=30,textvariable=self.login_username_var,placeholder_text="Enter choice...",font = TEXT_FONT)
        self.login_username_entry.pack(
        pady=(0, 15)
        )
        self.passlabel = ctk.CTkLabel(self.loginframe,text = "Enter password...",anchor = "w", font = TEXT_FONT)
        self.passlabel.pack(pady = (5,5), fill = "x")
        self.login_pass_var = ctk.StringVar()
        self.login_pass_entry = ctk.CTkEntry(self.loginframe,show = "*", corner_radius=10,width=420,height=30,textvariable=self.login_pass_var,placeholder_text="Enter password...",font = TEXT_FONT)
        self.login_pass_entry.pack(
        pady=(0, 10)
        )
        self.show_password = ctk.BooleanVar(value=False)
        self.check_passwordcheckbox = ctk.CTkCheckBox(self.loginframe,text= "Show Password...",command=self.toggle_password,variable=self.show_password)
        self.check_passwordcheckbox.pack(pady= (0,20), anchor = "w")
        self.loginbtn = ctk.CTkButton(self.loginframe, corner_radius=10,width=420,height=30,command=self.login,text = "LOGIN",font = BUTTON_FONT)
        self.loginbtn.pack(pady=10)
        self.signup_button = ctk.CTkButton(self.loginframe,text="Create an Account...",fg_color="transparent",hover=False,text_color="#1565C0",command=self.show_signup)
        self.signup_button.pack(pady=(20, 0))
        self.signupframe = ctk.CTkFrame(self.rightframe, fg_color="transparent")
        # self.signupframe.pack(pady=40, padx=40, fill="both", expand=True)
        self.signupheading = ctk.CTkLabel(self.signupframe, text="Create Account...", font=HEADING_FONT)
        self.signupheading.pack(pady=(10,30))
        self.fulllabel = ctk.CTkLabel(self.signupframe, text="Enter Full Name...", anchor="w", font=TEXT_FONT)
        self.fulllabel.pack(pady=(5,5), fill="x")
        self.fullname_var = ctk.StringVar()
        self.fullname_entry = ctk.CTkEntry(self.signupframe, corner_radius=10, width=420, height=30, textvariable=self.fullname_var, placeholder_text="Enter full name...", font=TEXT_FONT)
        self.fullname_entry.pack(pady=(0,15))
        self.userlabel = ctk.CTkLabel(self.signupframe, text="Enter Username...", anchor="w", font=TEXT_FONT)
        self.userlabel.pack(pady=(5,5), fill="x")
        self.signup_username_var = ctk.StringVar()
        self.signup_username_entry = ctk.CTkEntry(self.signupframe, corner_radius=10, width=420, height=30, textvariable=self.signup_username_var, placeholder_text="Choose username...", font=TEXT_FONT)
        self.signup_username_entry.pack(pady=(0,15))
        self.emaillabel = ctk.CTkLabel(self.signupframe, text="Enter Email...", anchor="w", font=TEXT_FONT)
        self.emaillabel.pack(pady=(5,5), fill="x")
        self.email_var = ctk.StringVar()
        self.email_entry = ctk.CTkEntry(self.signupframe, corner_radius=10, width=420, height=30, textvariable=self.email_var, placeholder_text="Enter email...", font=TEXT_FONT)
        self.email_entry.pack(pady=(0,15))
        self.passlabel = ctk.CTkLabel(self.signupframe, text="Create Password...", anchor="w", font=TEXT_FONT)
        self.passlabel.pack(pady=(5,5), fill="x")
        self.signup_pass_var = ctk.StringVar()
        self.signup_pass_entry = ctk.CTkEntry(self.signupframe, show="*", corner_radius=10, width=420, height=30, textvariable=self.signup_pass_var, placeholder_text="Create password...", font=TEXT_FONT)
        self.signup_pass_entry.pack(pady=(0,15))
        self.confirmlabel = ctk.CTkLabel(self.signupframe, text="Confirm Password...", anchor="w", font=TEXT_FONT)
        self.confirmlabel.pack(pady=(5,5), fill="x")
        self.confirm_var = ctk.StringVar()
        self.confirm_entry = ctk.CTkEntry(self.signupframe, show="*", corner_radius=10, width=420, height=30, textvariable=self.confirm_var, placeholder_text="Confirm password...", font=TEXT_FONT)
        self.confirm_entry.pack(pady=(0,15))
        self.show_signup_password = ctk.BooleanVar(value=False)
        self.signup_checkbox = ctk.CTkCheckBox(self.signupframe, text="Show Password...", variable=self.show_signup_password, command=self.toggle_signup_password)
        self.signup_checkbox.pack(anchor="w", pady=(0,20))
        self.signupbtn = ctk.CTkButton(self.signupframe, corner_radius=10, width=420, height=35, text="CREATE ACCOUNT", font=BUTTON_FONT, command=self.signup)
        self.signupbtn.pack(pady=10)
        self.loginlink = ctk.CTkButton(self.signupframe, text="Already have an account? Login", fg_color="transparent", hover=False, text_color="#1565C0", command=self.show_login)
        self.loginlink.pack(pady=(20,0))
        icon = Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/applogo.png")
        self.iconphoto(False, ImageTk.PhotoImage(icon))
        self.current_form = "login"
        self.show_login()

    def toggle_password(self):
        if self.show_password.get():
            self.login_pass_entry.configure(show="")
        else:
            self.login_pass_entry.configure(show="*")
                    
    def toggle_signup_password(self):
        if self.show_signup_password.get():
            self.pass_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")
            self.confirm_entry.configure(show="*")
            
    def login(self):
        username = self.login_username_entry.get().strip() #same for email.
        password = self.login_pass_entry.get() 
        if username == "" or password == "":
            messagebox.showerror("Missing data, please fill box through your username or email...")
            return
        res = self.db.login(username,password)

        if res:
            messagebox.showinfo("Login success!!!")
            self.openDashboard()
        else:
            messagebox.showerror("Login failed, please try again!!!")
       
    def signup(self):
        fullname = self.fullname_entry.get().strip()
        username = self.signup_username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.signup_pass_entry.get()
        confirm_password = self.confirm_entry.get()
        if not fullname or not username or not email or not password or not confirm_password:
            messagebox.showerror("Invalid signup, all fields are required!!!")
            return
        if password != confirm_password:
            messagebox.showerror("Passwords does not match, please renter password!!!")
            return
        res = self.db.signup(fullname,username,email,password)
        if res:
            messagebox.showinfo("Signup Successfull!!!")
            self.openDashboard()
        else:
            messagebox.showerror("Signup failed please try again!!!")
               
    def openDashboard(self): 
        self.destroy()
        app = Dashboard()
        app.mainloop()
        
    def show_login(self):
        self.signupframe.pack_forget()
        self.loginframe.pack(pady = 40, padx = 40, expand = True, fill = "both")
        # self.toggle_btn.configure(text="Sign Up")
        self.current_form = "login"
      
    def show_signup(self):
        self.loginframe.pack_forget()
        self.signupframe.pack(pady = 40, padx = 40, expand = True, fill = "both")
        # self.toggle_btn.configure(text="Login")
        self.current_form = "signup"
    
    def toggle_forms(self):
        if self.current_form == "login":
            self.show_signup()
        else:
            self.show_login()       
        
    def toggle_signup_password(self):
        if self.show_signup_password.get():
            self.signup_pass_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.signup_pass_entry.configure(show="*")
            self.confirm_entry.configure(show="*")
        
if __name__ == "__main__":
    app = Aquaguard()
    app.mainloop()