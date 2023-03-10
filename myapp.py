def check(puzzle, i, row, col):
    rows = puzzle[int(row)]
    column = [puzzle[r][col] for r in range(0,9,1)]
    if i in rows:
        return False
    if i in column:
        return False
    SquareRow = (row // 3)*3
    squareColumn = (col // 3)*3
    Square = [puzzle[y][z] for y in range(SquareRow, SquareRow+3) for z in range(squareColumn, squareColumn+3)]
    if i in Square:
        return False
    return True


def find(puzzle):
    for i in range(0,9,1):
        for j in range(0,9,1):
            if puzzle[i][j]==0:
                return i,j
    return None


def solve(board):
    finds = find(board)
    if not finds:
        return True
    else:
        row, col = finds

    for i in range(1,10):
        if check(board, i, row, col):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

########################################################################

import streamlit as st
from deta import Deta
import os
import cv2
from PIL import Image
import numpy as np
from utlis import *
    
##############################################################################
DETA_KEY = "d0zhy5rxc4r_UZs4mFzYorGrmTKbRhtANZzTqPJr9nyF" #Secret key to connect to deta drive
deta = Deta(DETA_KEY) # Initialize deta object with a project key

drive = deta.Drive("drive_name") # Connecting to the Deta drive

# Here i'm taking the input from `st.file_uploader`, same principle can be  applied.
st.title('Sudoku Solver')
html_temp = """
<body style="background-color:red;">
<div style="background-color:teal ;padding:10px">
<h2 style="color:white;text-align:center;">UnPuzzled Web App</h2>
</div>
</body>
"""
st.markdown(html_temp, unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Sudoku Image", type=['jpg', 'png', 'jpeg'])
st.set_option('deprecation.showfileUploaderEncoding', False) # Enabling the automatic file decoder
submit_button = st.button(label='Upload Sudoku') # Submit button
if uploaded_file is not None:
    file = uploaded_file.read() # Read the data
    image_result = open(uploaded_file.name, 'wb') # creates a writable image and later we can write the decoded result
    image_result.write(file) # Saves the file with the name uploaded_file.name to the root path('./')
    image_result.close() # Close the file pointer
    if submit_button:
        name = uploaded_file.name # Getting the name of current file
        path ='./'+uploaded_file.name # Creating path string which is basically ["./image.jpg"]
        drive.put(name, path=path) # so, we have our file name and path, so uploading images to the drive
        st.image(uploaded_file)
        
    if st.button("Solve Sudoku"):
        ########################################################################
        pathImage = uploaded_file.name
        heightImg = 450
        widthImg = 450
        model = intializePredectionModel()  # LOAD THE CNN MODEL
        ########################################################################


        #### 1. PREPARE THE IMAGE
        img = cv2.imread(pathImage)
        img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE TO MAKE IT A SQUARE IMAGE
        imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
        imgThreshold = preProcess(img)

        #### 2. FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS

        #### 3. FIND THE BIGGEST COUNTOUR AND USE IT AS SUDOKU
        biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            biggest = reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 0, 255), 25) # DRAW THE BIGGEST CONTOUR
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2) # GER
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            imgDetectedDigits = imgBlank.copy()
            imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

            #### 4. SPLIT THE IMAGE AND FIND EACH DIGIT AVAILABLE
            imgSolvedDigits = imgBlank.copy()
            boxes = splitBoxes(imgWarpColored)
            numbers = getPredection(boxes, model)
            imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
            numbers = np.asarray(numbers)
            posArray = np.where(numbers > 0, 0, 1)

            #### 5. FIND SOLUTION OF THE BOARD
            board = np.array_split(numbers,9)
            try:
                solve(board)
            except:
                pass
            flatList = []
            for sublist in board:
                for item in sublist:
                    flatList.append(item)
            solvedNumbers =flatList*posArray
            imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)

            # #### 6. OVERLAY SOLUTION
            pts2 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts1 =  np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
            imgInvWarpColored = img.copy()
            imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
            inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
            imgDetectedDigits = drawGrid(imgDetectedDigits)
            imgSolvedDigits = drawGrid(imgSolvedDigits)

            st.image(inv_perspective)
        else:
            st.write("No Sudoku Found")
        #cv2.waitKey(0)
        os.remove(uploaded_file.name) # Finally deleting it from root folder
        st.success('The Sudoku is solved!') # Success message
