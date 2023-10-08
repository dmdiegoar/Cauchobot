import pyRofex
import bolsar
contador =0

eco = True
eco = "no"

if eco== True:
    pyRofex._set_environment_parameter("url", "https://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)
    pyRofex._set_environment_parameter("ws", "wss://api.eco.xoms.com.ar/", pyRofex.Environment.LIVE)  

    pyRofex.initialize(user=bolsar.bullu,
                   password=bolsar.bullp,
                   account=bolsar.ecoc,
                   environment=pyRofex.Environment.LIVE)

else:

#######bullll

    pyRofex._set_environment_parameter("url", "https://api.bull.xoms.com.ar/", pyRofex.    Environment.LIVE)
    pyRofex._set_environment_parameter("ws", "wss://api.bull.xoms.com.ar/", pyRofex.Environment.LIVE)  





    pyRofex.initialize(user=bolsar.bullu,
                       password=bolsar.bullp,
                       account=bolsar.bullc,
                       environment=pyRofex.Environment.LIVE)
                   
print("cone rado")

todas = pyRofex.get_all_orders_status()
todastus = todas["status"]
#print(todastus)
ordenes = todas["orders"]

#print(todas)
#for po in ordenes:
    #print(po)
#    contador +=1
 #   print(contador)
    
for order in ordenes:
   if order["instrumentId"]["symbol"]=="MERV - XMEV - AL30 - 24hs" and order["status"] not in ("CANCELLED", "FILLED", "REJECTED"):
       print("####$$$###$$$$##$$")
       print(order["instrumentId"]["symbol"])
       print(order["status"])
       
       print(order)
       print("__________________________")
       
       print("intentando cancelarrr")
       
       
       try:
           cancel_order = pyRofex.cancel_order(order["origClOrdId"])
           print("Cancel Order Response: {0}".format(cancel_order))
       except Exception as e:
            print(e)
            
            print("no")
       print("__________________________")

    # Check cancel order status
#        cancel_order_status = pyRofex.get_order_status(cancel_order["order"]["clientId"])
 #       print("Cancel Order Status Response: {0}".format(cancel_order_status))

    # Check original order status
   #     original_order_status = pyRofex.get_order_status(order["order"]["clientId"])
 #       print("Original Order Status Response: {0}".format(original_order_status))
   
   # if ord["status"]== "FILLED":
    
     #   print(ord)
       # contador +=1
     #   print(contador)
    
    
print("fin")

order_status = pyRofex.get_order_status("435086416044936")

# Print the response
#print("Order Status Response: {0}".format(order_status))

# 5-If order status is PENDING_NEW then we keep checking the status until
# the market accept or reject the order or timeout is reach
timeout = 5 # Time out 5 seconds



