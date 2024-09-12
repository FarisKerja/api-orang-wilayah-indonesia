import os
# kalo bentuk data raw json
import ijson
import json

def rabbitLoop(locationfolder, source, value, parent, codename, id):
    '''
        - get value target, kalo dia adalah villages, auto break
        - insert dulu valuenya di data source
        - filter terlebih dahulu mana aja yang termasuk datanya
        - insert ke dalam target
        - lakukan looping kembali
    '''
    list = ['provinces', 'regencies', 'districts', 'villages']
    parent_id = [None, 'provinsi_id', 'kabupaten_id', 'kecamatan_id']
    if(source != 'villages'):
        getcurrentposition = list.index(source)
        setname = list[getcurrentposition + 1]
        setparent = parent_id[getcurrentposition + 1]
        seturl = locationfolder + '//raw//' + setname + ".json"
        settarget = locationfolder + '//convert//' + setname + ".csv"
        with open(seturl, 'r', newline='') as childdata:
            parser = ijson.items(childdata, 'item')
            
            for item in parser:
                if(item[setparent]) == id:
                    with open(settarget, 'a', newline='') as setchild:
                        setchild.write(item['full_code'] + "," + str(value) + "," + ((item['type'] + " ") if setname == "regencies" else "") + item['name'] + "\n")
                        if(setname != 'villages'):
                            #print(locationfolder, setname, item['full_code'], item[setparent], item['name'], item['id'])
                            rabbitLoop(locationfolder, setname, item['full_code'], item[setparent], item['name'], item['id'])
        # if(source != 'provinces' and source != 'villages'):
        #     print(locationfolder, source, value, parent, codename, id)
        #     with open(source,'a',newline='') as setwrite:
        #         setwrite.write(str(value) + "," +  parent + "," + codename + "\n")

currentLocation = os.path.dirname(__file__)
seturl = currentLocation + '//raw//' + "provinces" + ".json"
target = currentLocation + '//convert//' + "provinces" + ".csv"
with open(seturl, 'r') as file:
    # Parse the JSON objects one by one
    parser = ijson.items(file, 'item')
    
    # Iterate over the JSON objects
    for item in parser:
        # Process each JSON object as needed
        with open(target,'a',newline='') as setwrite:
            setwrite.write(item['code'] + "," + item['name'] + "\n")
            rabbitLoop(currentLocation, "provinces", item['code'], None, None, item['id'])