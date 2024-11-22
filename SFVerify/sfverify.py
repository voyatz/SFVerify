import requests, re, time

namespace = "profile-classic1x-us"
locale = "en_US"
region = "us"


def get_config():
    with open('config.txt', 'r') as file:
        lines = file.readlines()
        client_id = None
        client_secret = None

        for line in lines:
            if line.startswith('client_id'):
                client_id = line.split('=')[1].strip()
            elif line.startswith('client_secret'):
                client_secret = line.split('=')[1].strip()
            elif line.startswith('file_path'):
                file_path = line.split('=')[1].strip()

        if not client_id or not client_secret or not file_path:
            raise ValueError("Client ID, Client Secret, or File Path not found in the credentials file.")

        return client_id, client_secret, file_path

#def get_credentials():
#    client_id = input("Enter your Blizzard API Client ID: ").strip()
#    client_secret = input("Enter your Blizzard API Client Secret: ").strip()
#    return client_id, client_secret


def get_access_token(client_id, client_secret):
    url = "https://oauth.battle.net/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    return response.json().get("access_token")

def import_guild_members(file_path):
     with open(file_path, 'r') as file:
        lua_content = file.read()
    
    # Regular expression to match member names before the '-'
        member_names = re.findall(r'"([^"]+)-', lua_content)

        if "doomhowl" in lua_content:
            realm_name = "doomhowl"
        else:
            realm_name = "defias-pillager"
    
        return member_names, realm_name

#This functionality is not working because the Blizzard API call is bugged.
#See more on the issue here: https://us.forums.blizzard.com/en/wow/t/era-guild-and-guild-roster-api-no-longer-works/1969144/29?page=2

#def get_guild_members(access_token, region, realm, guild_name):
#    url = f"https://{region}.api.blizzard.com/data/wow/guild/{realm}/{guild_name}/roster?namespace={namespace}&locale={locale}"
#    headers = {"Authorization": f"Bearer {access_token}"}
#    response = requests.get(url, headers=headers)
#    return response.json()

def is_self_found(access_token, region, realm_slug, character_name, namespace, locale):
    url = f"https://{region}.api.blizzard.com/profile/wow/character/{realm_slug}/{character_name}?namespace={namespace}&locale={locale}"
    headers = {"Authorization": f"Bearer {access_token}"}

    #print(url)
    
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 404:
        #print(f"{character_name} not found (404 error). Skipping.")
        return None

    is_self_found = data.get("is_self_found")
    #print(is_self_found)

    if data.get("level") == 60:
        is_self_found = True

    return is_self_found

#def select_realm():
#    while True:
#        print("Please select a realm:\n1. Defias Pillager\n2. Doomhowl")
#        sel = input("Enter 1 or 2: ")
#        
#        if sel == "1":
#            print("Selection: Defias Pillager")
#            return "defias-pillager"
#            
#        elif sel == "2":
#            print("Selection: Doomhowl")
#            return "doomhowl"
#            
#        else:
#            print("Invalid selection. Please choose 1 or 2.")
    




client_id, client_secret, file_path = get_config()

access_token = get_access_token(client_id, client_secret)

#file_path = input("Enter the filepath to the output of your GuildRosterExporter. This should be located in WTF/Account/ID/SavedVariables: ").strip()

#realm = select_realm()

guild_members, realm = import_guild_members(file_path)

count_missing = 0
count_not_sf = 0
count_sf = 0

missing_members = []
nonsf_members = []

for member in guild_members:
    member_lower = member.lower()
    self_found = is_self_found(access_token, region, realm, member_lower, namespace, locale)
    time.sleep(0.01)

    if self_found is None:
        print(member + "'s data has not been updated in the Blizzard API yet.")
        count_missing += 1
        missing_members.append(member);

    elif not self_found:
        print(member + " is not Self Found!")
        count_not_sf += 1
        nonsf_members.append(member);
    else:
        print(member + " is Self Found!")
        count_sf += 1

print("\n\n\nMembers who are Self Found: " + str(count_sf))

print("Members with missing API data: " + str(count_missing))
print(missing_members)

print("Members who are not Self Found: " + str(count_not_sf))
print(nonsf_members)
    

input("\nPress Enter to exit.")