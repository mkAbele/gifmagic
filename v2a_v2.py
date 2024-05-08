import cv2
import os

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

def remove_directory(directory_path):
    try:
        # Iterate over all the files and subdirectories
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)  # Remove files
            elif os.path.isdir(item_path):
                remove_directory(item_path)  # Recursively remove subdirectories
        os.rmdir(directory_path)  # Remove the directory itself
        print(f"Directory '{directory_path}' and its contents removed successfully.")
    except OSError as e:
        print(f"Error: {directory_path} : {e.strerror}")

def video_to_images(path):
    remove_directory('Images')
    os.mkdir('Images')
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    success, image = video.read()
    counter = 1
    while success:
        cv2.imwrite("Images/Image{0}.jpg".format(str(counter)), image)
        success, image = video.read()
        counter += 1
    return fps, (counter - 1)

def pixelate_image(image, final_width=200):
    height, width = image.shape[:2]
    aspect_ratio = final_width / width
    final_height = int(height * aspect_ratio)
    return cv2.resize(image, (final_width, final_height))

def grayscale_image(image):
    # debug_image_data(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def ascii_conversion(bw_image, ascii_string=[" ", ".", ":", "-", "=", "+", "*", "#", "%", "@", "&"]):
    ascii_image_list = []
    debug_image_data(bw_image)
    for row in bw_image:
        print(row)
        ascii_row = [ascii_string[min(pixel // (256 // len(ascii_string)), len(ascii_string) - 1)] for pixel in row]
        ascii_image_list.append(''.join(ascii_row))
    return ascii_image_list

def get_color(image):
    return cv2.split(image)

def print_ascii(ascii_list, image, color_image, image_pos):
    channels = cv2.split(color_image)
    color_counter = 0
    for row in ascii_list:
        for j, char in enumerate(row):
            # Get color values from each channel
            r, g, b = [int(channel[image_pos // image.shape[1], image_pos % image.shape[1]]) for channel in channels]
            color_hex = '%02x%02x%02x' % (r, g, b)
            print("\x1b[38;2;{}m{}\x1b[0m".format(color_hex, char), end='')
            color_counter += 1
        print()
        
def main(video_path):
    ascii_string = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@", "&"]
    fps, number_images = video_to_images(video_path)

    remove_directory('TextImages')
    os.mkdir('TextImages')

    for i in range(1, number_images + 1):
        image = cv2.imread('Images/Image{0}.jpg'.format(str(i)))
        right_size_image = pixelate_image(image)
        bw_image = grayscale_image(right_size_image)
        converted_list = ascii_conversion(bw_image, ascii_string)
        color_list = get_color(right_size_image)
        print_ascii(converted_list, right_size_image, color_list, i)
        cv2.imwrite('TextImages/Image{0}.jpg'.format(str(i)), right_size_image)

    res = cv2.imread('TextImages/Image1.jpg').shape[:2][::-1]
    video = cv2.VideoWriter('final_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(fps), res)

    for j in range(1, number_images + 1):
        video.write(cv2.imread('TextImages/Image{0}.jpg'.format(str(j))))
    video.release()

main("C1_A.mp4")