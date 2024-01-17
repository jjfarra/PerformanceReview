import pandas as pd
from datetime import datetime as dt


def obtain_year_period(element):
    year, period = element.split("-")
    return int(year), int(period[0])


def obtain_columns(element):
    return element.columns.tolist()[7:-6]


def obtain_kind(career):
    return career.split(" ")[0]


def make_title(element):
    return " ".join(element.split("_")).capitalize()


def obtain_actual_period():
    year = int(dt.now().year)
    month = int(dt.now().month)
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


def obtain_sorted_values(labels, values):
    return_values = {}
    for i in range(len(labels)):
        return_values[labels[i]] = values[i]
    return_values = dict(sorted(return_values.items(), key=lambda item: item[1]))
    return return_values


def obtain_colors(student_id, values):
    colors = ["lightslategrey", ]*len(values.keys())
    idx = list(values.keys()).index(student_id)
    colors[idx] = "crimson"
    return colors


def check_novice(dataframe):
    actual_period = obtain_actual_period().split("-")
    next_year = int(actual_period[0]) + 1
    years = [actual_period[0], str(next_year)]
    dataframe["check_novice"] = [True if str(row.matricula)[:4] in years else False for idx, row in
                                 dataframe.iterrows()]
    return dataframe


def get_new_columns(dataframe):
    dataframe = decode_career(dataframe)
    dataframe["year_period"] = [f"{str(row.anio)}-{row.periodo}" for idx, row in dataframe.iterrows()]
    dataframe["course"] = [f"{row.year_period}-{str(row.paralelo)}" for idx, row in dataframe.iterrows()]
    dataframe["kind_career"] = [obtain_kind(row.carrera) for idx, row in dataframe.iterrows()]
    dataframe["estado"] = dataframe.apply(
        lambda x: "AP" if ((x.nota_teorico * 0.7) + (x.nota_practico * 0.3)) > 60 else "RP", axis=1)
    dataframe = check_novice(dataframe)
    return dataframe


def decode_career(dataframe):
    career_data = pd.read_excel("files/Carreras.xlsx")
    cod_to_carrera = dict(zip(career_data['COD'], career_data['CARRERA']))
    dataframe['carrera'] = dataframe['carrera'].map(cod_to_carrera).fillna(dataframe['carrera'])
    return dataframe


def get_student_dataframe(dataframe, selected_student):
    student_data = dataframe[dataframe.estudiante == selected_student].fillna(0)
    student_data.reset_index(drop=True, inplace=True)
    student_data = student_data.sort_values(by="year_period", ascending=False,
                                            key=lambda x: x.map(obtain_year_period))
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


def get_same_period(dataframe, student_data, criteria):
    period = obtain_actual_period()
    df_period = dataframe[dataframe.year_period == period][obtain_columns(dataframe)]
    dic_period = df_period.mean(axis=0).round(2).to_dict()
    if period in student_data.year_period.values.tolist():
        return period, dic_period[criteria]


def get_novice(dataframe, student_data, criteria):
    columns = obtain_columns(dataframe)
    df_novice = dataframe[dataframe.check_novice][columns]
    dic_novice = df_novice.mean(axis=0).round(2).to_dict()
    return student_data.shape[0] == 1, dic_novice[criteria]


def get_same_kind_career(dataframe, student_data, criteria):
    kind_career = student_data.kind_career[0]
    columns = obtain_columns(dataframe)
    dataframe.drop_duplicates(subset=["matricula"], keep="first", inplace=True)
    df_kind = dataframe[dataframe.kind_career == kind_career][columns]
    dic_kind = df_kind.mean(axis=0).round(2).to_dict()
    return kind_career, dic_kind[criteria]


def get_all_comparative(dataframe, student_data, criteria):
    times, times_value = get_times_taken_mean(dataframe, student_data, criteria)
    course, course_value = get_same_course(dataframe, student_data, criteria)
    career, career_value = get_same_career(dataframe, student_data, criteria)
    period, period_value = get_same_period(dataframe, student_data, criteria)
    novice, novice_value = get_novice(dataframe, student_data, criteria)
    kind, kind_value = get_same_kind_career(dataframe, student_data, criteria)
    student_value = student_data[criteria][0]
    return [times_value, course_value, career_value, period_value, novice_value, kind_value, student_value]
