import customtkinter as ctk
from tkinter import ttk
from db import Database
from report import generatePDF,exportCSV
class ReportsDatasets:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        
        
    def show(self):
        self.main = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=25, pady=25)
        self.createHeader()
        self.createSearchSection()
        self.createFilterSection()
        self.createTable()
        self.createExportSection()
        self.loadFilters()
        records = self.db.getAll()
        self.loadTable(records)
        
    def createHeader(self):
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header,text="Database Explorer & Report Generation",font=("JetBrains Mono", 24, "bold")
        ).pack(anchor="w")
    
    
    def createSearchSection(self):
        search = ctk.CTkFrame(self.main)
        search.pack(fill="x", pady=10)
        self.searchEntry = ctk.CTkEntry(search,width=350,placeholder_text="Search Station / State...")
        self.searchEntry.pack(side="left", padx=10, pady=10)
        ctk.CTkButton( search,text="Search",command=self.searchData
        ).pack(side="left", padx=5)
        ctk.CTkButton( search,text="Refresh",command=self.refreshTable
        ).pack(side="left", padx=5)
        
    def createFilterSection(self):
        filters = ctk.CTkFrame(self.main)
        filters.pack(fill="x", pady=10)
        self.stateBox = ctk.CTkComboBox(filters,values=["All States"])
        self.stateBox.pack(side="left", padx=10)
        self.clusterBox = ctk.CTkComboBox(filters,values=["All Clusters"])
        self.clusterBox.pack(side="left", padx=10)
        ctk.CTkButton(filters,text="Apply",command=self.applyFilters).pack(side="left", padx=10)
        
    def createExportSection(self):
        export = ctk.CTkFrame(self.main)
        export.pack(fill="x", pady=10)
        ctk.CTkButton(export,text="Export PDF",command=self.exportPDF
        ).pack(side="left", padx=10)
        ctk.CTkButton(export,text="Export CSV",command=self.exportCSV
        ).pack(side="left", padx=10)
        
    def createTable(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True, pady=15)
        columns = (
            "Station",
            "State",
            "pH",
            "DO",
            "BOD",
            "Cluster"
        )
        self.table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=18
        )
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150, anchor="center")
        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)

    def searchData(self):
        keyword = self.searchEntry.get().strip()
        records = self.db.searchRecords(keyword)
        self.loadTable(records)
        
    def applyFilters(self):
        state = self.stateBox.get()
        cluster = self.clusterBox.get()
        records = self.db.filterRecords(state, cluster)
        self.loadTable(records)
        
    def refreshTable(self):
        self.searchEntry.delete(0, "end")
        self.stateBox.set("All States")
        self.clusterBox.set("All Clusters")
        records = self.db.getAll()
        self.loadTable(records)
        
    def exportPDF(self):
        records = []
        for item in self.table.get_children():
            records.append(self.table.item(item)["values"])
        generatePDF(records)
        
    def exportCSV(self):
        records = []
        for item in self.table.get_children():
            records.append(self.table.item(item)["values"])
        exportCSV(records)
        
    def loadTable(self, records):
        self.table.delete(*self.table.get_children())
        for row in records:
            self.table.insert("", "end", values=(row["station_name"],row["state"],row["ph"],row["do_level"],row["bod"],
        row["cluster"]
    ))
        
    def loadFilters(self):
        states = ["All States"]
        for row in self.db.getStates():
            states.append(row["state"])
        self.stateBox.configure(values=states)
        self.stateBox.set("All States")
        clusters = ["All Clusters"]
        for row in self.db.getClusters():
            clusters.append(str(row["cluster"]))
        self.clusterBox.configure(values=clusters)
        self.clusterBox.set("All Clusters")
    
    