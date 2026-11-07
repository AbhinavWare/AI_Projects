import customtkinter as ctk
from db import Database
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataAnalysis:
    def __init__(self,parent,db):
        self.parent = parent
        self.db = db
    
    def show(self):
        self.main = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=25, pady=25)
        self.createHeader()
        self.createParameterCards()
        self.createStateAnalysis()
        self.createComparisonSection()
        self.createInsightsSection()
        self.loadDashboardData()
        self.drawComparisonChart()
        self.drawParameterChart()
        
    def createHeader(self):
        header = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))
        ctk.CTkLabel(header,text="Data Analysis",font=("JetBrains Mono",28,"bold")).pack(anchor="w")
        ctk.CTkLabel(header,text="Water Quality Statistical Analysis",text_color="#64748B"
        ).pack(anchor="w")

    def createParameterCards(self):
        self.cards = ctk.CTkFrame(self.main, fg_color="transparent")
        self.cards.pack(fill="x", pady=15)
        self.phCard = self.createCard(self.cards,"Average pH","0.00")
        self.doCard = self.createCard(self.cards,"Average DO","0.00")
        self.bodCard = self.createCard(self.cards,"Average BOD","0.00")
        self.nitrateCard = self.createCard(self.cards,"Average Nitrate","0.00")
        self.condCard = self.createCard(self.cards,"Average Conductivity","0.00")
        
    def createCard(self,parent,title,value):
        card = ctk.CTkFrame(parent,width=210,height=110,corner_radius=12,fg_color="white",border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(side="left",padx=10)
        card.pack_propagate(False)
        ctk.CTkLabel( card,text=title,font=("JetBrains Mono",12),text_color="#64748B"
        ).pack(pady=(20,5))
        valueLabel = ctk.CTkLabel(card,text=value,font=("JetBrains Mono",28,"bold"),text_color="#2563EB")
        valueLabel.pack()
        return valueLabel
    
    def createStateAnalysis(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="x",pady=15)
        ctk.CTkLabel(frame,text="State Analysis",font=("JetBrains Mono",18,"bold")
        ).pack(anchor="w",padx=20,pady=15)
        self.stateBox = ctk.CTkComboBox(frame,values=["Select State"],width=250
        )
        self.stateBox.pack(anchor="w",padx=20)
        ctk.CTkButton(frame,text="Load Analysis",command=self.loadStateSummary
        ).pack(anchor="w",padx=20,pady=15)
        self.stateSummary = ctk.CTkTextbox(frame,height=180
        )
        self.stateSummary.pack(fill="x",padx=20,pady=(0,20))


    def createComparisonSection(self):
        charts = ctk.CTkFrame(self.main,fg_color="transparent")
        charts.pack(fill="both",expand=True,pady=15)
        self.leftChart = ctk.CTkFrame(charts)
        self.leftChart.pack(side="left",fill="both",expand=True,padx=(0,10))
        self.rightChart = ctk.CTkFrame(charts)
        self.rightChart.pack(side="left",fill="both",expand=True,padx=(10,0))

    def createInsightsSection(self):
        insight = ctk.CTkFrame(self.main)
        insight.pack(fill="x",pady=15)
        ctk.CTkLabel(insight,text="Quick Insights",font=("JetBrains Mono",18,"bold")
        ).pack(anchor="w",padx=20,pady=(15,10))
        self.insightBox = ctk.CTkTextbox(insight,height=140)
        self.insightBox.pack(fill="x",padx=20,pady=(0,20))
        ctk.CTkButton(
        insight,
                                             text="Export Analysis",
                                             command=self.exportAnalysis
                                             ).pack(anchor="e", padx=20, pady=(0,15))

    def loadDashboardData(self):
        avg = self.db.dashboard_averages()
        self.phCard.configure(text=str(avg["avg_ph"]))
        self.doCard.configure(text=str(avg["avg_do"]))
        self.bodCard.configure(text=str(avg["avg_bod"]))
        self.nitrateCard.configure(text=str(avg["avg_nitrate"]))
        self.condCard.configure(text=str(avg["avg_conductivity"]))
        states = ["Select State"]
        for row in self.db.getStates():
            states.append(row["state"])
        self.stateBox.configure(values=states)
        self.loadInsights()

    def loadStateSummary(self):
        state = self.stateBox.get()
        if state == "Select State":
            return
        data = self.db.state_summary(state)
        self.stateSummary.delete("1.0","end")
        self.stateSummary.insert(
            "end",
            f"""
            State : {data['state']}

            Stations : {data['total_stations']}

            Average pH : {data['avg_ph']}

            Average DO : {data['avg_do']}

            Average BOD : {data['avg_bod']}

            Average Nitrate : {data['avg_nitrate']}

            Average Fluoride : {data['avg_fluoride']}

            Average Conductivity : {data['avg_conductivity']}

            Average Pollution : {data['avg_pollution']}
            """)

    def loadInsights(self):
        self.insightBox.delete("1.0","end")
        self.insightBox.insert(
            "end",
            "Average water quality statistics loaded.\n"
            "State-wise analysis available.\n"
            "Compare pollution across states.\n"
            "Identify regions requiring attention.\n")
        
        
    def drawComparisonChart(self):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        data = self.db.topPollutedStates()
        states = [row["state"] for row in data]
        pollution = [row["pollution"] for row in data]
        self.compareFigure = Figure(figsize=(6,4), dpi=100)
        ax = self.compareFigure.add_subplot(111)
        ax.bar(states, pollution)
        ax.set_title("Top Polluted States")
        ax.tick_params(axis="x", rotation=45)
        canvas = FigureCanvasTkAgg(
            self.compareFigure,
            master=self.leftChart
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                                self.compareFigure,
                                "Cluster Distribution"))
        
    def drawParameterChart(self):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        for widget in self.rightChart.winfo_children():
            widget.destroy()
        data = self.db.parameterDistribution("ph")
        values = [row["ph"] for row in data]
        self.clusterFigure = Figure(figsize=(6,4), dpi=100)
        ax = self.clusterFigure.add_subplot(111)
        ax.hist(values, bins=15)
        ax.set_title("pH Distribution")
        ax.set_xlabel("pH")
        ax.set_ylabel("Frequency")
        canvas = FigureCanvasTkAgg(
            self.clusterFigure,
            master=self.rightChart
        )
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                                self.clusterFigure,
                                "Cluster Distribution"))
        
    def exportAnalysis(self):
        data = self.db.getAll()
        records = [[
            "Station Name",
            "State",
            "pH",
            "Temperature",
            "Conductivity",
            "Nitrate",
            "Fluoride"
        ]]
        for row in data:
            records.append([
                row["station_name"],
                row["state"],
                row["ph"],
                row["temperature"],
                row["conductivity"],
                row["nitrate"],
                row["fluoride"]
            ])
        from report import generatePDF
        generatePDF(records)
        
    def openFigure(self, figure, title):
            top = ctk.CTkToplevel(self.parent)
            top.title(title)
            top.geometry("1000x750")
            canvas = FigureCanvasTkAgg(figure, master=top)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)