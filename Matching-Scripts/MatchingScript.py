# Import necessary libraries
import pandas as pd
import networkx as net
import firebase_admin
import googlemaps


# Connect to firebase
from firebase_admin import credentials, firestore
cred = credentials.Certificate("Path to JSON file")
firebase_admin.initialize_app(cred)


db = firestore.client()
collection = db.collection('users')
document = collection.get()


# Get all the UIDs
UID = []
for i in document:
    UID.append(i.id)


Donors = []
Receivers = []
Hospitals = []
BloodBanks = []


for uid in UID:
    doc = collection.document(uid)
    res = doc.get().to_dict()
    if res['whoAreYou']=='Hospital':
        # print('Hospital')
        Hospitals.append([uid, res['location']])
    elif res['whoAreYou']=='User':
        if res['userChoice'] == 'Donor':
            Donors.append([uid, res['location'], res['bloodGroup']] )
        if res['userChoice'] == 'Receiver':
            Receivers.append([uid, res['location'],res['bloodGroup']] )
        # print('User')
    else:
        # print('Blood Bank')
        BloodBanks.append([uid, res['location']])


DonorsDF = pd.DataFrame(Donors, columns = ['UID', 'Location', 'BloodGroup'])
ReceiversDF = pd.DataFrame(Receivers, columns = ['UID', 'Location', 'BloodGroup'])
HospitalsDF = pd.DataFrame(Hospitals, columns = ['UID', 'Location'])
BloodBanksDF = pd.DataFrame(BloodBanks, columns = ['UID', 'Location'])


# Get a list of UIDs of donors and receiver concatenated with their blood group to create all the possible edges
from Utils.CSVToList import csvtolist
dons, recs = csvtolist(DonorsDF, ReceiversDF)

# Create edges using Regex
from Utils.Regex import edgecreate
edges = edgecreate(dons, recs)

# Create the graph using networkx
from Utils.InitialGraph import graph
g = graph(dons, recs, edges)

# Get the matching edges using the algorithm from networkx
from Utils.MaxMatch import maxmatch
k = maxmatch(g, dons, recs)
# print(k)


# To Create a weighted graph for distance
new_x = []
new_y = []
distance = []


# Get distance between Donors and Hospitals
for idD,i,_ in Donors:
    for idH,j in Hospitals:
        new_x.append(idD)
        new_y.append(idH)
        gmaps = googlemaps.Client(key='YOUR_API_KEY')
        my_dist = gmaps.distance_matrix(i,j, departure_time = "now")
        if my_dist['rows'][0]['elements'][0]['status']=='OK':
            # print("OK")
            distance.append(my_dist['rows'][0]['elements'][0]['distance']['value'])        


# Get distance between Donors and BloodBanks
for idD,i,_ in Donors:
    for idB,j in BloodBanks:
        new_x.append(idD)
        new_y.append(idB)
        gmaps = googlemaps.Client(key='YOUR_API_KEY')
        my_dist = gmaps.distance_matrix(i,j, departure_time = "now")
        if my_dist['rows'][0]['elements'][0]['status']=='OK':
            # print("OK")
            distance.append(my_dist['rows'][0]['elements'][0]['distance']['value'])   


# Get distance between Receivers and BloodBanks
for idD,i,_ in Receivers:
    for idB,j in BloodBanks:
        new_x.append(idD)
        new_y.append(idB)
        gmaps = googlemaps.Client(key='YOUR_API_KEY')
        my_dist = gmaps.distance_matrix(i,j, departure_time = "now")
        if my_dist['rows'][0]['elements'][0]['status']=='OK':
            # print("OK")
            distance.append(my_dist['rows'][0]['elements'][0]['distance']['value'])   


# Get distance between Receivers and Hospitals
for idD,i,_ in Receivers:
    for idH,j in Hospitals:
        new_x.append(idD)
        new_y.append(idH)
        gmaps = googlemaps.Client(key='YOUR_API_KEY')
        my_dist = gmaps.distance_matrix(i,j, departure_time = "now")
        if my_dist['rows'][0]['elements'][0]['status']=='OK':
            # print("OK")
            distance.append(my_dist['rows'][0]['elements'][0]['distance']['value'])   


# Create the weighted graph with distance as weights
Graph = pd.DataFrame(list(zip(new_x, new_y, distance)), columns =['V1', 'V2', 'distance'])
G=net.from_pandas_edgelist(Graph, 'V1', 'V2', ['distance'])


# Function to find the best hospital or blood bank for donation
def find_hospital_or_blood_bank(reciever,donor):
    subGraphList = [n for n in net.all_neighbors(G,donor)]
    subGraphList.append(reciever)
    subGraphList.append(donor)
    H = G.subgraph(subGraphList)
    result = net.shortest_path(H,reciever,donor,weight='weight')
    return result[1]

# Function to update the database with the found matches
def setMatches(donor, receiver):
    matchedCentre = find_hospital_or_blood_bank(donor, receiver)

    collection.document(receiver).update({
        'matchedCentre': matchedCentre
    })
    collection.document(donor).update({
        'matchedCentre': matchedCentre
    })


    collection.document(receiver).update({
        'matchedUser': donor
    })
    collection.document(donor).update({
        'matchedUser': receiver
    })

    matchedDonation = collection.document(matchedCentre).get().to_dict()
    matchedDonation = matchedDonation['matchedDonation']
    matchedDonation.append({'Donor': donor, 'Receiver': receiver})
    collection.document(matchedCentre).update({'matchedDonation': matchedDonation})

for uid in HospitalsDF['UID']:
    collection.document(uid).update({'matchedDonation': []})

for uid in BloodBanksDF['UID']:
    collection.document(uid).update({'matchedDonation': []})

for i in k:
    setMatches(i[0], i[1])

