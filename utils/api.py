import socket

def get_api_key_and_auth():
    # Gets public key from spaces and places in correct format
    print("-- No API Key Found --")

    # Gets user to paste in generated token from app
    token = input('Enter provided API key here: ')

    # Writes activation key to file. This key can be used to open up Firehose connection
    f = open("API_KEY.txt", "a")
    f.write(token)
    f.close()
    return token


def get_api_url():
    # work around to get IP address on hosts with non resolvable hostnames
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP_ADRRESS = s.getsockname()[0]
    s.close()
    return 'http://' + str(IP_ADRRESS) + '/update/'