from bs4 import BeautifulSoup
import requests

TOKEN = input("Token: ")
EXCLUDES = []

headers = {
    "Cookie": f"_digitalocean2_session_v4={TOKEN}"
}

def main():
    droplets_request = requests.get(f"https://cloud.digitalocean.com/api/v1/droplets?page=1&query=&sort=best_match&sort_direction=desc", headers=headers).json()

    if "message" in droplets_request:
        print(f"Error: {droplets_request['message']}")
        exit()

    droplets = droplets_request["droplets"]


    for droplet in droplets:
        droplet_id = droplet["id"]
        droplet_name = droplet["name"]
        public_ipv4 = droplet["public_ipv4"]

        print(f"{droplet_name} {public_ipv4}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
