import cv2
import numpy as np
import imageio

# ASCII characters to represent different shades of gray
ASCII_CHARS = ' IDritVaiKociņ'

def v2i(video, path):
    # Open the video file
    cap = cv2.VideoCapture(video)

    # Initialize a counter for image filenames
    count = 0

    # Loop through the video frames
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if frame is successfully read
        if not ret:
            break

        # Save the frame as an image
        image_path = f'image_{count:04d}.jpg'
        cv2.imwrite(path+image_path, frame)

        # Increment counter
        count += 1

    # Release the video capture object
    cap.release()

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


def create_ascii_image(srcimg, outputimg, font_size=8):
    """Create an ASCII image using OpenCV."""
    grayscale_image = cv2.cvtColor(srcimg, cv2.COLOR_BGR2GRAY)

    # lines = ascii_str.split('\n')

    #img_width = len(max(lines, key=len)) * font_size
    #img_height = len(lines) * font_size
    height, width = srcimg.shape[:2]
    stepX = int(width / (font_size*2))
    stepY = int(height / (font_size*2))
    # print(stepX*(font_size*2))
    # print(stepY*(font_size*2))

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
    # x = font_size * 2
    # cv2.putText(ascii_img, "F", (0, x), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "U", (8, 8), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "C", (0, 16), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)
    # cv2.putText(ascii_img, "K", (8, 16), font, font_size / 10, (255, 255, 255), 1, cv2.LINE_AA)

    for x in range(0, stepX):
        for y in range(0, stepY):
            spaceing = (font_size*2)
            pxX = x * spaceing
            pxY = y * spaceing

            x1, y1 = (pxX),(pxY)
            x2, y2 = (pxX + spaceing),(pxY + spaceing)

            # print("-------")
            # print(str(x1)+" / "+str(y1))
            # print(str(x2)+" / "+str(y2))
            averageLuma =  np.round(np.mean(grayscale_image[y1:y2, x1:x2], axis=(0, 1))).astype(int)
            average_color =  np.clip(np.round(np.mean(srcimg[y1:y2, x1:x2], axis=(0, 1))).astype(int), 0, 255)
            # print("Average color (R, G, B):", average_color[0])
            # print(ASCII_CHARS[average_color // 32])
            # print("-------")
            cv2.putText(outputimg, ASCII_CHARS[averageLuma // 32], (x*(font_size*2), y*(font_size*2)), font, font_size / 10, (int(average_color[0]),int(average_color[1]),int(average_color[2])), 1, cv2.LINE_AA)
            # debug_image_data(grayscale_image[y1:y2, x1:x2])

    
    #debug_image_data(outputimg)

    return outputimg

def main(image_path, output_path):

    # Open the video file
    video_path = 'C2_A.mp4'
    cap = cv2.VideoCapture(video_path)

    # Initialize a list to store frames
    frames = []

    # Loop through the video frames
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if frame is successfully read
        if not ret:
            break

        blank_image = np.ones((800, 800, 3), np.uint8) * 0
        ascii_img = create_ascii_image(frame, blank_image, 4)
        #debug_image_data(ascii_img)

        # Convert the frame to RGB (imageio requires RGB format)
        frame_rgb = cv2.cvtColor(ascii_img, cv2.COLOR_BGR2RGB)

        # Append the frame to the list
        frames.append(frame_rgb)

    # Release the video capture object
    cap.release()

    # Save the frames as a GIF using imageio
    gif_path = 'C2_A_4.gif'
    imageio.mimsave(gif_path, frames, fps=12)

    # #Create new blank image
    # blank_image = np.ones((500, 500, 3), np.uint8) * 0

    # # Load the image
    # image = cv2.imread(image_path)

    # ascii_img = create_ascii_image(image, blank_image, 4)

    return 0

    # Save the ASCII image
    # cv2.imwrite(output_path, ascii_img)

if __name__ == "__main__":

    main('Images/Image1.jpg', 'TextImages/Image1.jpg')