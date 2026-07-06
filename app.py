from flask import Flask, json, render_template, request, redirect, session, send_file
import io
import datetime
import random


from reportlab.platypus import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet



app = Flask(__name__)

app.secret_key="invoice_secret_key"





# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("index.html")






# ---------------- SUPPLIER ----------------


@app.route("/supplier", methods=["GET","POST"])
def supplier():


    if request.method=="POST":


        session["supplier"]={

            "name":request.form["name"],

            "address":request.form["address"],

            "pin":request.form["pin"],

            "state":request.form["state"],

            "email":request.form.get("email",""),

            "phone":request.form.get("phone","")

        }



        return redirect("/client")



    return render_template("supplier.html")









# ---------------- CLIENT ----------------



@app.route("/client", methods=["GET","POST"])
def client():



    if request.method=="POST":



        session["client"]={


            "name":request.form["name"],

            "address":request.form["address"],

            "pin":request.form["pin"],

            "state":request.form["state"],

            "email":request.form.get("email",""),

            "phone":request.form.get("phone","")


        }




        return redirect("/config")




    return render_template("client.html")









# ---------------- CONFIG ----------------


@app.route("/config",methods=["GET","POST"])
def config():



    if request.method=="POST":



        session["config"]={


            "invoice":

            request.form["invoice"],


            "date":

            request.form["date"],


            "place":

            request.form["place"],


            "gst":

            request.form.get("gst")


        }





        return redirect("/items")




    invoice="INV-"+str(datetime.datetime.now().year)+"-"+str(random.randint(100,999))



    return render_template(
        "config.html",
        invoice=invoice
    )









# ---------------- ITEMS ----------------



@app.route("/items",methods=["GET","POST"])
def items():



    if request.method=="POST":

        import json
        session["items"] = json.loads(request.form["items"])



        return redirect("/preview")



    return render_template("items.html")









# ---------------- PREVIEW ----------------


@app.route("/preview")
def preview():

    supplier = session.get("supplier", {})
    client = session.get("client", {})
    config = session.get("config", {})
    items = session.get("items", [])

    subtotal = 0
    gst = 0

    for item in items:

        amount = item["qty"] * item["price"] - item["discount"]

        subtotal += amount

        gst += amount * item["tax"] / 100

    total = subtotal + gst

    return render_template(
        "preview.html",
        supplier=supplier,
        client=client,
        config=config,
        items=items,
        subtotal=subtotal,
        gst=gst,
        total=total
    )









# ---------------- DOWNLOAD PDF ----------------



@app.route("/download_pdf")
def download_pdf():



    buffer=io.BytesIO()



    pdf=SimpleDocTemplate(

        buffer,

        pagesize=A4

    )



    styles=getSampleStyleSheet()



    elements=[]







    # TITLE


    elements.append(

        Paragraph(

            "<b>TAX INVOICE</b>",

            styles["Title"]

        )

    )



    elements.append(Spacer(1,20))





    config=session.get("config",{})



    elements.append(

        Paragraph(

        f"""

        Invoice #: {config.get('invoice','')} 

        <br/>

        Date: {config.get('date','')}

        """,

        styles["Normal"]

        )

    )




    elements.append(Spacer(1,20))







    supplier=session.get("supplier",{})

    client=session.get("client",{})







    party=[


    [

    Paragraph(

    f"""

    <b>From (Supplier)</b><br/><br/>

    {supplier.get('name','')}<br/>

    {supplier.get('address','')}<br/>

    {supplier.get('state','')} - {supplier.get('pin','')}<br/>

    Email: {supplier.get('email','')}<br/>

    Phone: {supplier.get('phone','')}

    """,

    styles["Normal"]

    ),




    Paragraph(

    f"""

    <b>To (Client)</b><br/><br/>

    {client.get('name','')}<br/>

    {client.get('address','')}<br/>

    {client.get('state','')} - {client.get('pin','')}<br/>

    Email: {client.get('email','')}<br/>

    Phone: {client.get('phone','')}

    """,

    styles["Normal"]

    )



    ]

    ]






    box=Table(

        party,

        colWidths=[250,250]

    )



    box.setStyle(

        TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

        ("GRID",(0,0),(-1,-1),1,colors.grey)

        ])

    )




    elements.append(box)




    elements.append(Spacer(1,20))






    elements.append(

    Paragraph(

    "<b>Place of Supply:</b> "+

    config.get("place",""),

    styles["Normal"]

    )

    )





    elements.append(Spacer(1,20))







    data=[

    [

    "Description",

    "Qty",

    "Price",

    "GST",

    "Total"

    ]

    ]






    total=0




    items=session.get("items",[])





    for item in items:



        # fix string error


        if isinstance(item,dict):

            desc=item.get("description","")

            qty=float(item.get("qty",0))

            price=float(item.get("price",0))



        else:


            parts=item.split(",")



            desc=parts[0]

            qty=float(parts[1])

            price=float(parts[2])






        amount=qty*price


        gst=amount*0.18


        final=amount+gst



        total+=final




        data.append(

        [

        desc,

        qty,

        "₹"+str(amount),

        "18%",

        "₹"+str(final)

        ]

        )






    table=Table(data)




    table.setStyle(

    TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.black),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white)

    ])

    )





    elements.append(table)






    elements.append(Spacer(1,20))





    elements.append(

    Paragraph(

        "<b>Total Amount: ₹"+str(total)+"</b>",

        styles["Heading2"]

    )

    )





    pdf.build(elements)





    buffer.seek(0)



    return send_file(

        buffer,

        download_name="invoice.pdf",

        as_attachment=True

    )











# ---------------- HISTORY ----------------



@app.route("/history")
def history():


    return "Invoice History Page"









if __name__=="__main__":

    app.run(debug=True)