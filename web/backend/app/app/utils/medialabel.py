import re
from app import crud
from app.schemas import MediaLabelCreate, InvalidAnnotation

def get_medialabel_schemas_from_file_content(
    content: str,
    media_id: int,
    existing_labels: list
):
    label_names = list(map(lambda existing_label: existing_label.name, existing_labels))

    medialabels_times = {}
    medialabels_schemas = []
    invalid_lines = []

    previous_time_info = None #store time info before merge it with frequencies info

    lines = content.splitlines()
    for index, line in enumerate(lines):

        elements = re.split(r'\t+', line.decode('utf-8')) #split by tabulation

        if (len(elements) != 3):
            invalid_lines.append(InvalidAnnotation(line=index, content=line, detail="columns_number"))
            continue

        try:
            if (elements[0] == "\\"
                    and type(float(elements[1])) is float
                    and type(float(elements[2])) is float): #line data matches to frequencies

                if (type(previous_time_info) is not dict): #there was no valid time data on previous line
                    continue

                # verify frequencies
                previous_time_info["low_freq"] = float(elements[1])
                previous_time_info["high_freq"] = float(elements[2])
                if (previous_time_info["low_freq"] >= previous_time_info["high_freq"]):
                    invalid_lines.append(
                        InvalidAnnotation(line=index, content=line, detail="low_freq_lower_then_high_freq")
                    )
                    previous_time_info = None
                    continue

                if previous_time_info["begin_time"] in medialabels_times:
                    if previous_time_info["end_time"] in medialabels_times[previous_time_info["begin_time"]]:
                        unique_label_id = medialabels_times[previous_time_info["begin_time"]][previous_time_info["end_time"]]
                        if previous_time_info["label_id"] == unique_label_id:
                            invalid_lines.append(
                                InvalidAnnotation(line=index, content=line, detail="same_times_on_species")
                            )
                            previous_time_info = None
                            continue

                if not previous_time_info["begin_time"] in medialabels_times:
                    medialabels_times[previous_time_info["begin_time"]] = {}

                medialabels_times[previous_time_info["begin_time"]][previous_time_info["end_time"]] = previous_time_info["label_id"]

                # create medialabel schema
                medialabel_in = MediaLabelCreate(begin_time=previous_time_info["begin_time"],
                                        end_time=previous_time_info["end_time"],
                                        label_id=previous_time_info["label_id"],
                                        invalid_label_text=previous_time_info["invalid_label_text"],
                                        low_freq=previous_time_info["low_freq"],
                                        high_freq=previous_time_info["high_freq"],
                                        media_id=media_id)

                medialabels_schemas.append(medialabel_in)

                previous_time_info = None

            elif (type(float(elements[0])) is float
                    and type(float(elements[1])) is float
                    and type(elements[2]) is str): #line data matches to time info and label

                if (type(previous_time_info) is dict): # if there is no frequencies associated to previous annotation
                    # verify times
                    if (previous_time_info["begin_time"] >= previous_time_info["end_time"]):
                        invalid_lines.append(
                            InvalidAnnotation(line=index, content=line, detail="begin_time_lower_than_end_time")
                        )
                        previous_time_info = None
                        continue


                    if previous_time_info["begin_time"] in medialabels_times:
                        if previous_time_info["end_time"] in medialabels_times[previous_time_info["begin_time"]]:
                            unique_label_id = medialabels_times[previous_time_info["begin_time"]][previous_time_info["end_time"]]
                            if previous_time_info["label_id"] == unique_label_id:
                                invalid_lines.append(
                                    InvalidAnnotation(line=index, content=line, detail="same_times_on_species")
                                )
                                previous_time_info = None
                                continue

                    if not previous_time_info["begin_time"] in medialabels_times:
                        medialabels_times[previous_time_info["begin_time"]] = {}

                    medialabels_times[previous_time_info["begin_time"]][previous_time_info["end_time"]] = previous_time_info["label_id"]

                    medialabel_in = MediaLabelCreate(begin_time=previous_time_info["begin_time"],
                                            end_time=previous_time_info["end_time"],
                                            label_id=previous_time_info["label_id"],
                                            invalid_label_text=previous_time_info["invalid_label_text"],
                                            media_id=media_id)
                    medialabels_schemas.append(medialabel_in)

                previous_time_info = { "begin_time": float(elements[0]), "end_time": float(elements[1]) }

                # verify times
                if (previous_time_info["begin_time"] >= previous_time_info["end_time"]):
                    invalid_lines.append(
                        InvalidAnnotation(line=index, content=line, detail="begin_time_lower_than_end_time")
                    )
                    previous_time_info = None
                    continue

                label = elements[2]
                if not label in label_names:
                    previous_time_info["label_id"] = None
                    previous_time_info["invalid_label_text"] = label
                else:
                    label_index = label_names.index(label)
                    label_id = existing_labels[label_index].id
                    previous_time_info["label_id"] = label_id
                    previous_time_info["invalid_label_text"] = None

        except ValueError as error:
            invalid_lines.append(InvalidAnnotation(line=index, content=line, detail=str(error)))
            previous_time_info = None

    return (medialabels_schemas, invalid_lines)
