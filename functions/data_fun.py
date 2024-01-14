import pandas as pd


def obtain_year_period(element):
    year, period = element.split("-")
    return int(year), int(period[0])


def get_student_dataframe(dataframe, selected_student):
    student_data = dataframe[dataframe.estudiante == selected_student].fillna(0)
    student_data["estado"] = student_data.apply(
        lambda x: "AP" if ((x.nota_teorico*0.7)+(x.nota_practico*0.3)) > 60 else "RP", axis=1)
    student_data = student_data.sort_values(by="anio", ascending=False).reset_index(drop=True)
    return student_data


def get_times_taken_mean(dataframe, student_data, criteria):
    important_columns = dataframe.columns.tolist()[7:-2]
    max_student = student_data["vez_tomada"].values.max()
    df_time_taken = dataframe[dataframe.vez_tomada == max_student][important_columns]
    dic_time_taken = df_time_taken.mean(axis=0).round(2).to_dict()
    return max_student, dic_time_taken[criteria]


def get_same_course(dataframe, student_data, criteria):
    important_columns = dataframe.columns.tolist()[7:-2]
    student_period = student_data["year_period"].values.to_list()
    periods = sorted(student_period, key=obtain_year_period, reverse=True)
    actual_period = periods[0]
    df_same_course = dataframe[dataframe.year_period == actual_period][important_columns]
    dic_same_course = df_same_course.mean(axis=0).round(2).to_dict()
    return actual_period, dic_same_course[criteria]


# dataframe = pd.read_csv(".\performance_review_fixed.csv", sep=";")
# student_data = get_student_dataframe(dataframe, "Jane Smith")
# years_period = [f"{str(row.anio)}-{row.periodo}" for idx, row in student_data.iterrows()]

