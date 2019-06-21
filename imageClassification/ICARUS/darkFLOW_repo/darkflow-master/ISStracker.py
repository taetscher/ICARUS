import requests

while True:
    iss_info = requests.get('https://api.wheretheiss.at/v1/satellites/25544').content
    with open('Savefiles/ISS_Info.txt', 'a') as logger:
        logger.write(str(iss_info))
    print(iss_info)