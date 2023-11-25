import pyRofex




def todas_las_ordenes():
    todas = pyRofex.get_all_orders_status()
    #print(todas)
    #todastus = todas["status"]
    #print(todastus)
    ordenes = todas["orders"]
    return ordenes

def cancelar_todo():
    #consulto todas las ordenes
    ordenes = todas_las_ordenes()
    print("cancelando todo")
    
    for order in ordenes:
        if order["status"] not in ("CANCELLED", "FILLED", "REJECTED"):
            print("####$$$###$$$$##$$")
            print(order["instrumentId"]["symbol"])
            print(order["status"])

            print(order)
            print("__________________________")
       
            print("intentando cancelarrr")
       
       
            try:
                cancel_order = pyRofex.cancel_order(order["clOrdId"])
                print("Cancel Order Response: {0}".format(cancel_order))
                print("####$$$###$$$$##$$")
                print(order["instrumentId"]["symbol"])
                print(order["status"])

            except Exception as e:
                    print(e)
                    
                    print("no se pudo cancelar")
            print("__________________________")




def cancelar_lado(lado ="SELL" ):
    ellado=(lado,)
    #consulto todas las ordenes
    ordenes = todas_las_ordenes()
    print("cancelando ordenes de   " + str(ellado))
    for order in ordenes:
        if order["status"] not in ("CANCELLED", "FILLED", "REJECTED") and order['side'] in ellado:
            print("####$$$###$$$$##$$")
            print(order["instrumentId"]["symbol"])
            print(order["status"])

            print(order)
            print("__________________________")
       
            print("intentando cancelarrr")
       
       
            try:
                cancel_order = pyRofex.cancel_order(order["clOrdId"])
                print("Cancel Order Response: {0}".format(cancel_order))
                print("####$$$###$$$$##$$")
                print(order["instrumentId"]["symbol"])
                print(order["status"])

            except Exception as e:
                    print(e)
                    
                    print("no se pudo cancelar")
            print("__________________________")


    
def cancelar_papel(papel = "alito" ):
    papeles = (papel,)
    #consulto todas las ordenes
    ordenes = todas_las_ordenes()
    print("cancelando ordenes de   " + str(papeles))
    for order in ordenes:
        if order["status"] not in ("CANCELLED", "FILLED", "REJECTED") and order['symbol'] in papeles:
            print("####$$$###$$$$##$$")
            print(order["instrumentId"]["symbol"])
            print(order["status"])

            print(order)
            print("__________________________")
       
            print("intentando cancelarrr")
       
       
            try:
                cancel_order = pyRofex.cancel_order(order["clOrdId"])
                print("Cancel Order Response: {0}".format(cancel_order))
                print("####$$$###$$$$##$$")
                print(order["instrumentId"]["symbol"])
                print(order["status"])

            except Exception as e:
                    print(e)
                    
                    print("no se pudo cancelar")
            print("__________________________")