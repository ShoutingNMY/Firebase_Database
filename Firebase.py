import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
from collections import Counter
import matplotlib.pyplot as plt

file_path = "C:/Users/TobiasSlettli/Documents/firebase/Json/gront-bord-as-f9dd7c29cc42.json"
cred = credentials.Certificate(file_path)

firebase_admin.initialize_app(cred)

db = firestore.client()
# Creates name list for users
def UserName():
    user_first_name_dict = {
        "Ada",
        "Alan",
        "Benedict",
        "Ben"
    }
    user_last_name_dict = {
        "Lovelace",
        "Turing",
        "Smith",
        "Johnson"
    }
    return user_last_name_dict, user_first_name_dict
# Creates name list for customers
def CustomerName():
    customer_first_name_dict = {
        "Carol",
        "Chris",
        "Benedict",
        "Daniel",

    }
    customer_last_name_dict = {
        "Jones",
        "Williams",
        "Rodriguez",
        "Brown"
    }
    return customer_last_name_dict, customer_first_name_dict

# sets the lists to a variable
Users_name = UserName()
Customer_name = CustomerName()
jobs = ["Programmer", "Support", "Technician"]
# Creates user accounts for Firebase
def UserCreator():
    for first_name in Users_name[1]:
        for last_name in Users_name[0]:
            doc_ref = db.collection("users").document(f"{last_name + first_name}")
            doc_ref.set({"last": last_name, "first": first_name, "born": random.randint(1980, 2010), "Job": jobs[random.randint(0,2)], "Role": "User"})
# Creates customer accounts for Firebase
def CustomerCreator():
    for first_name in Customer_name[1]:
        for last_name in Customer_name[0]:
            doc_ref = db.collection("customer").document(f"{last_name + first_name}")
            doc_ref.set({"last": last_name, "first": first_name, "born": random.randint(1970,2020), "Role": "Customer"})

CustomerCreator()
UserCreator()
# Creates admin
doc_ref = db.collection("users").document("tslettli")
doc_ref.set({"first": "tobs", "last": "slettli", "born": 2007, "Job": "Admin"})

users_ref = db.collection("users")
docs = users_ref.stream()
born_y = []
job = []
# prints all users
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
    born_y.append(doc.to_dict()['born'])
    job.append(doc.to_dict()["Job"])

customers_ref = db.collection("customer")
docs = customers_ref.stream()
# prints all customers
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

# Counts the amount of each object
count_y = Counter(born_y)
count_j = Counter(job)
jobs.append("Admin")
job_list = []
a = 0
for i in range(len(jobs)):
    job_list.append(count_j[jobs[a]])
    a+=1

born_y.sort()
n_list = []
names_y = []
a = 0
for year in born_y:
    if len(names_y) == 0:
        names_y.append(str(year))
    else:
        if str(year) == names_y[a]:
            continue
        else:
            names_y.append(str(year))
            a+=1

a = 0
# Sets the amount
for i in range(len(count_y)):
    n_list.append(count_y[int(names_y[a])])
    a+=1

# Creates a bar chart
fig, axs = plt.subplots(1,2,figsize=(10,7))

# First bar chart
axs[0].bar(names_y, n_list, 0.5, color="darkblue")
axs[0].set_title("Year of birth amongst co-workers")
axs[0].set_xlabel("Year")
axs[0].set_ylabel("Amount")
axs[0].set_xticks(range(len(names_y)))
axs[0].set_xticklabels(names_y, rotation=-45)

# Second bar chart
axs[1].bar(jobs, job_list, 0.5, color="darkred")
axs[1].set_title("Amount of people within roles")
axs[1].set_xlabel("Role")
axs[1].set_ylabel("Amount")
axs[1].set_xticks(range(len(jobs)))
axs[1].set_xticklabels(jobs, rotation=-45)

plt.tight_layout()
plt.show()
