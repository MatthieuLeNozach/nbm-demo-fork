import shutil, csv, os, zipfile, requests
from pathlib import Path
from app.core.config import settings

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                        os.path.join(path, '..')))


def generate_mediae_zip(mediae, zip_name):
    temp_folder = settings.TMP_PATH
    shutil.rmtree(temp_folder)

    annotations_temp_folder = f"{temp_folder}annotations/"
    Path(annotations_temp_folder).mkdir(parents=True, exist_ok=True)
    annotation_file_path = f"{annotations_temp_folder}annotations.csv"
    with open(annotation_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow( ('t_start', 't_end', 'f_start', 'f_end', 'species', 'filename') )

        mediae_temp_folder = f"{temp_folder}mediae/"
        Path(mediae_temp_folder).mkdir(parents=True, exist_ok=True)

        for media in mediae:

            for medialabel in media.medialabels:
                if medialabel.label is not None:
                    label_name = medialabel.label.name
                    if medialabel.label.species:
                        label_name = medialabel.label.species.name
                    writer.writerow( (
                        medialabel.begin_time,
                        medialabel.end_time,
                        medialabel.low_freq,
                        medialabel.high_freq,
                        label_name,
                        os.path.basename(media.file_url),
                    ) )

            response = requests.get(f"{settings.NEXTCLOUD_HOST}/remote.php/dav/files/{settings.NEXTCLOUD_USER}/{media.file_url}",
                                    auth=(settings.NEXTCLOUD_USER, settings.NEXTCLOUD_PASSWORD))
            if response.status_code == 200:
                with open(f"{mediae_temp_folder}{os.path.basename(media.file_url)}", "wb") as f:
                    f.write(response.content)
                    f.close()

    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(mediae_temp_folder, zipf)

    zipf.write(annotation_file_path, os.path.basename(annotation_file_path))

    zipf.close()

    shutil.rmtree(mediae_temp_folder)
    shutil.rmtree(annotations_temp_folder)
