from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
import csv
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from datetime import datetime
from tkinter import messagebox
import os
REPORT_DIR = "Reports"
os.makedirs(REPORT_DIR, exist_ok=True)
pdf_path = os.path.join(REPORT_DIR, "Water_Report.pdf")
def generatePDF(records):
    styles = getSampleStyleSheet()
    title = Paragraph(
    "<b>AquaGuard - Water Quality Analytics Report</b>",
    styles["Title"])
    date = Paragraph(
    datetime.now().strftime("%d-%m-%Y %H:%M"),
    styles["Normal"])
    doc = SimpleDocTemplate(pdf_path)
    data = [["Station", "State", "pH", "DO", "BOD", "Cluster"]]
    data.extend(records)
    table = Table(
    data,
    colWidths=[250,150,45,45,45,40])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.darkblue),("TEXTCOLOR", (0,0), (-1,0), colors.white),("GRID", (0,0), (-1,-1), 1, colors.black),("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("BOTTOMPADDING", (0,0), (-1,0), 10)
    ]))
    elements = []
    elements.append(title)
    elements.append(date)
    elements.append(Spacer(1,20))
    elements.append(table)
    doc.build(elements)
    messagebox.showinfo(
    "Export Successful",
    f"PDF report has been saved successfully.\n\nLocation:\n{pdf_path}")
    return pdf_path
    
def exportCSV(records):
    csv_path = os.path.join(REPORT_DIR, "Water_Report.csv")
    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Station","State","pH","DO","BOD","Cluster"])
        writer.writerows(records)
        messagebox.showinfo(
        "Export Successful",
        f"CSV report has been saved successfully.\n\nLocation:\n{csv_path}")
    return csv_path