import customtkinter as ctk
from tkinter import messagebox
from PIL import Image,ImageTk
from db import Database
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Reports_Dataset import ReportsDatasets
from data_analysis import DataAnalysis
from water_qual import WaterQuality
from clusters import Clusters
from anomalies import Anomalies
from predict import Predictor
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
fontj = "JetBrains Mono"
fonti = "Inter"
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AquaGuard - Water Quality Analytics & Decision Support System") #Title of project.
        self.geometry("1600x900")
        self.minsize(1300, 750)
        icon = Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/applogo.png")
        self.iconphoto(False, ImageTk.PhotoImage(icon))
        self.bg = "#F5F7FA"
        self.header_color = "#FFFFFF"
        self.sidebar_color = "#0F172A"
        self.content_color = "#F8FAFC"
        self.configure(fg_color=self.bg)
        self.header = ctk.CTkFrame(self,height=70,corner_radius=0,fg_color=self.header_color) #Header bar.
        self.header.pack(fill = "x",padx = "20")
        self.header.pack_propagate(False)
        self.body = ctk.CTkFrame(self, fg_color="transparent") #Main body.
        self.body.pack(fill = "both", expand = True)
        self.sidebar = ctk.CTkFrame(self.body,width=350,corner_radius=0,fg_color=self.sidebar_color)
        self.sidebar.pack(side = "left", fill = "y")
        self.sidebar.pack_propagate(False)
        self.content = ctk.CTkFrame(self.body,corner_radius=0,fg_color=self.content_color)
        self.content.pack(side = "left", fill = "both", expand = True)
        self.title_label = ctk.CTkLabel(self.header,text = "Welcome to dashboard",font=(fonti, 28, "bold"),text_color="#2C96C4")
        self.title_label.pack(side = "left")
        self.user_label = ctk.CTkLabel(self.header,text = "Welcome User!",font=(fonti, 28, "bold"), text_color="#2C96C4" )
        self.user_label.pack(side = "right", padx = 20)
        # btns = ["Home","Data Analysis -da","Water Quality-wa","Clustering -cl","Anomaly Detction-ad","Reports-rp","Database / Dataset- dt"]
        home_btn = ctk.CTkButton(self.sidebar,text = "Home", command=self.show_home ,width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"))
        home_btn.pack(pady = 5)
        da_btn = ctk.CTkButton(self.sidebar,text = "Data Analysis", command=self.show_analysis,width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"))
        da_btn.pack(pady = 5)
        wa_btn = ctk.CTkButton(self.sidebar,text = "Water Quality", command=self.show_water_quality,width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"))
        wa_btn.pack(pady = 5)
        cl_btn = ctk.CTkButton(self.sidebar,text = "Clustering", command=self.show_cluster,width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"))
        cl_btn.pack(pady = 5)
        ad_btn = ctk.CTkButton(self.sidebar,text = "Anomaly Detction", command=self.show_anomaly,width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"))
        ad_btn.pack(pady = 5)
        rp_btn = ctk.CTkButton(self.sidebar,text = "Reports and Datasets",width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"),command=self.showReportsDataset)
        rp_btn.pack(pady = 5)
        p_btn = ctk.CTkButton(self.sidebar,text = "AI Based Water Assessment",width=220,height=42,fg_color="transparent",hover_color="#1E293B",anchor="w",font=(fontj,22,"bold"),command=self.showPredict)
        p_btn.pack(pady = 5)
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(expand = True)
        logoutbtn = ctk.CTkButton(self.sidebar,text = "Logout",font=(fontj, 24, "bold"),width=220,height=42,fg_color="#DC2626",hover_color="#B91C1C",text_color="white",command=self.logout)
        logoutbtn.pack(pady = 20)
        self.db = Database()
        self.analysis = DataAnalysis(self.content, self.db)
        self.water = WaterQuality(self.content, self.db)
        self.cluster = Clusters(self.content, self.db)
        self.anomaly = Anomalies(self.content, self.db)
        self.repDataset = ReportsDatasets(self.content, self.db)
        self.predictor= Predictor(self.content)
        self.show_home()
    
    def show_home(self):
        self.clear_content()
        self.loadDashboardData()
        self.loadDashboardAverages()
        self.loadPollutionTrend()
        self.loadClusterDistribution()
        home = ctk.CTkFrame(self.content, fg_color="transparent")
        home.pack(fill = "both", expand = True, padx = 25, pady = 25)
        self.createHeader(home)
        self.statisticsCards(home)
        self.createCharts(home)
        self.createSummary(home)
        
        
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def logout(self):
        from login import Aquaguard
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy()
            Aquaguard().mainloop()
        
    def show_analysis(self):
        self.title_label.configure(text="Data Analysis")
        self.clear_content()
        self.analysis.show()
    
    def showPredict(self):
        self.title_label.configure(text="Predict new data")
        self.clear_content()
        self.predictor.show()

    def show_water_quality(self):
        self.title_label.configure(text="Water Quality Analysis")
        self.clear_content()
        self.water.show()

    def show_cluster(self):
        self.title_label.configure(text="Cluster and PCA Analysis")
        self.clear_content()
        self.cluster.show()

    def show_anomaly(self):
        self.title_label.configure(text="Anomaly Analysis")
        self.clear_content()
        self.anomaly.show()

    def showReportsDataset(self):
        self.title_label.configure(text="Reports and Datasets")
        self.clear_content()
        self.repDataset.show()
    
    def createHeader(self,parent):
        ctk.CTkLabel(parent,text="Dashboard",font=("JetBrains Mono", 28, "bold"),text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(parent,text="Water Quality Analytics Overview",font=("JetBrains Mono", 15),text_color="#64748B").pack(anchor="w", pady=(0,20))
    
    def statisticsCards(self,parent):
        stats = ctk.CTkFrame(parent, fg_color="transparent")
        stats.pack(fill="x")
        cards = [("Total Samples", self.total_samples),("States", self.total_states),("Clusters",self.total_clusters),("Anomalies",self.total_anomalies)]
        for title, value in cards:
            card = ctk.CTkFrame(stats,width=220,height=120,fg_color="white",border_width=1,border_color="#E2E8F0",corner_radius=12)
            card.pack(side="left", padx=10)
            card.pack_propagate(False)
            ctk.CTkLabel(card,text=title,font=("JetBrains Mono",13),text_color="#64748B").pack(pady=(20,5))
            ctk.CTkLabel( card, text=value,font=("JetBrains Mono",30,"bold"),text_color="#2563EB").pack()
        
    def createCharts(self,parent):
        charts = ctk.CTkFrame(parent, fg_color="transparent",width=1000)
        charts.pack(fill="x", pady=25)
        self.left = ctk.CTkFrame(charts,width=400,height=280,fg_color="white",border_width=1,border_color="Dark Blue",corner_radius=12)
        self.left.pack(side="left", padx=20)
        self.left.pack_propagate(False)
        ctk.CTkLabel(self.left,text="Pollution Trend",font=("JetBrains Mono", 18, "bold")).pack(pady=20)
        self.right = ctk.CTkFrame(charts,width=400,height=280,fg_color="white",border_width=1,border_color="Dark Blue",corner_radius=12)
        self.right.pack(side="left", padx=20)
        self.right.pack_propagate(False)
        ctk.CTkLabel(self.right,text="Cluster Distribution",font=("JetBrains Mono", 18, "bold")).pack(pady=20)
        self.drawPollutionChart()
        self.drawClusterChart()
        
    def createSummary(self,parent):
        summary = ctk.CTkFrame(parent,height=170,fg_color="white")
        summary.pack(fill="x")
        summary.pack_propagate(False)
        ctk.CTkLabel(summary,text="Database Summary",font=("JetBrains Mono",18,"bold")).pack(anchor="w", padx=20, pady=(20,10))
        ctk.CTkLabel(summary,text="(Cl - Cluster) Cl 0:Normal, Cl 1:Moderately Polluted, Cl 3:Polluted",font = ("JetBrains Mono",14),text_color="Dark Blue").pack(anchor="w", padx=20)
        ctk.CTkLabel(summary,text="Latest statistics and activity will appear here",font = ("JetBrains Mono",14),text_color="#64748B").pack(anchor="w", padx=20)
        averages = [
        ("Average pH", self.avg_ph),
        ("Average DO", self.avg_do),
        ("Average BOD", self.avg_bod),
        ("Average Nitrate", self.avg_nitrate),
        ("Average Conductivity", self.avg_conductivity)]
        for label, value in averages:
            ctk.CTkLabel(summary, text=f"{label} : {value}", font=("JetBrains Mono", 14)).pack(anchor="w", padx=20, pady=3)
    
    def loadDashboardData(self):
        summary = self.db.dashboard_summary()
        self.total_samples = summary["total_samples"]
        self.total_states = summary["total_states"]
        self.total_clusters = summary["total_clusters"]
        self.total_anomalies = summary["total_anomalies"]
    
    def loadDashboardAverages(self):
        averages = self.db.dashboard_averages()
        self.avg_ph = averages["avg_ph"]
        self.avg_do = averages["avg_do"]
        self.avg_bod = averages["avg_bod"]
        self.avg_nitrate = averages["avg_nitrate"]
        self.avg_conductivity = averages["avg_conductivity"]
        
    def loadPollutionTrend(self):
        self.pollution_data = self.db.pollutionTrend()


    def loadClusterDistribution(self):
        self.cluster_data = self.db.cluster_distribution()
        
    def drawPollutionChart(self):
        states = [row["state"] for row in self.pollution_data[:10]]
        pollution = [row["avg_pollution"] for row in self.pollution_data[:10]]
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(states, pollution)
        ax.set_title("Average Pollution Index")
        ax.set_xlabel("State")
        ax.set_ylabel("Pollution Index")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        fig.savefig(
            "/home/abhinav/Desktop/Aquagaurd_Project/Assets/poll.png",
            dpi=300,
            bbox_inches="tight"
        )
        img = Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/poll.png")
        self.pollImage = ctk.CTkImage(
            light_image=img,
            size=(650, 350)
        )
        self.pollLabel = ctk.CTkLabel(
            self.left,
            image=self.pollImage,
            text=""
        )
        self.pollLabel.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        self.pollLabel.bind(
            "<Button-1>",
            lambda e: self.openFigure(
                fig,
                "Average Pollution Index"
            )
        )

    def drawClusterChart(self):
        labels = [f"Cl {row['cluster']}" for row in self.cluster_data]
        values = [row["total"] for row in self.cluster_data]
        self.clusterFigure = Figure(figsize=(6,4), dpi=100)
        ax = self.clusterFigure.add_subplot(111)
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Cluster Distribution")
        canvas = FigureCanvasTkAgg(self.clusterFigure, master=self.right)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                        self.clusterFigure,
                        "Cluster Distribution"))
        
    def openFigure(self, figure, title):
            top = ctk.CTkToplevel(self)
            top.title(title)
            top.geometry("1000x750")
            canvas = FigureCanvasTkAgg(figure, master=top)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
                
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
    
    
