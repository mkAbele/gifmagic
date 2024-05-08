import cv2

# ASCII characters to represent different shades of gray
ASCII_CHARS = '@%#*+=-:. '

def resize_image(image, new_width=100):
    """Resize the image to fit within a certain width while maintaining aspect ratio."""
    (height, width) = image.shape[:2]
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def convert_to_grayscale(image):
    """Convert the image to grayscale."""
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image

def convert_to_ascii(image):
    """Convert the grayscale image to ASCII representation."""
    ascii_str = ''
    for row in image:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // 32]
        ascii_str += '\n'
    return ascii_str

def create_ascii_image(ascii_str, font_size=8):
    """Create an ASCII image using OpenCV."""
    lines = ascii_str.split('\n')
    img_width = len(max(lines, key=len)) * font_size
    img_height = len(lines) * font_size

    # Create a blank white image
    ascii_img = 255 * np.ones((img_height, img_width, 3), np.uint8)

    # Choose a font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Write text to image
    y = font_size
    for line in lines:
        cv2.putText(ascii_img, line, (0, y), font, font_size / 10, (0, 0, 0), 1, cv2.LINE_AA)
        y += font_size

    return ascii_img

def main(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image
    resized_image = resize_image(image)

    # Convert the image to grayscale
    grayscale_image = convert_to_grayscale(resized_image)

    # Convert the grayscale image to ASCII
    ascii_str = convert_to_ascii(grayscale_image)

    # Create the ASCII image using OpenCV
    ascii_img = create_ascii_image(ascii_str)

    # Save the ASCII image
    cv2.imwrite(output_path, ascii_img)

if __name__ == "__main__":
    import numpy as np

    main('Images/Image1.jpg', 'TextImages/Image1.jpg')