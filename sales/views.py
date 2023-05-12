from rest_framework.views import APIView
from rest_framework import status,response
from django.db.models import Count,Sum 

from .serializers import SaleSerializer
from .models import Sale 
import os 

from fpdf import FPDF
from PIL import Image
from matplotlib import pyplot as plt 


pdf = FPDF()
pdf.add_page()


# Create your views here.
class SalesReportAPIView(APIView):
    def get(self,request):
        order_count_by_year=Sale.objects.values('order_date__year').annotate(count=Count('id')).order_by("-order_date__year")
        total_customer=Sale.objects.values("customer_id").distinct() 
        top_3_customer=Sale.objects.values('customer_id',"customer_name").annotate(count=Count('id'),transaction=Sum("sales")).order_by("-transaction")[:3]
        
        customer_transaction_per_year=Sale.objects.values('order_date__year').annotate(transaction=Sum("sales")).order_by("-order_date__year")
        most_selling_sub_cat=Sale.objects.values('sub_category').annotate(count=Count('id')).order_by("-count")
        region_basis=Sale.objects.values('region').annotate(transaction=Sum("sales")).order_by("transaction")

        data={
             "order_count_by_year":order_count_by_year,
             "total_customer":total_customer.count(),
             "top_three_customer":top_3_customer,
             "customer_transaction_per_year":customer_transaction_per_year,
             "most_selling_sub_category":most_selling_sub_cat,
             "region_basis_sales":region_basis
         }
        location=self.preprocess_data(data)
        
        return response.Response({
              "msg":"Open this file on any brower,or click the link",
            "download_url":"http://127.0.0.1:8000/"+location,
           
            },status=status.HTTP_200_OK)
    
    def preprocess_data(self,data):
        #Order Count Per Year:
        order_count_by_year=data["order_count_by_year"]
        count_by_year=[("Year","Order Count")]
        for oc in order_count_by_year:
            count_by_year.append((
                str(oc["order_date__year"]),str(oc["count"])
            ))
        order_count_by_year=count_by_year

          #Top 3 customers who have ordered the most with their total amount of transactions.
        top_three_customer=data["top_three_customer"]
        top3_customer=[("Names","Count","Transaction")]
      
        for t3c in top_three_customer:
            top3_customer.append((
                str(t3c["customer_name"]),str(t3c["count"]),str(float(t3c["transaction"]))
            )) 
        top_three_customer=top3_customer

        #Order Count Per Year:
        customer_transaction_per_year=data["customer_transaction_per_year"]
        temp=customer_transaction_per_year
        transaction_per_year=[("Year","Transaction")]
       
        for ct in customer_transaction_per_year:
            transaction_per_year.append((
                str(ct["order_date__year"]),str(round(float(ct["transaction"]),2))
            ))
        customer_transaction_per_year=transaction_per_year
        
        most_selling_sub_category=data["most_selling_sub_category"]
      
        sub_cat_list=[("Name","Sale Count")]
        for sc in most_selling_sub_category:
            sub_cat_list.append((
                str(sc["sub_category"]),str(sc["count"])
            ))
        most_selling_sub_category=sub_cat_list
        region_basis_sales=data["region_basis_sales"]
        region,sales=[],[]
        for rs in region_basis_sales:
            region.append(str(rs["region"]))
            sales.append(round(float(rs["transaction"]),2))
        
        region_basis_sales={
            "region":region,"sales":sales
        }
        year,sales=[],[]
        for t in temp:
            year.append(t["order_date__year"])
            sales.append(float(t["transaction"]))
        line_chart={"year":year,"sales":sales}
        
        data={
            "order_count_by_year":order_count_by_year,
            "top_three_customer":top_three_customer,
            "customer_transaction_per_year":customer_transaction_per_year,
            "most_selling_sub_category":most_selling_sub_category,
            "region_basis_sales":region_basis_sales,
            "line_chart":line_chart,
            "total_customer":data["total_customer"]
        }

        return self.makepdf(data)
         
    def makepdf(self,data):
        pdf.set_font("Times", size=30)
        pdf.cell(200, 20, txt = "Super Shop Sales Report", align = 'C')
        pdf.set_font("Times", size=16)
        pdf.write_html("<br><br><br><br>")
        title1="Order Count Per Year: "
        title2="Top 3 customers who have ordered the most with their total amount of transactions.:"
        title3="Customer Transactions per Year (from the beginning year to last year) :"
        title4="Most selling items sub-category names :"
        title5=" Region basis sales performance pie chart: "
        title6="Sales performance line chart over the years: "
        
        self.table(title1,data["order_count_by_year"])
        pdf.write_html(f'''
        <br><br>
           <h2> Total Customers  : {data["total_customer"]} </h2>
           <br><br>
        ''')
      
        self.table(title2,data["top_three_customer"])
        self.table(title3,data["customer_transaction_per_year"])
        self.table(title4,data["most_selling_sub_category"])

      

        region_graph=self.make_graph(data["region_basis_sales"],chart_type="pie")
        pdf.write_html("<br><br>")
        pdf.cell(200, 10, txt = title5, align = 'l')
        pdf.write_html("<br><br>") 
        pdf.image(region_graph)
     
        pdf.write_html("<br><br>")
        pdf.cell(200, 10, txt = title6, align = 'l')
        pdf.write_html("<br><br>") 
        graph=self.make_graph(data['line_chart'],chart_type="line")
        pdf.image(graph)
        location="static/sales.pdf"
        
        pdf.output(location)
        
        os.remove(graph)
        os.remove(region_graph)
        return location
      



    def table(self,title,data):
        pdf.write_html("<br><br>")
        pdf.cell(200, 10, txt = title, align = 'l')
        pdf.write_html("<br><br>")
        with pdf.table() as table:
            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

    def make_graph(self,data,chart_type):
        if chart_type=="pie":
           
            region=data["region"]
            sales=data["sales"]
            plt.pie(sales,labels=region,autopct='%1.1f%%')
            location="static/pie_chart.png"
            plt.savefig(location)
            plt.close()
            img=Image.open(location).resize((400,300))
            img.save(location)
        elif chart_type=="line":
         
            year=data["year"]
            sales=data["sales"]
            plt.plot(year,sales) 
            location="static/line_chart.png"
            plt.savefig(location)
            plt.close()
            img=Image.open(location).resize((500,300))
            img.save(location)
        
        return location
        




class SaleAPIView(APIView):
    def get(self,request):
        sales=Sale.objects.all().order_by("-id")
        serializer=SaleSerializer(sales,many=True)
        
        return response.Response({"results":serializer.data},
                                        status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializer=SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"msg":"Your Order created successfully"},
                                        status=status.HTTP_201_CREATED)
        return response.Response({"errors":serializer.errors},
                                     status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk,format=None):
        if Sale.objects.filter(pk=pk).exists():
            sale=Sale.objects.get(pk=pk)
            serializer=SaleSerializer(data=request.data,instance=sale)
            if serializer.is_valid():
                serializer.save()
                return response.Response({"msg":"Your Order updated successfully"},
                                            status=status.HTTP_201_CREATED)
            return response.Response({"errors":serializer.errors},
                                        status=status.HTTP_400_BAD_REQUEST)
    
        return response.Response({"errors":"Order Not found"},
                                     status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        if Sale.objects.filter(pk=pk).exists():
           sale= Sale.objects.get(id=pk)
           sale.delete()
           return response.Response({"msg":"Your Order deleted successfully"},
                                        status=status.HTTP_202_ACCEPTED)

        return response.Response({"errors":"Order Not found"},
                                     status=status.HTTP_400_BAD_REQUEST)