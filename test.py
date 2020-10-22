import requests
import json
import statistics as stat
import cv2

url_item = 'https://www.pathofexile.com/api/trade/search/Heist'
url_currency = 'https://www.pathofexile.com/api/trade/exchange/Heist'
url_get = 'https://www.pathofexile.com/api/trade/fetch/'

def get_exa_value():
    return get_currency_price("exa")

def get_item_price(item, itype, head = 10):
    myobj = {
       "query": {
            "status": {"option": "online"},
            "name": item,
            "type": itype,
            "stats": [{
                "type": "and",
                "filters": []
            }]
        },
        "sort": {
            "price": "asc"
        },
        # "filters":{"trade_filters":{"filters":{"price":{"option":currency}}}}
    }    
    respond = requests.post(url_item, json = myobj)
    respond = json.loads(respond.text)
    respond_id = respond["id"]
    #ignore first 2 listing
    respond_result = respond["result"][2:head+2]

    myobj = ",".join(respond_result)
    url_get_item = url_get + '%s?query=%s'%(myobj,respond_id)
    respond = requests.get(url_get_item)
    respond = json.loads(respond.text)

    respond_result = respond["result"]
    price_catalog = []
    for x in respond_result:
        listing = x["listing"]
        price = listing["price"]
        if price["currency"] == "exalted":
            price_catalog.append(price["amount"]*exa_value)
        else:
            price_catalog.append(price["amount"])

    price = round((stat.mean(price_catalog)+stat.median(price_catalog))/2, 2)
    return price 

def get_currency_price(want, have='chaos', head = 10):
    myobj = {
        "exchange": {
            "want": [want],
            "have": [have],
            "status": "online"
        }
    }    
    respond = requests.post(url_currency, json = myobj)
    respond = json.loads(respond.text)
    respond_id = respond["id"]
    #ignore first 2 listing
    respond_result = respond["result"][2:head+2]

    myobj = ",".join(respond_result)
    url_get_item = url_get + '%s?query=%s'%(myobj,respond_id)
    respond = requests.get(url_get_item)
    respond = json.loads(respond.text)

    respond_result = respond["result"]
    price_catalog = []
    for x in respond_result:
        listing = x["listing"]
        price = listing["price"]
        price_catalog.append(price["amount"])
    price = round((stat.mean(price_catalog)+stat.median(price_catalog))/2, 2)
    return price 

