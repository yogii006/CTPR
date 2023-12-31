import streamlit as st
from PIL import Image
#from cv2 import cv2
from PIL import Image
from PIL import Image, ImageFilter
import numpy as np
import imagehash
from imagehash import phash
from PIL import Image, ImageOps, ImageFilter
def hamming_distance(bin_str1, bin_str2):
    """
    Calculates the Hamming distance between two binary strings
    """
    assert len(bin_str1) == len(bin_str2), "Binary strings must have the same length"
    dist = 0
    for i in range(len(bin_str1)):
        if bin_str1[i] != bin_str2[i]:
            dist += 1
    return dist
def segment_image(image):
    # Convert the image to grayscale
    gray_image = (image)

    # Convert the grayscale image to a NumPy array
    gray_array = np.array(gray_image)

    # Reshape the array to a single column
    reshaped_array = gray_array.reshape(-1, 1)

    # Apply K-means clustering for segmentation
    k = 2  # Number of clusters (background and foreground)
    kmeans_centers = np.array([0, 255]).reshape((-1, 1))
    kmeans_labels = np.argmin(np.abs(reshaped_array - kmeans_centers.T), axis=1)
    segmented_array = kmeans_centers[kmeans_labels].reshape(gray_array.shape)

    # Convert the segmented array back to an image
    segmented_image = Image.fromarray(segmented_array.astype(np.uint8))

    return segmented_image
st.title("Image Editing app")
default_option = "Image options"
options = ["Image options", "Similarity"]
option_chosen = st.selectbox("Select an object", options, index=options.index(default_option))
if option_chosen == "Image options":
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_image is not None:
        default_value = "Original"
        choices = ["Grayscale", "Blur", "Original", "Segment","Rotate"]

        selected = st.selectbox("Select an option", choices, index=choices.index(default_value))
        col4, col5 = st.columns(2)



        


        
        if selected == "Blur":
            blur_intensity = st.slider("Blur Intensity", 0, 50, 0)
        if selected == "Rotate":
            rotation_angle = st.slider("Rotation Angle", -180, 180, 0)

        with col4:
            image = Image.open(uploaded_image)
            st.image(image, caption="Original Image", use_column_width=True)

        with col5:

            if selected == "Original":
                st.image(image, caption="Original Image", use_column_width=True)
            if selected == "Grayscale":
                # image1 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
                # st.image(image1, caption="Grayscale Image", use_column_width=True)

                img_array = np.array(image)
                # Compute the grayscale value of each pixel
                gray_array = np.mean(img_array, axis=2)

                # Replace the RGB values of each pixel with the grayscale value
                gray_array = np.dstack([gray_array]*3)

                # Convert the numpy array back to a PIL image
                gray_img = Image.fromarray(np.uint8(gray_array))

                # Display the resulting grayscale image using Streamlit
                st.image(gray_img, caption='Grayscale Image', use_column_width=True)


            
            if selected == "Blur":

                # Apply the blur effect based on the slider value
                blurred_img = image.filter(ImageFilter.GaussianBlur(blur_intensity))
                st.image(blurred_img, caption=f'Blurred Image (Intensity: {blur_intensity})', use_column_width=True)
            if selected == "Rotate":
                rotated_img = image.rotate(rotation_angle)
                st.image(rotated_img, caption=f'Rotated Image (Angle: {rotation_angle} degrees)', use_column_width=True)


            if selected == "Segment":
                segmented_image = segment_image(image)

                # Display original and segmented images
                st.image(segmented_image, caption='Segmented Image', width=300)
            #     img_array = np.array(image)

            #     # Perform image segmentation
            #     gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            #     ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #     # Draw the contours on the image
            #     img_contours = cv2.drawContours(img_array, contours, -1, (0, 255, 0), 3)
            #     # Display the segmented image
                # st.image(seg_image, caption='Segmented Image', use_column_width=True)

if option_chosen == "Similarity":
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image1 = st.file_uploader("Choose an image2...", type=["jpg", "png"])

    with col2:
        uploaded_image2 = st.file_uploader("Choose an image3...", type=["jpg", "png"])

    if uploaded_image1 and uploaded_image1 is not None:
        col3, col4 = st.columns(2)
        with col3:
            st.image(uploaded_image1, caption="First Image", use_column_width=True)
        with col4:
            st.image(uploaded_image2, caption="Second Image", use_column_width=True)

        image2 = Image.open(uploaded_image1)
        hex_value1 = f'''{phash(image2)}'''
        int_value1 = int(hex_value1, base=16)
        bin_value1 = bin(int_value1)

        image3 = Image.open(uploaded_image2)
        hex_value2 = f'''{phash(image3)}'''
        int_value2 = int(hex_value2, base=16)
        bin_value2 = bin(int_value2)
        dist = hamming_distance(bin_value1, bin_value2)
        st.write("Calculations")
        st.write(f"binary hash code of image1 is {bin_value1}")
        st.write(f"binary hash code of image2 is {bin_value2}")
        st.write(f"hamming distance  {dist}")
        st.write(f"percentage matching of these two images is {((56 -dist) / 56 * 100)}%")
