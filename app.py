
import streamlit as st
import cv2
import os
import tempfile
import pandas as pd
import json
import google.generativeai as genai
from scenedetect import SceneManager, open_video, ContentDetector

# Configure Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Settings Page
st.sidebar.header("Settings")
max_images = st.sidebar.slider("Max Frames to Extract", min_value=1, max_value=20, value=5)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini for processing."""
    file = genai.upload_file(path, mime_type=mime_type)
    return file

def extract_key_frames(video_path, output_folder, max_frames):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_frames = []
    
    for scene in scene_list[:max_frames]:
        start_frame = scene[0].get_frames()
        timestamp = scene[0].get_seconds()
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = cap.read()
        if ret:
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            extracted_frames.append((frame_path, start_frame, timestamp))
            frame_count += 1
    
    cap.release()
    return extracted_frames

def extract_baseball_stats_with_gemini(image_data):
    extracted_stats = []
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
    )
    
    for image_path, frame_number, timestamp in image_data:
        file = upload_to_gemini(image_path, mime_type="image/jpeg")
        chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": [file, f"Extract structured baseball game statistics such as pitch speed (in mph), exit velocity (in mph), player names, scores, innings, and any other relevant in-game data. Ensure that numeric values include appropriate SI units where necessary. Return the result as a properly formatted JSON with keys corresponding to the extracted statistics. The timestamp of this frame is {timestamp} seconds."]}
            ]
        )
        response = chat_session.send_message("Extract structured baseball statistics with SI units.")
        extracted_stats.append((response.text, frame_number, timestamp))
    
    return extracted_stats

def clean_gemini_json(raw_json):
    """Cleans the raw JSON string from Gemini response to ensure it's valid JSON format."""
    try:
        cleaned_json = raw_json.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        return None

def consolidate_gemini_outputs(extracted_data):
    """Takes all extracted data and consolidates it into a structured format with uniform key names."""
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
    )
    
    formatted_data = [{"timestamp": ts, "frame_number": fn, "raw_data": raw} for raw, fn, ts in extracted_data]
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [json.dumps(formatted_data), "Consolidate the extracted baseball statistics data into a structured JSON format where all key names are consistent across all frames. Ensure each row corresponds to a single frame and that all extracted values are structured in a tabular manner without nested JSON values in cells. Include SI units where necessary (e.g., pitch speed in mph)."]}
        ]
    )
    response = chat_session.send_message("Generate a consolidated and coherent structured JSON for the dataset.")
    return clean_gemini_json(response.text)

def chat_with_data(user_query, dataframe):
    """Allows users to query the dataframe using Gemini AI."""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [f"Given the following baseball game statistics dataframe, answer the user's query:\n{dataframe.to_json(orient='records')}\n\nQuery: {user_query}"]}
        ]
    )
    response = chat_session.send_message("Answer the user's query based on the dataframe.")
    return response.text

# Streamlit UI
st.title("Baseball Stat Extractor from Media Files")
st.write("Upload a baseball game video or image, and we’ll extract key statistics using AI.")

uploaded_file = st.file_uploader("Upload Baseball Video/Image", type=["mp4", "avi", "mov", "jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension in ["mp4", "avi", "mov"]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_video:
            temp_video.write(uploaded_file.read())
            media_path = temp_video.name
        
        st.write("Extracting key scenes...")
        output_folder = tempfile.mkdtemp()
        frames = extract_key_frames(media_path, output_folder, max_images)
        st.write(f"Extracted {len(frames)} key frames.")
        
    elif file_extension in ["jpg", "png", "jpeg"]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_image:
            temp_image.write(uploaded_file.read())
            media_path = temp_image.name
        frames = [(media_path, None, None)]
    
    st.write("Extracting baseball statistics using Gemini AI...")
    extracted_stats = extract_baseball_stats_with_gemini(frames)
    consolidated_data = consolidate_gemini_outputs(extracted_stats)
    
    if consolidated_data:
        df = pd.DataFrame(consolidated_data)
        st.write("Extracted baseball statistics in tabular format:")
        st.dataframe(df)
        
        st.write("### Chat with Your Data")
        user_query = st.text_input("Ask a question about the extracted stats:")
        if user_query:
            answer = chat_with_data(user_query, df)
            st.write("**Response:**", answer)
    else:
        st.write("Error parsing consolidated output: Invalid JSON format.")

    st.success("Processing complete! The extracted statistics are displayed above.")
