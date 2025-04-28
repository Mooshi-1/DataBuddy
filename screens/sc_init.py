import fitz
import sys
import os
import re
from enum import Enum

# Define regex patterns for each method
# add control in eventually....
patterns = {
    "LCMSMS": re.compile(r'([A-Za-z]{0,2})(\d{2})-(\d{4})'),
    "SCRNZ": re.compile(r'([A-Za-z]{0,2}\d+-\d+_.+ [AB])')
}
patternsQC = {
    "Sequence": re.compile(r'sequence', re.IGNORECASE),
    "Control": re.compile(r'(\w CTL)', re.IGNORECASE)
}

# Define a mapping of methods to subclass constructors
subclass_map = {
    "LCMSMS": lambda caseNum, path: LCMSMS(caseNum, path),
    "SCRNZ": lambda caseNum, path: SCRNZ(caseNum, path)
}

class FileType(Enum):
    topSheet = "Top Sheet"
    detailSheet = "Detail Sheet"
    amdisSheet = "AMDIS Sheet"
    topSheetRI = "RI Top Sheet"
    detailRI = "RI Detail Sheet"
    amdisRI = "RI AMDIS Sheet"
    unknown = "UNKNOWN"
    

# merge reinject case numbers into base case
# detailed printout
#   caseNum     topSheet    detail1
#   2025-001     check         X
# format for terminal

# class BatchFile():
#     def __init__(self, type, path):
#         self.type = type
#         self.paths = [path]

class CaseFile():
    def __init__(self, caseNum, path):
        self.caseNum = caseNum
        self.paths = [path]

    def order(self):
        return
        
    
    def assignType(self):
        #key:value -- value=list, iterate list
        return

    def bind(self):
        return
    
    def checkCompletion(self):
        #print whether all parts are there
        return
    
    def findChild(self):
        return
    
    def findParent(self):
        return
    
    def findReinjects(self):
        return
    
class BatchFile(CaseFile):
    def __init__(self, caseNum, path):
        super().__init__(caseNum, path)    
    
class SCRNZ(CaseFile):
    def __init__(self, caseNum, path):
        super().__init__(caseNum, path)
        self.assignments = {}

    def order(self):
        self.ordered = {ftype: self.assignments.get(ftype, []) for ftype in FileType}


        self.checkCompletion()
        for types, paths in self.ordered.items():
            print(f"{types}: {paths}")

    def bind(self, outputDir, batch):
        #for Z specific binding, get A/N pair and continue to merge
        fullName = os.path.join(outputDir, f"{self.caseNum}_{batch}.pdf")
        
        mergedDoc = fitz.open()

        for types, paths in self.ordered.items():
            for path in paths:
                with fitz.open(path) as sourceDoc:
                    mergedDoc.insert_pdf(sourceDoc)

        mergedDoc.save(fullName)
        mergedDoc.close()




    def assignType(self):
        for path in self.paths:
#initialize assignment. Check for identifier, assign type, check type - change if needed, append.
            assignment=None
            lines = fitz_get_lines_pg1(path)
            if "SCRNZ Report (Not For Quantitative Purposes)" in lines:
                # how to sort acids/bases?
                assignment = FileType.topSheet

            elif "YYY" in lines:
                assignment = FileType.detailBase
                
            elif "ZZZ" in lines:
                assignment = FileType.amdisBase

            if not assignment:
                assignment = FileType.unknown
                print(f'added unknown file type for {path}')

            if assignment in self.assignments:
                    self.assignments[assignment].append(path)
            else:
                self.assignments[assignment] = [path]

    
    def checkCompletion(self):
        methodRequirements = {
            FileType.topSheet: 1,
            FileType.detailSheet: float('inf'),
            FileType.amdisSheet: 1,
        }
        for ftype, requiredCount in methodRequirements.items():
            assignedFiles = self.ordered.get(ftype, [])
            assignedCount = len(assignedFiles)
            
            if assignedCount > requiredCount:
                print(f"Extra Files Found for {ftype}. Select a file to remove", flush=True)
                print("0. Keep all files")
                for i, path in enumerate(assignedFiles, start=1):
                    print(f"{i}. {path}")
                print("Choose an option: ", flush=True)
                answer = int(input())
                if answer == 0:
                    continue
                elif 1 <= answer <= len(assignedCount):
                    remove = assignedFiles.pop(answer - 1)
                    print(f"removed {remove} from {ftype}")
            elif assignedCount < requiredCount:
                print(f"missing files for {ftype} in {self.caseNum}, expecting {requiredCount} not {assignedCount}")
                #implement logic to quit/add more files


class LCMSMS(CaseFile):
    def __init__(self, caseNum, path):
        super().__init__(caseNum, path)

def fitz_get_lines_pg1(path):
    doc = fitz.open(path)
    page = doc[0]
    text = page.get_text().strip()
    #lines = text.split('\n')
    doc.close()
    return text


def getCases(method, currentDir="./", outputDir="./"):
    #hold files to process in {caseNumber: object} dict
    caseDict = {}
    #assign casenumber searching pattern
    pattern = patterns.get(method)
    pdfFilesFound = 0
    #iterate and find files
    for file in os.listdir(currentDir):
        if file.endswith(".pdf"):
            pdfFilesFound += 1
            pdfPath = os.path.join(currentDir, file)
            lines = fitz_get_lines_pg1(pdfPath)
            print(lines)
            caseNum = None
            try: 
                for patternKey in [method, "Sequence", "Control"]:
                    pattern = patterns.get(method) if patternKey == method else patternsQC.get(patternKey)
                    match = pattern.search(lines)
                    if match:
                        caseNum = match.group()
                        break
                if not caseNum:
                    print(f"No case number identified for {file}")
                print(f"caseNum = {caseNum}")
            except:
                print("REGEX ERROR")
            #replace file with extracted name
            #caseNum = str(caseNum)
            if caseNum in caseDict:
                caseDict[caseNum].paths.append(pdfPath)
                print(f"{pdfPath} added to self.path for {caseNum}")
                
            else:
                constructor = subclass_map.get(method)
                caseDict[caseNum] = constructor(caseNum, pdfPath)
                print(f"new dict entry {caseNum} created")
            print(f"casedict {pdfFilesFound} complete")
    return caseDict

def main(method):

    currentDir = None
    outputDir = None
    batchNum = "111"

    #maybe separate into separate QC dict?
    #still need to catch sequence from getting scooped into cases
    caseDict = getCases(method)

    print("--starting object sort phase--")

    for case in caseDict.keys():
        print(f"processing {case}")
        #order automatically called by assignType() method
        caseDict[case].assignType()
        caseDict[case].order()
        caseDict[case].checkCompletion()
        caseDict[case].bind(outputDir, batchNum)



if __name__ == "__main__":
    print(sys.argv)
    main("SCRNZ")