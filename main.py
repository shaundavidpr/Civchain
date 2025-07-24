import time
import requests
import shutil
import os
import qrcode
from blockchain import Blockchain  
from colorama import init, Fore, Style
init(autoreset=True)


def fetch_location():
    try:
        res = requests.get('http://ip-api.com/json/').json()
        lat = res.get("lat")
        lon = res.get("lon")
        city = res.get("city")
        return f"{lat}, {lon} ({city})"
    except:
        return "Unknown"

def save_photo(photo_path, block_index):
    if not os.path.exists("photos"):
        os.makedirs("photos")
    ext = os.path.splitext(photo_path)[1]
    dest_path = f"photos/survivor_{block_index}{ext}"
    try:
        shutil.copy(photo_path, dest_path)
        return dest_path
    except:
        return "Photo not saved"

def generate_qr_code(data, block_index):
    if not os.path.exists("qrcodes"):
        os.makedirs("qrcodes")
    qr = qrcode.make(data)
    qr_path = f"qrcodes/survivor_{block_index}.png"
    qr.save(qr_path)
    return qr_path

def get_survivor_data(block_index):
    print("\nEnter Survivor Details:")
    name = input("Name: ").strip()
    status = input("Status (safe, injured, missing): ").strip().lower()
    notes = input("Additional notes (optional): ").strip()

    # Fetch auto location
    location = fetch_location()
    print(f"Auto-detected location: {location}")

    # Photo input
    photo_path = input("Enter photo file path (or leave blank): ").strip()
    saved_photo = save_photo(photo_path, block_index) if photo_path else "Not provided"

    data = {
        "name": name,
        "location": location,
        "status": status,
        "notes": notes,
        "photo_path": saved_photo,
        "recorded_at": time.ctime()
    }

    # Generate QR with data summary
    qr_data = f"{name} | {status} | {location} | {notes}"
    qr_path = generate_qr_code(qr_data, block_index)
    data["qr_code_path"] = qr_path

    return data

def print_blockchain(chain):
    print("\n=== CivChain Ledger ===")
    for block in chain.chain:
        print(f"\nBlock #{block.index}")
        print(f"Timestamp: {time.ctime(block.timestamp)}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash[:20]}...")
        print(f"Prev: {block.previous_hash[:20]}...")

# --- Main CLI ---

def main():
    civ_chain = Blockchain()
    civ_chain.load_from_file()

    while True:
        print("\n--- CivChain Menu ---")
        print("1. Add survivor entry")
        print("2. View CivChain")
        print("3. Save and exit")
        choice = input("Select an option (1/2/3): ").strip()

        if choice == "1":
            data = get_survivor_data(len(civ_chain.chain))
            civ_chain.add_block(data)
            print("✅ Survivor added to CivChain.")
        elif choice == "2":
            print_blockchain(civ_chain)
        elif choice == "3":
            civ_chain.save_to_file()
            print("💾 CivChain saved to file. Exiting.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
