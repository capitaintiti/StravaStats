from requests_oauthlib import OAuth2Session

### CREATED BY capitaintiti ###

#Parameters to set before running

# Output
number_kudoers_wanted = 200 # Number of maximum people printed
kudoers_per_line = 3 
number_activity_wanted = 90 # Show over the last N activities

# Set local id, secret, and redirect_url variables
client_id = ''
client_secret = ''
redirect_url = "https://localhost/exchange_token"

### Program

# Create session variable
session = OAuth2Session(client_id=client_id, redirect_uri=redirect_url)

# Set auth url and scope variables
auth_base_url = "https://www.strava.com/oauth/authorize"
session.scope = ["read_all,profile:read_all,activity:read_all"]
auth_link = session.authorization_url(auth_base_url)

# Print auth link and accept input
print(f"Click Here: {auth_link[0]}")
redirect_response = input(f"Paste redirect url here: ")

# Get oauth token
token_url = "https://www.strava.com/api/v3/oauth/token"
session.fetch_token(
    token_url=token_url,
    client_id=client_id,
    client_secret=client_secret,
    authorization_response=redirect_response,
    include_client_id=True
)

# Make request to activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"
request_page_num = 1
param = {'per_page': 200, 'page': request_page_num}
response = session.get(activities_url, params=param)

# Print response
print("\n\n\n")
print(f"Response Status: {response.status_code}")
print(f"Response Reason: {response.reason}")
print(f"Time Elaspsed: {response.elapsed}")
print("\n",'-'*15,"\n")

# Create the id activities list
activities_list = list(response.json())
activites_id_list = []
activites_hidden_id_list = []
for activity in activities_list:
    if activity['private'] == False:
        activites_id_list.append(activity['id'])
    else:
        activites_hidden_id_list.append(activity['id'])

# Retrieve the kudoers
activity_url = "https://www.strava.com/api/v3/activities/"
kudo_count = {}
i = 0
while i < number_activity_wanted:
    id = activites_id_list[i]
    activitiy_kudos_url = "{}/{}/kudos".format(activity_url, id)
    response = session.get(activitiy_kudos_url)
    already_kudoers = kudo_count.keys()
    for json in response.json():
        user_giving_kudo = json['firstname']+" "+json['lastname']
        if user_giving_kudo in already_kudoers:
            kudo_count.update({user_giving_kudo:kudo_count[user_giving_kudo]+1})
        else:
            kudo_count[user_giving_kudo]=1 
    i+=1
    progression = int(i/number_activity_wanted*100)
    left = 100 - int(i/number_activity_wanted*100)
    string = "Progress bar : [" + progression*"#"+left*" "+"]"
    print(string,end='\r')
    

# Podium kudoers building

sorted_kudoers = dict(sorted(kudo_count.items(), key=lambda x:x[1], reverse=True))
print("")
print("\n",'-'*15,"\nSur les " + str(number_activity_wanted) +" dernières activités, voici le top " + str(number_kudoers_wanted) + " de tes supporters : \n")

results = ""
line = ""
rank = 1
for key, value in sorted_kudoers.items():
    if rank > number_kudoers_wanted:
        break
    elif rank%kudoers_per_line == 0:
        results += line+"\n"
        line = ""
    line += str(rank) + "# " + str(key) + " ("+str(value) + " \U0001f44d)    "
    rank += 1

results+=line
print(results)


