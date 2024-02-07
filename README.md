# Student Performance Review with Streamlit

This project is a Streamlit web application for reviewing and visualizing student performance in various subjects. Users can upload data files for different years, select specific students, and view their performance in terms of theoretical and practical scores, lessons, workshops, and exams. \
You can try the dashboard on [Click Here!](https://performance-review.streamlit.app/) The Link doesn't work, problem with Streamlit and their host

## Getting Started

To run this Streamlit application locally, follow the steps below:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/jjfarra/PerformanceReview.git

2. Navigate to the project directory:

    ```bash
    cd PerformanceReview
3. Create a virtual environment:

   ```bash
    python -m venv venv

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt

5. Run the Streamlit app:

    ```bash
    streamlit run dashboard.py
    
The Streamlit app will be accessible in your web browser.

## Usage
Upload Data Files: Users can upload CSV files for different years containing student performance data. For this example: You can use the file called: *performance_review_test.csv*

Select Student: Users can select a specific student from the dropdown list to view their performance.

View Performance: The app displays performance information in gauge charts, separating lessons, workshops, and exams. Users can see the student's progress in each category.

## File Structure
To work properly the upload file on the dashboard, the header and the structure need to be:\
**HEADER:** \
**matricula,estudiante,carrera,anio,periodo,paralelo,vez_tomada,\
nota_teorico,nota_practico,\
leccion_1,leccion_2,leccion_3,leccion_4,\
taller_1,taller_2,taller_3,taller_4,\
examen_parcial,examen_final,examen_mejoramiento,profesor**

### Columns:

- **matricula:** Appears to be a unique identifier for each student.
- **estudiante:** The name of the student.
- **carrera:** The code of the course or program the student is enrolled in. 
- **anio:** The year in which the evaluation took place.
- **periodo:** The academic period of the evaluation (like 1S, 2S, etc.).
- **paralelo:** Number of the parallel or section.
- **vez_tomada:** The number of times the student has taken the subject.
- **nota_teorico:** Grade obtained in the theoretical part of the course.
- **nota_practico:** Grade obtained in the practical part of the course.
- **leccion_1** to **leccion_4:** Grades for different lessons or tests.
- **taller_1** to **taller_4:** Grades for different workshops or practical assignments.
- **examen_parcial:** Grade of the midterm exam.
- **examen_final:** Grade of the final exam.
- **examen_mejoramiento:** Grade of an improvement exam, if applicable.
- **profesor:** Name of the professor who taught the course.

## Customization
You can customize the appearance and styling of the app, including font styles, colors, and layout, to match your preferences.

You can adjust the dimensions and styles of the gauge charts to better suit your design.

If you need additional features, you can extend the app with more visualizations or functionality.

## Contributing
If you'd like to contribute to this project, please follow these guidelines:

Fork the repository.

Create a new branch for your feature or bug fix.

Make your changes and commit them.

Create a pull request, explaining your changes and their purpose.

## Acknowledgments
This project uses Streamlit for creating interactive web applications in Python.
Plotly is used for creating gauge charts.
## Contact
If you have questions or need further assistance, feel free to contact @jjfarra.

Enjoy using the Student Performance Review app!
