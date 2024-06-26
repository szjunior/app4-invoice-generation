import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*.xlsx")

for filepath in filepaths:

    # nr_invoice = filepath[filepath.index("\\") + 1: filepath.find("-")]
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    nr_invoice, date_invoice = filename.split("-")

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr. {nr_invoice}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date {date_invoice}", ln=1)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # add a header
    columns = list(df.columns)
    columns = [item.replace("_", " ").title() for item in columns]
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=25, h=8, txt=columns[0], border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=35, h=8, txt=columns[2], border=1)
    pdf.cell(w=30, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    # add rows to the table
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=25, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=35, h=8, txt=str(row["amount_purchased"]), border=1, align="C")
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1, align="R")
        pdf.cell(w=30, h=8, txt=str(row["total_price"]),border=1, ln=1, align="R")

    # add total row
    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=25, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=35, h=8, txt="", border=1, align="C")
    pdf.cell(w=30, h=8, txt="", border=1, align="R")
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, align="R", ln=1)

    # add total sum sentence
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is {total_sum} euros !", ln=1)

    # add company name and logo
    pdf.set_font(family="Times", size=10)
    pdf.cell(w=30, h=8, txt=f"SCJ Python DevOps")



    pdf.output(f"PDFS/{nr_invoice}.pdf")
