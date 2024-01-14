import pandas as pd
from datetime import datetime as dt


def obtain_year_period(element):
    year, period = element.split("-")
    return int(year), int(period[0])


def obtain_columns(element):
    return element.columns.tolist()[7:-4]


def obtain_period(year, month):
    period = ""
    if month < 3:
        period += "2S"
        year -= 1
    elif 2 <= month < 5:
        period += "0S"
    elif 5 <= month < 7:
        period += "1S"
    elif 7 <= month:
        period += "2s"
    return f"{year}-{period}"


def get_student_dataframe(dataframe, selected_student):
    student_data = dataframe[dataframe.estudiante == selected_student].fillna(0)
    student_data["estado"] = student_data.apply(
        lambda x: "AP" if ((x.nota_teorico*0.7)+(x.nota_practico*0.3)) > 60 else "RP", axis=1)
    student_data = student_data.sort_values(by="anio", ascending=False).reset_index(drop=True)
    return student_data


def get_times_taken_mean(dataframe, student_data, criteria):
    max_student = student_data["vez_tomada"].values.max()
    df_time_taken = dataframe[dataframe.vez_tomada == max_student][obtain_columns(dataframe)]
    dic_time_taken = df_time_taken.mean(axis=0).round(2).to_dict()
    return max_student, dic_time_taken[criteria]


def get_same_course(dataframe, student_data, criteria):
    student_data = student_data.sort_values(by="year_period", ascending=False, key=lambda x: x.map(obtain_year_period))
    actual_course = student_data["course"].values.tolist()[0]
    df_same_course = dataframe[dataframe.course == actual_course][obtain_columns(dataframe)]
    dic_same_course = df_same_course.mean(axis=0).round(2).to_dict()
    return actual_course, dic_same_course[criteria]


def get_same_career(dataframe, student_data, criteria):
    career = student_data["carrera"].unique().tolist()[0]
    df_career = dataframe[dataframe.carrera == career][obtain_columns(dataframe)]
    dic_career = df_career.mean(axis=0).round(2).to_dict()
    return career, dic_career[criteria]


def get_novice(dataframe, student_data, criteria):
    actual_year = int(dt.now().year)
    actual_month = int(dt.now().month)
    period = obtain_period(actual_year, actual_month)
    df_novice = dataframe[dataframe.year_period == period][obtain_columns(dataframe)]
    dic_novice = df_novice.mean(axis=0).round(2).to_dict()
    if period in student_data.year_period:
        return period, dic_novice[criteria]



# dataframe = pd.read_csv(".\performance_review_fixed.csv", sep=";")
# dataframe["year_period"] = [f"{row.anio}-{row.periodo}" for idx, row in dataframe.iterrows()]
# dataframe["course"] = [f"{row.year_period}-{row.paralelo}" for idx, row in dataframe.iterrows()]
# student_data = get_student_dataframe(dataframe, "Jane Smith")
# compare_value = dataframe[dataframe["carrera"] == "Matematicas"]["nota_teorico"]
# print(compare_value)
actual_year = int(dt.now().year)
actual_month = int(dt.now().month)
aperiod = obtain_period(actual_year, actual_month)
print((aperiod))
