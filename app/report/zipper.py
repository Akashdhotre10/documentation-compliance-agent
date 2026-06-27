import zipfile
import os
import glob


class ReportZipper:

    def create_zip(self):

        os.makedirs("downloads", exist_ok=True)

        zip_path = "downloads/compliance_reports.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for file in glob.glob("reports/*.html"):

                zipf.write(
                    file,
                    os.path.basename(file)
                )

        return zip_path