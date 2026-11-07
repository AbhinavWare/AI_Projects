import customtkinter as ctk
from db import Database
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Clusters:
    def __init__(self,parent,db):
        self.parent = parent
        self.db = db
    
    def show(self):
        self.main = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=25, pady=25)
        self.createHeader()
        self.createParameterCards()
        self.createCharts()
        self.createResultFrame()     
        self.loadClusterData()
        
    def openFigure(self, figure, title):
            top = ctk.CTkToplevel(self.parent)
            top.title(title)
            top.geometry("1000x750")
            canvas = FigureCanvasTkAgg(figure, master=top)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
                
    def createHeader(self):
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(fill="x", pady=(0,20))
        ctk.CTkLabel(header,text="Clusters",font=("JetBrains Mono",28,"bold")).pack(anchor="w")
        ctk.CTkLabel(header,text="K-Means Clustering Results in 3 distinct groups, it divided water samples in 3 groups.",text_color="#64748B"
        ).pack(anchor="w")

    def createParameterCards(self):
        self.cards = ctk.CTkFrame(self.main, fg_color="transparent")
        self.cards.pack(fill="x", pady=15)
        self.clusterCard = self.createCard(self.cards,"Total Clusters","3")
        self.sampleCard = self.createCard(self.cards,"Total Samples in 2021","988")
        self.scoreCard= self.createCard(self.cards,"Silhouette Score","0.31")
        self.pcaCard = self.createCard(self.cards,"PCA Components","2")
       
        
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
        ctk.CTkLabel(frame,text="Cluster Interpretation",font=("JetBrains Mono",18,"bold")
        ).pack(anchor="w", padx=20, pady=15)
        self.resultBox = ctk.CTkTextbox(frame,height=180)
        self.resultBox.pack(fill="x",padx=20,pady=(0,20))
        ctk.CTkButton(
            frame,
            text="Export Cluster Report",
            command=self.exportClusters
        ).pack(anchor="e", padx=20, pady=(0,15))
        
    def loadClusterData(self):
        self.clusterCard.configure(text="3")
        self.sampleCard.configure(text="988")
        self.scoreCard.configure(text="0.31")
        self.pcaCard.configure(text="2")
        self.drawClusterChart()
        self.drawPCA()
        self.loadClusterSummary()

    def loadClusterSummary(self):
            self.resultBox.delete("1.0","end")
            self.resultBox.insert("end",
                """
            K-Means Clustering Results
            • Number of Clusters : 3
            • Silhouette Score : 0.31
            
            Cluster 0
            Good Water Quality
            Low Pollution

            Cluster 1
            Moderate Pollution
            Requires Monitoring

            Cluster 2
            High Pollution
            Immediate Attention Required

            PCA was applied to reduce multiple water quality
            parameters into two principal components for
            visual visualization of clusters.
            """
            )    
  
    def drawClusterChart(self):
        data = self.db.cluster_distribution()
        clusters = [f"Cluster {row['cluster']}" for row in data]
        counts = [row["total"] for row in data]
        self.fig = Figure(figsize=(6,4), dpi=100)
        ax = self.fig.add_subplot(111)
        ax.bar(clusters, counts)
        ax.set_title("Cluster Distribution")
        ax.set_xlabel("Clusters")
        ax.set_ylabel("Samples")
        canvas = FigureCanvasTkAgg(self.fig,master=self.leftChart)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        widget.bind("<Button-1>",lambda e: self.openFigure(
                                        self.fig,
                                        "Cluster Distribution"))
                
        
    def drawPCA(self):
        image = ctk.CTkImage(Image.open("/home/abhinav/Desktop/Aquagaurd_Project/Assets/pca.png"),size=(520,350))
        label = ctk.CTkLabel(self.rightChart,image=image,text="")
        label.image = image
        label.pack(expand=True)
        self.createPCALegend()
        
    def exportClusters(self):
        records = [["Total Clusters", "3"],["Total Samples", "988"],["Silhouette Score", "0.31"],["PCA Components", "2"]]
        from report import generatePDF
        generatePDF(records)
        
    def createPCALegend(self):
        legend = ctk.CTkFrame(self.rightChart,fg_color="white",corner_radius=10,border_width=1,border_color="#E2E8F0")
        legend.pack(fill="x", padx=10, pady=(5,10))
        ctk.CTkLabel(legend,text="PCA Cluster Legend",font=("JetBrains Mono",14,"bold")
        ).pack(anchor="w", padx=12, pady=(8,5))
        colors = [("(Blue dots)Cluster 0", "Good Water Quality"),("Cluster 1", "(Light Gray dots)Moderate Water Quality"),("(Red dots)Cluster 2", "Highly Polluted Water")]
        for cluster, desc in colors:
            ctk.CTkLabel(legend,text=f"{cluster}  -  {desc}",anchor="w",font=("JetBrains Mono",12)
            ).pack(fill="x", padx=15, pady=2)