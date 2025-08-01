import streamlit as st
from PIL import Image
import io
import textwrap
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError
import time

st.title("CheatGPT")

import os

# Configure API key (consider using st.secrets for production)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    st.error("Google API key is not set. Please set the GOOGLE_API_KEY environment variable.")
genai.configure(api_key=GOOGLE_API_KEY)

# Create tabs for different input modes
tab1, tab2 = st.tabs(["💬 Text Chat", "🖼️ Image Analysis"])

def analyze_with_gemini_text(prompt):
    """Analyze text prompt using Google Gemini"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def analyze_with_gemini_image(prompt, img):
    """Analyze image with custom prompt using Google Gemini"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, img])
    return response.text

# Text Chat Tab
with tab1:
    st.header("💬 Text-only Chat with Gemini")
    
    # Text input for prompt
    user_prompt = st.text_area(
        "Enter your question or prompt:",
        placeholder="Ask anything... e.g., 'Explain quantum physics', 'Write a Python function', 'Help me with math problems'",
        height=100
    )
    
    st.write("**AI Model:** Google Gemini 1.5 Flash")
    
    if st.button("💭 Generate Response", key="text_button"):
        if user_prompt.strip():
            try:
                with st.spinner("Generating response with Google Gemini..."):
                    response_text = analyze_with_gemini_text(user_prompt)
                    st.write("**Google Gemini Response**")
                    st.markdown(response_text)
                    
            except ResourceExhausted as e:
                st.error("⚠️ **Google API Quota Exceeded Error**")
                st.write("You've reached the free tier limits for the Gemini API. Here are your options:")
                st.write("1. **Wait**: Free tier quotas reset daily")
                st.write("2. **Upgrade**: Consider upgrading to a paid plan")
                st.write("3. **Try later**: The API has per-minute limits that may reset soon")
                
                if hasattr(e, 'retry_delay') and e.retry_delay:
                    retry_seconds = e.retry_delay.seconds
                    st.write(f"Suggested retry delay: {retry_seconds} seconds")
                
                st.write("**Error details:**")
                st.code(str(e))
                
            except GoogleAPICallError as e:
                st.error(f"Google API Error: {e}")
                
            except Exception as e:
                st.error(f"Unexpected error: {e}")
        else:
            st.warning("Please enter a prompt first!")