if __name__ == "__main__":
    exa_value = get_exa_value()
    price_list = {}
    fragment_catalog = [
        "hydra","phoenix","minot","chimer",
        "fragment-of-enslavement","fragment-of-eradication","fragment-of-constriction","fragment-of-purification",
        "fragment-of-terror","fragment-of-emptiness","fragment-of-shape","fragment-of-knowledge"]
    delirium_catalog = ["fine-delirium-orb","singular-delirium-orb","thaumaturges-delirium-orb","blacksmiths-delirium-orb","armoursmiths-delirium-orb","cartographers-delirium-orb","jewellers-delirium-orb","abyssal-delirium-orb","decadent-delirium-orb","foreboding-delirium-orb","obscured-delirium-orb","whispering-delirium-orb","fragmented-delirium-orb","skittering-delirium-orb","fossilised-delirium-orb","portentous-delirium-orb","amorphous-delirium-orb","blighted-delirium-orb","timeless-delirium-orb","imperial-delirium-orb","primal-delirium-orb","diviners-delirium-orb"]
    catalyst_catalog = ["turbulent-catalyst","imbued-catalyst","abrasive-catalyst","tempering-catalyst","fertile-catalyst","prismatic-catalyst","intrinsic-catalyst"]
    scarab_catalog = ["gilded-metamorph-scarab","polished-metamorph-scarab","gilded-legion-scarab","polished-legion-scarab","gilded-perandus-scarab","polished-perandus-scarab","gilded-harbinger-scarab","polished-harbinger-scarab","gilded-sulphite-scarab","polished-sulphite-scarab","polished-bestiary-scarab","gilded-bestiary-scarab","gilded-ambush-scarab","polished-ambush-scarab","polished-elder-scarab","gilded-elder-scarab","gilded-reliquary-scarab","polished-reliquary-scarab","gilded-cartography-scarab","polished-cartography-scarab","polished-torment-scarab","gilded-torment-scarab","gilded-shaper-scarab","polished-shaper-scarab","gilded-breach-scarab","polished-breach-scarab","polished-divination-scarab","gilded-divination-scarab"]
    fossil_catalog = ["scorched-fossil","frigid-fossil","metallic-fossil","jagged-fossil","encrusted-fossil","aberrant-fossil","faceted-fossil","pristine-fossil","bloodstained-fossil","dense-fossil","hollow-fossil","corroded-fossil","fractured-fossil","prismatic-fossil","glyphic-fossil","aetheric-fossil","serrated-fossil","tangled-fossil","sanctified-fossil","lucent-fossil","gilded-fossil","shuddering-fossil","bound-fossil","perfect-fossil","enchanted-fossil"]
    # essence_catalog = ["deafening-essence-of-hatred","deafening-essence-of-woe","deafening-essence-of-greed","deafening-essence-of-contempt","deafening-essence-of-sorrow","deafening-essence-of-anger","deafening-essence-of-torment","deafening-essence-of-rage","deafening-essence-of-suffering","deafening-essence-of-fear","deafening-essence-of-wrath","deafening-essence-of-doubt","deafening-essence-of-anguish","deafening-essence-of-loathing","deafening-essence-of-spite","deafening-essence-of-zeal","deafening-essence-of-misery","deafening-essence-of-dread","deafening-essence-of-scorn","deafening-essence-of-envy","essence-of-hysteria","essence-of-insanity","essence-of-horror","essence-of-delirium"]
    for item in fragment_catalog:
        price_list[item] = get_currency_price(item)
        print(item)
    for item in delirium_catalog:
        price_list[item] = get_currency_price(item)
        print(item)
    for item in scarab_catalog:
        price_list[item] = get_currency_price(item)
        print(item)
    for item in catalyst_catalog:
        price_list[item] = get_currency_price(item)
        print(item)
    for item in fossil_catalog:
        price_list[item] = get_currency_price(item)
        print(item)

        # print("%s:  %s"%(item, get_currency_price(item)))
    # print(price_list['hydra'])

    img = cv2.imread('/home/natsu/poe/' + 'stash.jpg', 1)
    img2 = cv2.imread('/home/natsu/poe/' + 'stash2.jpg', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    ##Fossil
    cv2.putText(img2, str(price_list.get('jagged-fossil')), (89,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('dense-fossil')), (161,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('frigid-fossil')), (235,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('aberrant-fossil')), (309,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('scorched-fossil')), (383,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('metallic-fossil')), (459,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('pristine-fossil')), (530,74), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img2, str(price_list.get('bound-fossil')), (13,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('corroded-fossil')), (89,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('perfect-fossil')), (161,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('prismatic-fossil')), (235,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('enchanted-fossil')), (309,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('aetheric-fossil')), (383,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('lucent-fossil')), (459,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('serrated-fossil')), (530,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('shuddering-fossil')), (606,148), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
    cv2.putText(img2, str(price_list.get('tangled-fossil')), (48,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('bloodstained-fossil')), (124,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('gilded-fossil')), (235,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('encrusted-fossil')), (309,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('sanctified-fossil')), (383,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)    
    cv2.putText(img2, str(price_list.get('hollow-fossil')), (494,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('fractured-fossil')), (566,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img2, str(price_list.get('faceted-fossil')), (533,297), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('glyphic-fossil')), (87,297), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    ##Caty
    cv2.putText(img2, str(price_list.get('turbulent-catalystl')), (48,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('imbued-catalyst')), (124,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('abrasive-catalyst')), (235,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('tempering-catalyst')), (309,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('fertile-catalyst')), (383,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)    
    cv2.putText(img2, str(price_list.get('prismatic-catalyst')), (494,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img2, str(price_list.get('intrinsic-catalyst')), (566,221), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    ## Fragment
    cv2.putText(img, str(price_list.get('hydra')), (679,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('phoenix')), (741,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('minot')), (679,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('chimer')), (741,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('fragment-of-enslavement')), (17,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-eradication')), (82,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-constriction')), (17,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-purification')), (82,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('fragment-of-terror')), (539,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-emptiness')), (603,73), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-shape')), (539,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragment-of-knowledge')), (603,130), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    ## Scarab
    #col 1
    cv2.putText(img, str(price_list.get('polished-bestiary-scarab')), (81,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-bestiary-scarab')), (147,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-reliquary-scarab')), (81,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-reliquary-scarab')), (147,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-torment-scarab')), (81,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-torment-scarab')), (147,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-sulphite-scarab')), (81,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-sulphite-scarab')), (147,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA) 
    #col 2
    cv2.putText(img, str(price_list.get('polished-metamorph-scarab')), (312,75), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-metamorph-scarab')), (375,75), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-legion-scarab')), (312,140), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-legion-scarab')), (375,140), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-ambush-scarab')), (312,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-ambush-scarab')), (375,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-shaper-scarab')), (312,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-shaper-scarab')), (375,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-perandus-scarab')), (312,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-perandus-scarab')), (375,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-cartography-scarab')), (312,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-cartography-scarab')), (375,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    #col 3
    cv2.putText(img, str(price_list.get('polished-harbinger-scarab')), (539,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-harbinger-scarab')), (603,207), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-elder-scarab')), (539,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-elder-scarab')), (603,275), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-divination-scarab')), (539,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-divination-scarab')), (603,339), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('polished-breach-scarab')), (539,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('gilded-breach-scarab')), (603,409), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    ##Delirium
    cv2.putText(img, str(price_list.get('decadent-delirium-orb')), (5,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('cartographers-delirium-orb')), (86,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('blighted-delirium-orb')), (167,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('blacksmiths-delirium-orb')), (248,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('armoursmiths-delirium-orb')), (329,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('singular-delirium-orb')), (411,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('primal-delirium-orb')), (492,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    # cv2.putText(img, str(price_list.get('delirium-orb')), (572,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('jewellers-delirium-orb')), (654,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('imperial-delirium-orb')), (737,492), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('fossilised-delirium-orb')), (5,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('foreboding-delirium-orb')), (86,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fine-delirium-orb')), (167,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('diviners-delirium-orb')), (248,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('portentous-delirium-orb')), (329,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('skittering-delirium-orb')), (411,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('timeless-delirium-orb')), (492,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('thaumaturges-delirium-orb')), (572,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('obscured-delirium-orb')), (654,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('fragmented-delirium-orb')), (737,574), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.putText(img, str(price_list.get('abyssal-delirium-orb')), (704,238), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('amorphous-delirium-orb')), (704,319), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, str(price_list.get('whispering-delirium-orb')), (704,395), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite('/home/natsu/poe/' + 'final.png', img)
    cv2.imwrite('/home/natsu/poe/' + 'final2.png', img)