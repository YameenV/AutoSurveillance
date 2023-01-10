import streamlit as st
import tempfile as tpf
from streamlit_webrtc import webrtc_streamer
import av
import cv2 as cv
from model import loadModel
from util import detect, framePerSecond, defaultConfig
import time

defaultConfig(1)

st.title("Pedestrian Tracking")
model = loadModel("./best.pt")

class LiveVideoProcessor:
    def recive(self, frame):
        frm = frame.to_ndarray(format="bgr24")
        # same step use in upload video
        return av.VideoFrame.from_ndarray(frm, format='bgr24')

def main():

    videoBuffer = st.file_uploader("Upload a Video file", type=["mp4"])
    tpFile = tpf.NamedTemporaryFile(suffix=".mp4", delete=False)

    stframe = st.empty()
    stNoOfPeopleTxt = st.empty()
    stPeopleWithMask = st.empty()
    stPeopleWithOutMask = st.empty()
    stFps = st.empty()

    #Calculating Fps
    prevFrameTime = 0
    newFrameTime = 0

    if videoBuffer:
        tpFile.write(videoBuffer.read())
        videoFrame = cv.VideoCapture(tpFile.name)

        while videoFrame.isOpened():
            ret, frame = videoFrame.read()
            if not ret:
                break

            result = model(frame)
            data = result.pandas().xyxy[0]

            frame = detect(data, frame)
            
            #Updating Frame
            stframe.image(frame)

            # Calculating Fps
            newFrameTime = time.time()
            fps = framePerSecond(newFrameTime,prevFrameTime) 
            prevFrameTime = newFrameTime

            ## Data To be Display
            stNoOfPeopleTxt.text(f"Number of People = {len(data.index)}")
            stPeopleWithMask.text(f'People With Mask = {len(data[data["class"] == 1])}')
            stPeopleWithOutMask.text(f'People With Out Mask = {len(data[data["class"] == 0])}')
            stFps.text(f"FPS = {str(int(fps))}")

  
    st.text("Start a WebCam")
    webrtc_streamer(key="key", video_processor_factory=LiveVideoProcessor)
    

if __name__ == "__main__":
    main()