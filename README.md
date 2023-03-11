
# UnPuzzled 

A UnPuzzled is a web application that allows users to upload a picture of an unsolved Sudoku puzzle and receive the solved puzzle in return. The app works by using image recognition technology to identify the numbers in the puzzle, and then applying algorithms to solve the puzzle.

The app can be a useful tool for anyone who enjoys solving Sudoku puzzles but may struggle with particularly challenging puzzles, or who simply wants a quick and easy way to get the solution to a puzzle.
## Tech Stack

- OpenCV: OpenCV is an open-source computer vision library that is used to read, analyze and apply various image processing techniques to the image, such as thresholding, erosion, dilation, etc. 

- Python: Python is a high-level programming language which is used for programming the model. 

- NumPy: NumPy is a Python library which is used for numerical computations of multi-dimensional arrays and matrices

- OCR (Optical Character Recognition) Engine: An OCR engine is used to recognize the digits in the Sudoku puzzle. In our project myModel.h5 fulfills this role. 

- Backtracking algorithm: A backtracking algorithm is used to solve the Sudoku puzzle once the digits have been recognized. Backtracking is an algorithmic technique that is used to solve constraint satisfaction problems by trying out different solutions and undoing them if they lead to an invalid solution.

- Streamlit: Used for constructing and deploying the web app. 

- Deta Space: Used for obtaning a temporary path for the uploaded sudoku image since we need the image path to perform certain functions. 



## Screenshots

**Web App Layout**
![App](https://github.com/Tiagupt03/UnPuzzled/blob/main/Sample_images/Readme_images/Screenshot%20(236).png?raw=true)

**Sudoku Uploaded**
![Upload](https://github.com/Tiagupt03/UnPuzzled/blob/main/Sample_images/Readme_images/Screenshot%20(237).png?raw=true)

**Sudoku image submitted**
![Submit](https://github.com/Tiagupt03/UnPuzzled/blob/main/Sample_images/Readme_images/Screenshot%20(238).png?raw=true)

**Sudoku Solved**
![Solution](https://github.com/Tiagupt03/UnPuzzled/blob/main/Sample_images/Readme_images/Screenshot%20(240).png?raw=true)
## References

- [OpenCV basics](https://www.youtube.com/playlist?list=PLS1QulWo1RIa7D1O6skqDQ-JZ1GGHKK-K)
- [Sudoku backtracking algorithm](https://youtu.be/eqUwSA0xI-s)
- [myModel.h5](https://youtu.be/y1ZrOs9s2QA)
- [Sudoku image processing](https://youtu.be/qOXDoYUgNlU)
- [Web App layout](https://youtu.be/gksXyp3J-Ho)
- [Streamlit Documentation](https://docs.streamlit.io/)
## Acknowledgements

- We would like to express our sincere gratitude for the invaluable support and guidance of WE mentors throughout our project journey. Their guidance and mentorship have been instrumental in helping us achieve our project goals and deliverables.

- Kavita
- Asokan 
- Kunisha
- Spoorthy
- Anasuya 
- Sai Krishna 

## Demo

[Demo of the Web App](https://drive.google.com/file/d/1n2KF894HV_GBRK48IzbDs_onRFOEazp1/view?usp=sharing)
