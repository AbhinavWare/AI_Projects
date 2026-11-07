import customtkinter as ctk
from db import Database
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from report import generatePDF

class Anomalies:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def show(self):
        self.main = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=25, pady=25)
        self.createHeader()
        self.createCards()
        self.createCharts()
        self.createResultFrame()
        self.loadAnomalyData()
        
    def createHeader(self):
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))
        ctk.CTkLabel(header,text="Anomaly Detection",font=("JetBrains Mono",28,"bold")).pack(anchor="w")
        ctk.CTkLabel(header,text="Isolation Forest, Random Forest & KNN Analysis",text_color="#64748B"
        ).pack(anchor="w")
        
    def createCards(self):
            self.cards = ctk.CTkFrame(self.main, fg_color="transparent")
            self.cards.pack(fill="x", pady=15)
            self.total = self.createCard(self.cards,"Total Clusters","3")
            self.normal = self.createCard(self.cards,"Total Samples in 2021","988")
            self.anomaly = self.createCard(self.cards,"Silhouette Score","0.31")
            self.rf = self.createCard(self.cards,"PCA Components","2")
            
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
        
    def createCharts(self):
            charts = ctk.CTkFrame(self.main, fg_color="transparent")
            charts.pack(fill="both", expand=True, pady=15)
            self.leftChart = ctk.CTkFrame(charts)
            self.leftChart.pack(side="left", fill="both", expand=True, padx=(0,10))
            self.rightChart = ctk.CTkFrame(charts)
            self.rightChart.pack(side="left", fill="both", expand=True, padx=(10,0))
    
    def createResultFrame(self):
            frame = ctk.CTkFrame(self.main)
            frame.pack(fill="x", pady=20)
            ctk.CTkLabel(frame,text="Prediction Results",font=("JetBrains Mono",18,"bold")
            ).pack(anchor="w", padx=20, pady=15)
            self.resultBox = ctk.CTkTextbox(frame,height=180)
            self.resultBox.pack(fill="x",padx=20,pady=(0,20))
            ctk.CTkButton(frame,
            text="Export Report",
            command=self.exportAnomalyReport
            ).pack(anchor="e", padx=20, pady=(0,15))
            
    def loadAnomalyData(self):
        summary = self.db.anomalySummary()
        accuracy = self.db.modelAccuracy()
        self.total.configure(text=str(summary["total"]))
        self.normal.configure(text=str(summary["normal"]))
        self.anomaly.configure(text=str(summary["anomaly"]))
        self.rf.configure(text=f"{accuracy['Random Forest']}%")
        self.drawAnomalyChart()
        self.drawPredictionChart()
        self.loadPredictionSummary()
        
    def openFigure(self, figure, title):
            top = ctk.CTkToplevel(self.parent)
            top.title(title)
            top.geometry("1000x750")
            canvas = FigureCanvasTkAgg(figure, master=top)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def drawAnomalyChart(self):
        data = self.db.anomalyDistribution()
        labels = ["Normal","Anomaly"]
        values = [
            data["normal"],
            data["anomaly"]
        ]
        self.anomalyFigure = Figure(figsize=(5,4), dpi=100)
        ax = self.anomalyFigure.add_subplot(111)
        ax.bar(labels, values)
        ax.set_title("Isolation Forest Result")
        canvas = FigureCanvasTkAgg(self.anomalyFigure,master=self.leftChart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                                                self.anomalyFigure,
                                                "Cluster Distribution"))

    def drawPredictionChart(self):
        data = self.db.modelAccuracy()
        models = list(data.keys())
        accuracy = list(data.values())
        self.clusterFigure = Figure(figsize=(5,4), dpi=100)
        ax = self.clusterFigure.add_subplot(111)
        ax.bar(models, accuracy)
        ax.set_ylim(0,100)
        ax.set_ylabel("Accuracy (%)")
        ax.set_title("Model Comparison")
        canvas = FigureCanvasTkAgg(self.clusterFigure,master=self.rightChart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                                                self.clusterFigure,
                                                "Cluster Distribution"))

    def loadPredictionSummary(self):
        summary = self.db.anomalySummary()
        accuracy = self.db.modelAccuracy()
        self.resultBox.delete("1.0","end")
        self.resultBox.insert("end",
            f"""
        Isolation Forest Results
        Total Samples : {summary['total']}
            Normal Samples : {summary['normal']}
            Anomalies Detected : {summary['anomaly']}
            Random Forest Accuracy : {accuracy['Random Forest']}%
            KNN Accuracy : {accuracy['KNN']}%

            Conclusion

            • Isolation Forest successfully detected abnormal
            water quality samples.

            • Random Forest achieved the highest prediction
            accuracy.

            • KNN provides comparable performance and can
            be used as an alternative prediction model.

            • Detected anomalies should be investigated for
            possible contamination or unusual water quality.
            """)

    def exportAnomalyReport(self):
        summary = self.db.anomalySummary()
        accuracy = self.db.modelAccuracy()
        records = [
            ["Total Samples", summary["total"]],
            ["Normal Samples", summary["normal"]],
            ["Anomalies", summary["anomaly"]],
            ["Random Forest Accuracy", accuracy["Random Forest"]],
            ["KNN Accuracy", accuracy["KNN"]]
        ]
        generatePDF(records)