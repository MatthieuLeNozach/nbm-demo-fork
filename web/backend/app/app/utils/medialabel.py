import re
from app import crud
from app.schemas import MediaLabelCreate, InvalidAnnotation

def get_medialabel_schemas_from_file_content(
    content: str,
    media_id: int,
    existing_labels: list
):
    label_names = list(map(lambda existing_label: existing_label.name, existing_labels))

    medialabels_schemas = []
    invalid_lines = []
    invalid_labels = []

    previous_time_info = None #store time info before merge it with frequencies info

    lines = content.splitlines()
    for index, line in enumerate(lines):

        elements = re.split(r'\t+', line.decode('utf-8')) #split by tabulation

        if (len(elements) != 3):
            invalid_lines.append(InvalidAnnotation(line=index, content=line))
            continue

        try:
            if (elements[0] == "\\"
                    and type(float(elements[1])) is float
                    and type(float(elements[2])) is float): #line data matches to frequencies

                if (type(previous_time_info) is not dict): #there was no valid time data on previous line
                    continue

                medialabel_in = MediaLabelCreate(begin_time=previous_time_info["begin_time"],
                                        end_time=previous_time_info["end_time"],
                                        label_id=previous_time_info["label_id"],
                                        low_freq=float(elements[1]),
                                        high_freq=float(elements[2]),
                                        media_id=media_id)
                medialabels_schemas.append(medialabel_in)

                previous_time_info = None

            elif (type(float(elements[0])) is float
                    and type(float(elements[1])) is float
                    and type(elements[2]) is str): #line data matches to time info and label

                if (type(previous_time_info) is dict): # if there is no frequencies associated to previous annotation
                    medialabel_in = MediaLabelCreate(begin_time=previous_time_info["begin_time"],
                                            end_time=previous_time_info["end_time"],
                                            label_id=previous_time_info["label_id"],
                                            media_id=media_id)
                    medialabels_schemas.append(medialabel_in)

                label = elements[2]

                if not label in label_names:
                    invalid_labels.append({"line": index, "content": label})
                    continue

                label_index = label_names.index(label)
                label_id = existing_labels[label_index].id
                previous_time_info = { "begin_time": float(elements[0]),
                                        "end_time": float(elements[1]),
                                        "label_id": label_id, }

        except ValueError:
            invalid_lines.append(InvalidAnnotation(line=index, content=line))

    return (medialabels_schemas, invalid_lines, invalid_labels)
