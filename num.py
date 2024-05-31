import cv2 as cv
import numpy as np
import pytesseract
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r''

cascade = cv.CascadeClassifier("haarcascade_russian_plate_number.xml")
states = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CG": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OD": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TS": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UK": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DN": "Dadra and Nagar Haveli and Daman and Diu",
    "DL": "Delhi",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "PY": "Puducherry"
}

def extract_num(img_name):
    global read
    img = cv.imread(img_name)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    nplate = cascade.detectMultiScale(gray,1.1,4)
    for (x,y,w,h) in nplate:
        a,b = (int(0.02*img.shape[0]), int(0.02*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]

#         Image Processing
    kernel = np.ones((1,1), np.uint8)
    plate = cv.dilate(plate, kernel, iterations=1)
    plate = cv.erode(plate, kernel, iterations=1)
    plate_gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
    (thresh, plate) = cv.threshold(plate_gray, 127, 255, cv.THRESH_BINARY)

    read = pytesseract.image_to_string((plate))
    print(read)
    read = ''.join(e for e in read if e.isalnum())
    stat = read[0:2]
    try:
        print('Car Belongs to', states[stat])
    except:
        print('State not recognized!')
    print(read)
    cv.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
    cv.rectangle(img, (x,y - 40), (x+w, y), (51,51,255), -1)
    cv.putText(img, read, (x + 50, y), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), thickness=2)
    cv.imshow("Plate", plate)

    cv.imshow("Result", img)
    cv.imwrite("result.jpg", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def browse_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                          filetypes=(("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")))
    extract_num(filename)


window = tk.Tk()
window.title("License Plate Recognition")
window.geometry("400x200")

select_button = tk.Button(window, text="Select Image", command=browse_file)
select_button.pack()

# output_button = tk.Button(window, text="Show Output", command=lambda: extract_num("result.jpg"))
# output_button.pack()

window.mainloop()
