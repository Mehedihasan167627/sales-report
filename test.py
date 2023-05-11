from fpdf import FPDF

# variable pdf
TABLE_DATA = (
    ("Year", "Order Count"),
    ("Jules", "34",),
    ("Mary","45", ),
    ("Carlson", "19"),
    ("Carlson", "19"),
    ("Carlson", "19"),
   
)

DATA=[('Year', 'Order Count'), ('2018', '3258'), ('2017', '2534'), ('2016', '2055'), ('2015', '1953')]

pdf = FPDF()
pdf.add_page()

pdf.set_font("Times", size=30)
pdf.cell(200, 20, txt = "Super Shop Sales Report", align = 'C')

pdf.set_font("Times", size=16)

pdf.write_html("<br><br><br><br>")




title1="Order Count Per Year: "
title2="Top 3 customers who have ordered the most with their total amount of transactions.:"
title3="Customer Transactions per Year (from the beginning year to last year) :"
title4="Most selling items sub-category names :"

def table(title,data):
   pdf.write_html("<br><br>")
   pdf.cell(200, 10, txt = title, align = 'l')
   pdf.write_html("<br><br>")
   with pdf.table() as table:
      for data_row in data:
         row = table.row()
         for datum in data_row:
               row.cell(datum)
               

table(title1,DATA)
table(title2,TABLE_DATA)
table(title3,TABLE_DATA)
table(title4,TABLE_DATA)

pdf.write_html("<br><br>")
pdf.cell(200, 10, txt = "Region basis sales performance pie chart :", align = 'l')
pdf.write_html("<br><br>")
pdf.image("ss.png")
pdf.write_html("<br><br>")
pdf.cell(200, 10, txt = "Sales performance line chart over the years:", align = 'l')
pdf.write_html("<br><br>")
pdf.image("ss.png")

pdf.output("GFG.pdf")  