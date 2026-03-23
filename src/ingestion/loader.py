import os
import glob
from pypdf import PdfReader


class DataLoader:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir

    def load_documents(self):

        search_pattern = os.path.join(self.data_dir, "**/*.pdf")


        files = glob.glob(search_pattern, recursive=True)

        if not files:
            print(f"    No PDFs found inside {self.data_dir}")

        for filepath in files:
            filename = os.path.basename(filepath)

            try:

                reader = PdfReader(filepath)
                text = ""


                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

                yield filename, text

            except Exception as e:
                print(f"    Failed to read {filename}: {e}")
                yield filename, ""