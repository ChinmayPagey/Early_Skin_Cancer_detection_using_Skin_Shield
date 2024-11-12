import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import time

st.set_page_config(
    page_title="Skin Lesion Detection",
    page_icon="🔬",
    layout="wide"
)

st.markdown("""
   <style>
    .stApp { 
        max-width: 1200px; 
        margin: 0 auto; 
    }
    .welcome-page { 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        height: 100vh; 
        background-color: #0e1118;
        color: #fff;
        text-align: center;
    }
    .welcome-text { 
        font-size: 48px; 
        font-weight: bold; 
        margin-bottom: 20px; 
        animation: slideUpDown 5s ease-in-out infinite; /* Slower animation */
    }
    .sub-text { 
        font-size: 24px; 
        font-weight: 500; 
        color: #00bcd4;
    }
    @keyframes slideUpDown { 
        0% { transform: translateY(-30px); } 
        50% { transform: translateY(0); } 
        100% { transform: translateY(-30px); } 
    }
</style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_lesion_model():
    try:
        model = load_model('skin_lesion_main_model.h5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def preprocess_image(img):
    # Resize image to 133x133
    img = img.resize((133, 133))
    # Convert to array and preprocess
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize
    return img_array

def main():
    # Load model
    model = load_lesion_model()
    if model is None:
        st.error("Failed to load the model. Please check if the model file exists.")
        return

    # Welcome page
    st.markdown("""
    <div class="welcome-page">
        <div class="welcome-text">Welcome to Skin Shield, your partner in early skin cancer detection!</div>
        <div class="sub-text">Early Detection at your fingertips!</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)

    st.title("Skin Lesion Detection")
    st.markdown("""
    Upload an image of a skin lesion for analysis. 
    The system will classify it as either benign or malignant.
    """)

    st.markdown('<div class="upload-prompt">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of the skin lesion. Supported formats: PNG, JPG, JPEG"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    show_doctors_section = False  # Variable to control doctor display

    if uploaded_file is not None:
        try:
            # Create columns for image and prediction
            col1, col2 = st.columns(2)
            
            # Display original image
            with col1:
                st.subheader("Uploaded Image")
                image_bytes = uploaded_file.getvalue()
                original_image = Image.open(io.BytesIO(image_bytes))
                st.image(original_image, use_column_width=True)

            # Process image and make prediction
            with col2:
                st.subheader("Analysis")
                with st.spinner('Analyzing image...'):
                    # Preprocess image
                    preprocessed_img = preprocess_image(original_image)
                    # Make prediction
                    prediction = model.predict(preprocessed_img)
                    prediction_value = float(prediction[0][0])
                    # Calculate confidence
                    confidence = abs(prediction_value - 0.5) * 200
                    # Determine result
                    result = "Malignant" if prediction_value < 0.0000003 else "Benign"
                    
                    # Display prediction with appropriate styling
                    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                    
                    # Show result with color coding
                    result_color = "red" if result == "Malignant" else "green"
                    st.markdown(f"<h3 style='color: {result_color}; text-align: center;'>{result}</h3>", 
                                unsafe_allow_html=True)
                    
                    # Show confidence
                    
                    #st.markdown(f"""
                        #<p style='text-align: center; font-size: 18px;'>
                        #Predicted value: {prediction_value}
                        #</p>
                        #""", 
                        #unsafe_allow_html=True)
                    
                    
                    
                    if result=="Benign":
                        st.subheader("Your mole has been classified as benign, which is great news! Here is our advise: ")
                        st.write("**Step 1:-  it's essential to remember that skin cancer can be caused by various factors, including UV radiation, genetic predisposition, and other environmental factors")
                        st.write("**Step 2:- Please schedule a follow-up appointment with your primary care physician or dermatologist within 6-12 months for another examination.")
                        st.write("**Step 3:- Remember to continue monitoring your mole and report any changes to your doctor.")
                        st.write("We encourage you to take advantage of the knowledge and resources we've provided. Learn more about skin cancer risks, prevention strategies, and early detection techniques. By being informed and proactive, you're better equipped to protect your skin health.")
                    # If malignant, show consult option
                    if result == "Malignant":
                        st.subheader("Your mole has been classified as potentially malignant. Here are the steps we advise you to follow: ")
                        st.write("**Step 1:- DO NOT PANIC! This classification does not necessarily mean it is cancerous, but rather warrants further examination by a medical professional.")
                        st.write("**Step 2:- Schedule an appointment with your primary care physician or dermatologist within a week")
                        st.write("**Step 3:- Keep a close eye on the mole and note any changes in size, shape, color, or texture. This information will be helpful when discussing treatment options with your doctor.")
                        st.write("We'll provide you with additional resources and guidance to support your care. Please check our website for more information on skin cancer symptoms, risk factors, and treatment options.")
                    st.markdown('</div>', unsafe_allow_html=True)

            # Additional information
            st.markdown("""
            ---
            **Note:** This analysis is for informational purposes only and should not 
            be considered as medical advice. Please consult a healthcare professional 
            for proper diagnosis and treatment.
            """)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.markdown("""
            Please ensure:
            - The image is in a supported format (PNG, JPG, JPEG)
            - The image is clear and well-lit
            - The file is not corrupted
            """)

    
        
if __name__ == '__main__':
    main()
