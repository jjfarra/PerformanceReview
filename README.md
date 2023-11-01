# Student Performance Review with Streamlit

This project is a Streamlit web application for reviewing and visualizing student performance in various subjects. Users can upload data files for different years, select specific students, and view their performance in terms of theoretical and practical scores, lessons, workshops, and exams.

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
Upload Data Files: Users can upload CSV files for different years containing student performance data. For this example: You can use the file called: *performance_review_fixed.csv*

Select Student: Users can select a specific student from the dropdown list to view their performance.

View Performance: The app displays performance information in gauge charts, separating lessons, workshops, and exams. Users can see the student's progress in each category.

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
