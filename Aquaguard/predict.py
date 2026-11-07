import joblib
import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from ai_helper_api import AIHelper
import traceback
import threading
class Predictor:
    def __init__(self,parent):
        self.parent = parent
        self.scaler = joblib.load("/home/abhinav/Desktop/Aquagaurd_Project/models/scaler.pkl")
        self.kmeans = joblib.load("/home/abhinav/Desktop/Aquagaurd_Project/models/kmeans_model.pkl")
        self.iso = joblib.load("/home/abhinav/Desktop/Aquagaurd_Project/models/isolation_forest_model.pkl")
        self.ai = AIHelper()
        
    def show(self):
        self.main=ctk.CTkScrollableFrame(self.parent,fg_color="transparent",height = 300,width=1000)
        self.main.pack(fill="both",expand=True,padx=25,pady=25)
        ctk.CTkLabel(self.main,text="Predict Water Quality",font=("JetBrains Mono",28,"bold")).pack(anchor="w")
        ctk.CTkLabel(self.main,text="Enter water quality parameters to predict Cluster and Anomaly.",text_color="#64748B").pack(anchor="w",pady=(0,20))
        form=ctk.CTkFrame(self.main,height = 350)
        form.pack(fill="x",padx = 20 ,pady = 20)
        form.pack_propagate(False)
        ctk.CTkLabel(form, text="pH", font=("JetBrains Mono", 12, "bold")).grid(row=0, column=0, padx=(40,20), pady=(15,5))
        ctk.CTkLabel(form, text="DO", font=("JetBrains Mono", 12, "bold")).grid(row=0, column=1, padx=(40,20), pady=(15,5))
        self.ph = self.entry(form, 1, 0)
        self.do = self.entry(form, 1, 1)
        ctk.CTkLabel(form, text="BOD", font=("JetBrains Mono", 12, "bold")).grid(row=2, column=0, padx=(40,20), pady=(10,5))
        ctk.CTkLabel(form, text="Nitrate", font=("JetBrains Mono", 12, "bold")).grid(row=2, column=1, padx=(40,20), pady=(10,5))
        self.bod = self.entry(form, 3, 0)
        self.nitrate = self.entry(form, 3, 1)
        ctk.CTkLabel(form, text="Conductivity", font=("JetBrains Mono", 12, "bold")).grid(row=4, column=0, padx=(40,20), pady=(10,5))
        ctk.CTkLabel(form, text="Temperature", font=("JetBrains Mono", 12, "bold")).grid(row=4, column=1, padx=(40,20), pady=(10,5))
        self.cond = self.entry(form, 5, 0)
        self.temp = self.entry(form, 5, 1)
        ctk.CTkButton(form,text="Predict",command=self.predict,width=250,height = 42,fg_color="#2563EB",
        hover_color="#1D4ED8").grid(row=6,column=0,columnspan=2,pady=25)
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)
        result=ctk.CTkScrollableFrame(self.main)
        result.pack(fill="x",pady=20)
        ctk.CTkLabel(result,text="Prediction Result",font=("JetBrains Mono",18,"bold")).pack(anchor="w",padx=20,pady=(15,10))
        self.result=ctk.CTkTextbox(result,height=300)
        self.result.pack(fill="x",padx=20,pady=(0,20))
        self.createInputGuide()
        

    def entry(self,parent,r,c):
        e=ctk.CTkEntry(parent,width=260)
        e.grid(row=r,column=c,padx=(40,20),pady=(0,10))
        return e

    def generatePrediction(self):
        try:
            values = [
                float(self.ph.get()),
                float(self.do.get()),
                float(self.bod.get()),
                float(self.nitrate.get()),
                float(self.cond.get()),
                float(self.temp.get())
            ]
            df = pd.DataFrame(
                [[
                    values[5],   # Temperature
                    values[2],   # BOD
                    values[0],   # pH
                    values[4],   # Conductivity
                    0.5,         # Fluoride
                    values[3]    # Nitrate
                ]],
                columns=[
                    "Temperature",
                    "BOD",
                    "pH",
                    "Conductivity",
                    "Fluoride",
                    "Nitrate"
                ]
            )
            x = self.scaler.transform(df)
            cluster = int(self.kmeans.predict(x)[0])
            anomaly = "Anomaly" if self.iso.predict(x)[0] == -1 else "Normal"
            names = {
                0: "Good Water Quality",
                1: "Moderately Polluted",
                2: "Highly Polluted"
            }
            analysis = self.ai.analyze(
                ph=values[0],
                do=values[1],
                bod=values[2],
                nitrate=values[3],
                conductivity=values[4],
                temperature=values[5],
                category=names[cluster],
                anomaly=anomaly
            )
            text = f"""
    Prediction Completed

    Cluster : {cluster}

    Category : {names[cluster]}

    Status : {anomaly}

    ==================================

    AI Water Quality Assessment

    {analysis}
    """
            self.main.after(0, lambda: self.show_result(text))
        except Exception as e:
            self.main.after(0, lambda: messagebox.showerror("Error", str(e)))
    
    def predict(self):
            self.result.configure(state="normal")
            self.result.delete("1.0", "end")
            self.result.insert("end", "Generating AI analysis...\nPlease wait...")
            self.result.configure(state="disabled")

            threading.Thread(
                target=self.generatePrediction,
                daemon=True
            ).start()
            
    def show_result(self, text):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("end", text)
        self.result.configure(state="disabled")
            
    def createInputGuide(self):
            frame = ctk.CTkFrame(self.main, fg_color="white", border_width=1, border_color="#E2E8F0")
            frame.pack(fill="x", padx=20, pady=15)
            ctk.CTkLabel(frame,text="Valid Input Ranges",font=("JetBrains Mono",16,"bold")).pack(anchor="w",padx=15,pady=(10,5))
            guide = """
        • pH            : 0 - 14
        • Temperature   : 0 - 50 °C
        • Conductivity  : 0 - 3000 µS/cm
        • DO            : 0 - 20 mg/L
        • BOD           : 0 - 30 mg/L
        • Nitrate       : 0 - 100 mg/L
        Enter only numeric values."""
            ctk.CTkLabel(frame,text=guide,font=("JetBrains Mono",13),justify="left",anchor="w").pack(anchor="w",padx=15,pady=(0,12))
                    
            