# Image Analysis Tab
with tab2:
    st.header("🖼️ Image Analysis with Custom Prompts")
    
    uploaded_file = st.file_uploader("Upload your PNG or JPG image:", type=["png", "jpg"])
    
    # Custom prompt input
    custom_prompt = st.text_area(
        "Enter your custom prompt for image analysis:",
        value="Analyze this image and answer any questions shown in it. Provide step-by-step explanations for any problems or questions you can identify.",
        height=100,
        help="Customize how you want the AI to analyze your image"
    )
    
    # Prompt suggestions
    with st.expander("💡 Prompt Suggestions"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Academic Help:**")
            if st.button("📚 Solve math problems in this image", key="math"):
                custom_prompt = "Solve all the math problems shown in this image. Provide step-by-step solutions with clear explanations."
                st.rerun()
            
            if st.button("🧪 Explain science concepts", key="science"):
                custom_prompt = "Identify and explain any scientific concepts, diagrams, or experiments shown in this image."
                st.rerun()
            
            if st.button("📝 Read and summarize text", key="read"):
                custom_prompt = "Read all the text in this image and provide a clear summary of the main points."
                st.rerun()
        
        with col2:
            st.write("**General Analysis:**")
            if st.button("🔍 Describe everything in detail", key="describe"):
                custom_prompt = "Provide a detailed description of everything you see in this image, including objects, text, people, and context."
                st.rerun()
            
            if st.button("❓ Answer questions in image", key="questions"):
                custom_prompt = "Find and answer all questions present in this image. If there are multiple choice questions, explain why each answer is correct or incorrect."
                st.rerun()
            
            if st.button("📊 Analyze charts/graphs", key="charts"):
                custom_prompt = "Analyze any charts, graphs, or data visualizations in this image. Explain the trends, patterns, and key insights."
                st.rerun()

    if uploaded_file is not None:
        # Validate the file extension
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            # Read the image bytes
            img_bytes = uploaded_file.read()

            # Convert bytes to PIL Image object
            img = Image.open(io.BytesIO(img_bytes))
            st.write("✅ Image Uploaded Successfully")
            st.image(img, caption="Uploaded Image")
            
            st.write("**AI Model:** Google Gemini 1.5 Flash")

            # Add a button to trigger analysis
            if st.button("🔍 Analyze Image", key="image_button"):
                if custom_prompt.strip():
                    try:
                        with st.spinner("Analyzing image with Google Gemini..."):
                            response_text = analyze_with_gemini_image(custom_prompt, img)
                            st.write("**Google Gemini Response**")
                            st.markdown(response_text)
                            
                    except ResourceExhausted as e:
                        st.error("⚠️ **Google API Quota Exceeded Error**")
                        st.write("You've reached the free tier limits for the Gemini API. Here are your options:")
                        st.write("1. **Wait**: Free tier quotas reset daily")
                        st.write("2. **Upgrade**: Consider upgrading to a paid plan")
                        st.write("3. **Try later**: The API has per-minute limits that may reset soon")
                        
                        if hasattr(e, 'retry_delay') and e.retry_delay:
                            retry_seconds = e.retry_delay.seconds
                            st.write(f"Suggested retry delay: {retry_seconds} seconds")
                        
                        st.write("**Error details:**")
                        st.code(str(e))
                        
                    except GoogleAPICallError as e:
                        st.error(f"Google API Error: {e}")
                        
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
                else:
                    st.warning("Please enter a custom prompt for image analysis!")
                    
        else:
            st.error("Please upload a valid PNG or JPG image file.")

# Add information about usage
with st.expander("ℹ️ Usage Information"):
    st.write("""
    **Google Gemini 1.5 Flash - Free Tier Limits:**
    - 15 requests per minute
    - 1,500 requests per day
    - Limited input tokens per minute
    - Supports both text and image analysis
    - Fast processing speed
    - Completely free to use (within limits)
    
    **Features:**
    - ✅ Text-only conversations
    - ✅ Image analysis with custom prompts
    - ✅ Academic help (math, science, reading)
    - ✅ Multiple choice question solving
    - ✅ Chart and graph analysis
    - ✅ Document text extraction
    
    **Tips for Better Results:**
    - Be specific in your prompts
    - For math problems: Ask for step-by-step solutions
    - For images: Describe what you want to focus on
    - Wait between requests to avoid rate limits
    - Try different prompt styles if you don't get the desired result
    """)

# API Configuration section
with st.expander("🔧 API Configuration"):
    st.write("""
    **To use this app, you need a Google Gemini API key:**
    
    **Steps to get your API key:**
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Sign in with your Google account
    3. Click "Create API Key"
    4. Copy the generated API key
    5. Replace the GOOGLE_API_KEY in the code with your key
    
    **Free Tier Benefits:**
    - No credit card required
    - 1,500 requests per day
    - Both text and vision capabilities
    - Fast response times
    
    **For Production:**
    - Use Streamlit secrets to store your API key securely
    - Consider upgrading to paid tier for higher limits
    """)

# Model information
st.sidebar.info("""
**Google Gemini 1.5 Flash**

**Capabilities:**
- ✅ Text generation & analysis
- ✅ Image understanding & analysis
- ✅ Mathematical problem solving
- ✅ Code generation & debugging
- ✅ Language translation
- ✅ Document analysis
- ✅ Scientific explanations

**Advantages:**
- 🆓 Free tier available
- ⚡ Fast processing
- 🧠 Multimodal (text + images)
- 📚 Large context window
- 🔒 Privacy-focused
""")

# Usage tips
st.sidebar.success("""
**💡 Usage Tips:**

**For Text Chat:**
- Ask specific questions
- Request step-by-step explanations
- Use examples in your prompts

**For Image Analysis:**
- Upload clear, high-quality images
- Customize prompts for better results
- Try different prompt suggestions
- Be specific about what you want analyzed
""")

# Chat history management
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if st.sidebar.button("🗑️ Clear Session"):
    st.session_state.chat_history = []
    st.rerun()

# Security note
st.sidebar.warning("⚠️ **Security Note**: Store your API key in Streamlit secrets for production deployment, not hardcoded in the script.")