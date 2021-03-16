apiKey = "Your Key Here"

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

#grab and combine the price of each individual set piece!
for plushie in plushie_id:
    price_of_plushie_set = obj_items['items'][plushie]['market_value'] + price_of_plushie_set
for flower in flower_id:
    price_of_flower_set = obj_items['items'][flower]['market_value'] + price_of_flower_set
print('Right now, a flower set is worth: $%s'%price_of_flower_set)
print('Right now, a plushie set is worth: $%s'%price_of_plushie_set) 

#this will convert the total plushie/flower set list to be ONLY the ones you are missing from the set!
for i in obj_inventory['inventory']:
    if str(i['ID']) in plushie_id:
        plushie_id.remove(str(i['ID']))
    elif str(i['ID']) in flower_id:
        flower_id.remove(str(i['ID']))

#now that the missing set items are filtered down, we're going to combine them into one variable to 
#make future computations easier
total_missing = flower_id + plushie_id

#tell us what were missing!
print('\n')
if len(total_missing) == 0:
    print('Congratulations, you have a full set!')
else:
    print('As it stands, you are missing these items:')
for i in total_missing:
    print(obj_items['items'][i]['name'])


print('\n')

# open the item market page for each piece that is missing from your set!
for i in total_missing:
     item_market_link = "https://www.torn.com/imarket.php#/p=shop&type=" + i
     webbrowser.open(item_market_link)
 #try to get the lowest price available from bazaar AND item market    
for i in total_missing:

     APIurl_bazaar = 'https://api.torn.com/market/%s?selections=bazaar&key=%s'%(i,apiKey)
     obj_bazaar = json.loads(requests.get(APIurl_bazaar).text)
     APIurl_itemmarket = 'https://api.torn.com/market/%s?selections=itemmarket&key=%s'%(i,apiKey)
     obj_itemmarket = json.loads(requests.get(APIurl_itemmarket).text)
     LP_bazaar = obj_bazaar['bazaar'][0]['cost']
     LP_itemmarket = obj_itemmarket['itemmarket'][0]['cost']
     market_value = obj_items['items'][i]['market_value']

     #we need to have difference results for whether the bazaar price or item market price is lower, 
     #and different results for whether that price is higher or lower than the market value
     
     if LP_bazaar > LP_itemmarket :
        if LP_itemmarket > market_value:
            difference = LP_itemmarket - market_value
            print('The cheapest %s is $%s on the item market, which is $%s higher than market value.' %(obj_items['items'][i]['name'],LP_itemmarket,difference))
        else:
            difference = market_value - LP_itemmarket
            print('The cheapest %s is $%s on the item market, which is $%s lower than market value.' %(obj_items['items'][i]['name'],LP_itemmarket,difference))
     else:
        if LP_bazaar > market_value:
            difference =  LP_bazaar - market_value
            print('The cheapest %s is $%s in a bazaar, which is $%s higher than market value.' %(obj_items['items'][i]['name'],LP_bazaar,difference))
        else:
            difference = market_value - LP_bazaar
            print('The cheapest %s is $%s in a bazaar, which is $%s lower than market value.' %(obj_items['items'][i]['name'],LP_bazaar,difference)) 

            
print('\n')     
input("press ENTER to continue")