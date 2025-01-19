import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import whisper
import os
import tempfile

# Step 1: Extract Audio from Video
def extract_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)
    audio.close()
    video.close()

# Step 2: Transcribe Audio
def transcribe_audio(audio_path, model="base"):
    whisper_model = whisper.load_model(model)
    result = whisper_model.transcribe(audio_path)
    return result['text']

# Step 3: Correct Grammar
def correct_grammar(text):
    # Placeholder for grammar correction logic (can be integrated with GPT-4 or other APIs)
    return text

# Step 4: Convert Text to Speech
def text_to_speech(text, output_audio_path):
    tts = gTTS(text)
    tts.save(output_audio_path)

# Step 5: Replace Audio in Video
def replace_audio(video_path, new_audio_path, output_video_path):
    print("Replacing audio in video...")
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)
    video = video.set_audio(new_audio)
    # Save the output video to a fixed directory
    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=video.fps)
    new_audio.close()
    video.close()

# Main Processing Function
def process_video(video_path, output_video_path, model="base"):
    try:
        # Paths
        extracted_audio = "extracted_audio.wav"
        new_audio = "new_audio.mp3"

        # Step-by-step processing
        extract_audio(video_path, extracted_audio)
        transcribed_text = transcribe_audio(extracted_audio, model)
        corrected_text = correct_grammar(transcribed_text)
        text_to_speech(corrected_text, new_audio)
        replace_audio(video_path, new_audio, output_video_path)
        print("Processing completed successfully!")

        # Check if the file exists before proceeding
        if os.path.exists(output_video_path):
            with open(output_video_path, "rb") as file:
                # Process the file (e.g., for Streamlit download)
                print(f"Successfully accessed {output_video_path}")
        else:
            print(f"Error: {output_video_path} not found.")

        # Cleanup temporary files
        os.remove(extracted_audio)
        os.remove(new_audio)

    except Exception as e:
        print(f"An error occurred: {e}")

# Streamlit UI
def main():
    st.title("AI Voice Replacement for Videos")
    st.subheader("- VARUN SAI 😊❤️")
    st.markdown("Add short videos of length between 50 sec - 1.30 mins")

    # File upload
    video_file = st.file_uploader("Upload a Video File", type=["mp4", "mov", "avi"])

    if video_file:
        st.video(video_file)

        with st.spinner("Processing video... Please wait."):
            # Save the uploaded file temporarily
            temp_video_path = os.path.join(tempfile.mkdtemp(), "uploaded_video.mp4")
            with open(temp_video_path, "wb") as f:
                f.write(video_file.read())

            # Define the output video path
            output_video_path = os.path.join(tempfile.mkdtemp(), "output_video.mp4")

            # Process the video
            process_video(temp_video_path, output_video_path)

            if os.path.exists(output_video_path):
                st.success("Processing completed successfully!")

                # Allow user to download the output video
                with open(output_video_path, "rb") as file:
                    st.download_button(
                        label="Download Processed Video",
                        data=file,
                        file_name="output_video.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("There was an issue with processing the video.")

if __name__ == "__main__":
    main()
