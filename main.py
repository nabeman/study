import cv2
import time
import datetime
import eel
import motion

def main():
    eel.init("web")

    @eel.expose
    def Capture():
        print(time.time() * 1000)
        # motion.Motion().run()
        cap = cv2.VideoCapture(0)
        
        while(True):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow("Webcam Live", frame)
                # print(datetime.datetime.fromtimestamp(int(time.time())))
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    eel.MakeJson()
                    break

        cap.release()
        cv2.destroyAllWindows()

    eel.start("index.html")

if __name__ == "__main__":
    main()