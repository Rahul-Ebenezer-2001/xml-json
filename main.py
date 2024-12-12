import glob
import json
import os
import xml.etree.ElementTree as ET
import xmltodict

# Set directory paths
sourcedirectory = r"C:\Users\Rahul.Ebenezer\OneDrive - WiseTech Global Pty Ltd\Desktop\xml_files"
targetDirectory = r"C:\Users\Rahul.Ebenezer\OneDrive - WiseTech Global Pty Ltd\Desktop\json_files"
separateJsonFolder = os.path.join(targetDirectory, "separate_json_files")
mergedJsonFolder = os.path.join(targetDirectory, "merged_json")
mergedJsonFile = os.path.join(mergedJsonFolder, "merged_output.json")


def merge_json_files(separateJsonFolder, mergedJsonFile):
    all_json_data = []

    json_files = sorted(glob.glob(os.path.join(separateJsonFolder, "*.json")), key=os.path.getmtime)

    for json_file in json_files:
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                all_json_data.extend(data)

        except Exception as e:
            print(f"Error reading or processing file {json_file}: {e}")
    try:
        with open(mergedJsonFile, "w") as merged_file:
            json.dump(all_json_data, merged_file, indent=4)
        print(f"Status: |Success| Merged JSON file created: {mergedJsonFile}")
    except Exception as e:
        print(f"Error saving merged JSON file: {e}")


def process_files(retrieveDirectory, filePattern, separateJsonFolder):
    fileList = sorted(glob.glob(f"{filePattern}"), key=os.path.getmtime)

    for fileName in fileList:
        try:
            file_path = os.path.join(retrieveDirectory, fileName)
            tree = ET.parse(file_path)
            root = tree.getroot()

            merged_xml_content = ET.tostring(root, encoding="unicode")
            x = xmltodict.parse(merged_xml_content)

            output_json_file = os.path.join(separateJsonFolder, f"{os.path.splitext(fileName)[0]}.json")

            with open(output_json_file, "w") as json_file:
                json.dump([x], json_file, indent=4)

            print(f"Status: |Success| JSON file created for {fileName}")
        except Exception as e:
            print(f"Status: |Error| Processing file {fileName} failed.", e)


if __name__ == "__main__":
    if not os.path.exists(separateJsonFolder):
        os.makedirs(separateJsonFolder)
    if not os.path.exists(mergedJsonFolder):
        os.makedirs(mergedJsonFolder)

    os.chdir(sourcedirectory)
    retrieveDirectory = os.getcwd()
    process_files(retrieveDirectory, "*.xml", separateJsonFolder)
    merge_json_files(separateJsonFolder, mergedJsonFile)
