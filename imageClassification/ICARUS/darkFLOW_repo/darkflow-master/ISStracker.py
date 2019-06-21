import requests

while True:
    iss_info = requests.get('https://api.wheretheiss.at/v1/satellites/25544').content
    with open('Savefiles/ISS_Info.txt', 'a') as logger:
        line = eval(str(iss_info)[2:-1])
        logger.write(str(line) + "\n")
        
        print(line)
        