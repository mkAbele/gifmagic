
import cv2

# Open the video file
input_video = cv2.VideoCapture('input_video.mp4')

# Get video properties
fps = input_video.get(cv2.CAP_PROP_FPS)
frame_width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID', 'MJPG', etc.
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

while input_video.isOpened():
    ret, frame = input_video.read()
    if not ret:
        break

    # Perform your frame manipulation here
    # Example: Convert frame to grayscale
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Write the modified frame to the output video
    output_video.write(frame)

# Release resources
input_video.release()
output_video.release()
cv2.destroyAllWindows()