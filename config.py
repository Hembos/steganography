import xml.etree.ElementTree as ET
from work import Work, WorkType, FileWorkType


def read_works(config_file_name: str) -> list:
    tree = ET.parse(config_file_name)
    root = tree.getroot()
    
    works = []

    for workInfo in root.findall('work'):
        work = Work()
        work.type = WorkType[workInfo.find('type').text]
        work.fileType = FileWorkType[workInfo.find('file_type').text]
        work.inFile = workInfo.find('inFile').text
        work.toFile = workInfo.find('toFile').text
        work.outFile = workInfo.find('outFile').text

        works.append(work)

    return works
