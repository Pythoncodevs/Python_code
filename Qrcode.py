import qrcode

def generate_qr_code(url, save_path):
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,  # QR code size: 1 is the smallest, 40 is the largest
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Border thickness
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Convert QR code into an image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    img.save(save_path)
    print(f"QR code successfully saved to {save_path}")

# Example usage
url = 'https://example.com'
save_path = 'qr_code.png'
generate_qr_code(url, save_path)