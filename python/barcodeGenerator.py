import qrcode
import time
import os
import random
from datamanager import dataManager

# Create barcodes directory if it doesn't exist
os.makedirs("barcodes", exist_ok=True)

def generate_barcode():
    # Data to encode
    mac = "00:1A:2B:3C:4D:5E"
    serial = random.randint(100000, 999999)  # Random serial number
    date = time.strftime("%Y/%m/%d") 
    version = "1.0"
    data = f"{mac},{serial},{date},{version}"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create filename with current date and serial
    current_date = time.strftime("%Y_%m_%d")
    filename = f"barcodes/barcode_{current_date}_{serial}.png"

    # Generate and save the QR code image
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)
    print(f"QR code generated and saved as: {filename}")
    
    # Update the data manager with the new record
    dataManager.append_data(mac, str(serial), date, version)
    return filename, data

if __name__ == "__main__":
    filename, data = generate_barcode()
    print(f"Generated QR code contains: {data}")
