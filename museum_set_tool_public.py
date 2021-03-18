apiKey = "YOUR KEY HERE"
import requests
import json
import webbrowser



APIurl_items = 'https://api.torn.com/torn/?selections=items&key=%s'%(apiKey)
APIurl_inventory = 'https://api.torn.com/user/?selections=inventory&key=%s'%(apiKey)
obj_items = json.loads(requests.get(APIurl_items).text)
obj_inventory = json.loads(requests.get(APIurl_inventory).text)
plushie_id = ['186','187','215','258','261','266','268','269','273','274','281','384','618']
flower_id = ['260','263','264','267','271','272','276','277','282','385','617']
price_of_plushie_set = 0
price_of_flower_set = 0
types_of_sets = [plushie_id,flower_id]

#missing function will filter museum sets down to what items you are missing.
def missing(x):
    for i in obj_inventory['inventory']:
            if str(i['ID']) in x:
                x.remove(str(i['ID']))

def lowest_price(x):
    for piece in x:
        APIurl_bazaar = 'https://api.torn.com/market/%s?selections=bazaar&key=%s'%(piece,apiKey)
        obj_bazaar = json.loads(requests.get(APIurl_bazaar).text)
        APIurl_itemmarket = 'https://api.torn.com/market/%s?selections=itemmarket&key=%s'%(piece,apiKey)
        obj_itemmarket = json.loads(requests.get(APIurl_itemmarket).text)
        LP = min(obj_itemmarket['itemmarket'][0]['cost'],obj_bazaar['bazaar'][0]['cost'])
        market_value = obj_items['items'][piece]['market_value']
        if LP > market_value:
            difference = LP - market_value
            print('You are missing a %s. The cheapest one is %s, which is %s higher than market value.'%(obj_items['items'][piece]['name'],LP,difference))
        elif LP == market_value:
            print('You are missing a %s. The cheapest one is %s, which is the same price as market value.'%(obj_items['items'][piece]['name'],LP))
        else:
            difference = market_value - LP
            print('You are missing a %s. The cheapest one is %s, which is %s lower than market value.'%(obj_items['items'][piece]['name'],LP,difference))
    print('\n')    
        
def open_market(x):
    for piece in x:
        item_market_link = "https://www.torn.com/imarket.php#/p=shop&type=" + piece
        webbrowser.open(item_market_link)       

def function(x):
    if x == 'done':
        return
    try:    
        if x == 'plushy':
           missing(types_of_sets[0])
           lowest_price(types_of_sets[0])
           open_market(types_of_sets[0])
        elif x == 'flower':
           missing(types_of_sets[1])
           lowest_price(types_of_sets[1])
           open_market(types_of_sets[1])            
    except:
        print("That doesn't look right, try again.") 
    function(input('Which museum set are you looking for? Please enter plushy or flower. Enter "done" to finish.\n'))

function(input('Which museum set are you looking for? Please enter plushy or flower.\n'))




input("press ENTER to close")