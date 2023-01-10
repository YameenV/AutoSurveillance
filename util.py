import cv2 as cv
import streamlit as st

def detect(dataFrame, frame):

    (w,h) = frame.shape[:2]
    topLeft = []
    topRight = []
    bottomLeft = []
    bottomRight = []
    xCen, yCen = int(w//2), int(h//2)

    # Display Back Canvas
    frame[:] = (0,0,0)

    # Display Grid
    cv.line(frame, (0, int(w/2)), (h, int(w/2)), color=(199,21,133), thickness=10)
    cv.line(frame, (int(h/2), 0), (int(h/2), w), color=(199,21,133), thickness=10)


    for i in dataFrame.index:

        if dataFrame["class"][i] == 1:
            cv.rectangle(frame,(int(dataFrame["xmin"][i]),int(dataFrame["ymin"][i])),(int(dataFrame["xmax"][i]),int(dataFrame["ymax"][i])),(0,255,0),2)
            cv.putText(frame, f'{i}', (int(dataFrame["xmin"][i]),int(dataFrame["ymin"][i])-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            
            x = int((int(dataFrame["xmin"][i]) + int(dataFrame["xmax"][i])) / 2)
            y = int((int(dataFrame["ymin"][i]) + int(dataFrame["ymax"][i])) / 2)
            cv.circle(frame, (x,y), radius=5, color=(0, 0, 255), thickness=-1)
        

        else:
            cv.rectangle(frame,(int(dataFrame["xmin"][i]),int(dataFrame["ymin"][i])),(int(dataFrame["xmax"][i]),int(dataFrame["ymax"][i])),(255,0,0),2)
            cv.putText(frame, f'{i}', (int(dataFrame["xmin"][i]),int(dataFrame["ymin"][i])-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

            x = int(int(dataFrame["xmin"][i]) + int(dataFrame["xmax"][i]) / 2)
            y = int(int(dataFrame["ymin"][i]) + int(dataFrame["ymax"][i]) / 2)
            cv.circle(frame, (x,y), radius=5, color=(0, 0, 255), thickness=-1)
       
        if y > xCen:
            
            if x < yCen:
                try:
                    xPrev, yPrev = topLeft[-1]
                    cv.line(frame, (xPrev, yPrev), (x,y), color = (0, 0, 255), thickness=3)
                except:
                    pass
                topLeft.append((x,y))
            else:
                try:
                    xPrev, yPrev = topRight[-1]
                    cv.line(frame, (xPrev, yPrev), (x,y), color=(0, 0, 255), thickness=3)
                except:
                    pass
                topRight.append([x,y])
        
        else:

            if x < yCen:
                try:
                    xPrev, yPrev = bottomLeft[-1]
                    cv.line(frame, (xPrev, yPrev), (x,y), color = (0, 0, 255), thickness=3)
                except:
                    pass
                bottomLeft.append((x,y))
            else:
                try:
                    xPrev, yPrev = bottomRight[-1]
                    cv.line(frame, (xPrev, yPrev), (x,y), color=(0, 0, 255), thickness=3)
                except:
                    pass
                bottomRight.append([x,y])

    
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    return frame 

def framePerSecond(newTime, prvTime):
    return 1/(newTime - prvTime)


def defaultConfig(pagesize:int=0):
    if pagesize == 0:
        st.set_page_config(layout="wide")
    elif pagesize == 1:
        st.set_page_config(layout="centered")
        
    hide_st_style = """
                <style>
                MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


