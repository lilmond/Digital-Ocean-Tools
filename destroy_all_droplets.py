from bs4 import BeautifulSoup
import requests

TOKEN = input("Token: ")
EXCLUDES = []

headers = {
    "Cookie": f"_digitalocean2_session_v4={TOKEN}",
    "X-Csrf-Token": ""
}

def get_csrf_token():
    
    page_content = requests.get("https://cloud.digitalocean.com/droplets", headers=headers, allow_redirects=True).text
    html = BeautifulSoup(page_content, "html.parser").find("meta", {"name": "csrf-token"})

    return html.get("content")

def main():
    droplets_request = requests.get(f"https://cloud.digitalocean.com/api/v1/droplets?page=1&query=&sort=best_match&sort_direction=desc", headers=headers).json()

    if "message" in droplets_request:
        print(f"Error: {droplets_request['message']}")
        exit()

    droplets = droplets_request["droplets"]

    csrf_token = get_csrf_token()

    headers["X-Csrf-Token"] = csrf_token

    for droplet in droplets:
        droplet_id = droplet["id"]
        droplet_name = droplet["name"]
        public_ipv4 = droplet["public_ipv4"]

        if droplet_name in EXCLUDES:
            print(f"Skipping Delete Droplet: {droplet_name} ID: {droplet_id} IPv4: {public_ipv4}")
            continue

        print(f"Deleting Droplet: {droplet_name} ID: {droplet_id} IPv4: {public_ipv4}")

        result = requests.delete(f"https://cloud.digitalocean.com/api/v1/droplets/{droplet_id}", headers=headers)

        if result.status_code == 202:
            print(f"Success!")
        else:
            print(f"Error: {result.text}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
