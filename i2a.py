import cv2
import numpy as np

# ASCII characters to represent different shades of gray
ASCII_CHARS = ' FUCKTHIS'

def debug_image_data(image):
    try:
        # Read the image
        #image = cv2.imread(image_path)
        
        # Check if image is loaded successfully
        if image is None:
            print("Error: Unable to load image.")
            return
        
        # Perform some operations (e.g., resizing, converting to grayscale)
        # Example operations:
        # resized_image = cv2.resize(image, (new_width, new_height))
        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Display the original image
        cv2.imshow("Original Image", image)
        
        # Display the result (e.g., resized image, grayscale image)
        # cv2.imshow("Resized Image", resized_image)
        # cv2.imshow("Grayscale Image", gray_image)
        
        # Wait for a key press and close the window when any key is pressed
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {e}")


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

def create_ascii_image(srcimg, ascii_str, font_size=8):
    """Create an ASCII image using OpenCV."""
    lines = ascii_str.split('\n')

    #img_width = len(max(lines, key=len)) * font_size
    #img_height = len(lines) * font_size
    height, width = srcimg.shape[:2]
    stepX = int(width / font_size)
    stepY = int(height / font_size)

    # Create a blank white image
    # ascii_img = 255 * np.ones((height, width, 3), np.uint8)
    ascii_img = srcimg

    # Choose a font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Write text to image
    # y = font_size
    # for line in lines:
    #     cv2.putText(ascii_img, line, (0, y), font, font_size / 10, (0, 0, 0), 1, cv2.LINE_AA)
    #     y += font_size
    # cv2.putText(ascii_img, "F", (0, 8), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "U", (8, 8), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "C", (0, 16), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "K", (8, 16), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    for x in range(0, stepX):
        cv2.putText(ascii_img, "F", (x, 8), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)


    debug_image_data(ascii_img)

    return ascii_img

def main(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    #debug_image_data(image)

    # Resize the image
    resized_image = resize_image(image, 500)
    # debug_image_data(resized_image)

    # Convert the image to grayscale
    grayscale_image = convert_to_grayscale(resized_image)

    # Convert the grayscale image to ASCII
    ascii_str = convert_to_ascii(grayscale_image)
    #print(ascii_str)
    # Create the ASCII image using OpenCV

    ascii_img = create_ascii_image(resized_image, ascii_str, 4)
    #debug_image_data(ascii_img)

    return 0

    # Save the ASCII image
    # cv2.imwrite(output_path, ascii_img)

if __name__ == "__main__":

    main('Images/Image1.jpg', 'TextImages/Image1.jpg')