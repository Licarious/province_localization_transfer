import glob
import codecs

class ProvName:
    ID = ""
    Name = ""
    Language = ""
    def __init__(self, ID):
        self.ID = ""
        self.provList = []
class Translator:
    def __init__(self, ID):
        self.ID = ""
        self.NameList =[]
        self.LanguageList = []

combinedLangList = []
#Get Unique Names from Languages
TranslationBase = glob.glob("Base\\*\\*.yml")

def getProvNames():
    for file in TranslationBase:
        tmpTranslate = codecs.open(file, 'r', 'utf-8-sig')
        lang = file.split("\\")[1] #grabs language
        langList = []
        for line in tmpTranslate:
            if line.startswith(" PROV"):
                if not langList:    #check if list is empty and add firt prov to it
                    prov = ProvName(line.split("\"")[0])
                    prov.ID = line.split("\"")[0]
                    prov.Name = line.split("\"")[1]
                    prov.Language = lang
                    prov.provList.append(prov.ID)
                    
                    langList.append(prov)
                else:
                    nameFound = False
                    for element in langList: #add prov IDs to existing names for when one base language has more Name instances the other base languages
                        if line.split("\"")[1] == element.Name:
                            element.provList.append(line.split("\"")[0])
                            nameFound = True
                            break
                    if not nameFound: # add new unique prov names to list
                        prov = ProvName(line.split("\"")[0])
                        prov.ID = line.split("\"")[0]
                        prov.Name = line.split("\"")[1]
                        prov.Language = lang
                        prov.provList.append(prov.ID)
                    
                        langList.append(prov)


        combinedLangList.append(langList)
    i=0
#Match and Combine localizations
translateList = []

def matchProvNames():
    for lang in combinedLangList:
        for prov in lang:
            if not translateList:   #check if list is empty and add firt prov to it
                NameList = []
                LanguageList = []
                local = Translator(prov.ID)
                local.ID = prov.ID
                local.NameList.append(prov.Name)
                local.LanguageList.append(prov.Language)
                translateList.append(local)
            else:
                #print(prov.Name)
                IDFound = False
                for line in translateList:
                    if line.ID in prov.provList:
                        #print(line.NameList[0])
                        line.NameList.append(prov.Name)

                        line.LanguageList.append(prov.Language)

                        #print(line.NameList)
                        IDFound = True
                        #break
                if not IDFound:
                    NameList = []
                    LanguageList = []
                    local = Translator(prov.ID)
                    local.ID = prov.ID
                    local.NameList.append(prov.Name)
                    local.LanguageList.append(prov.Language)
                    translateList.append(local)
i=0
#Get Input
InputList = []
TranslationInput = glob.glob("Input\\*.yml")

#print(TranslationInput)
#for yml files
def getInputLocal():
    for file in TranslationInput:
        tmpTranslate = codecs.open(file, 'r', 'utf-8-sig')
        tmpList = file.split("_")
        lang = tmpList[len(tmpList)-1].rstrip(".yml")#grabs language
        provNames = []

        for line in tmpTranslate:
            if line.strip().startswith("#") or line.startswith("l_") or line.strip()=="":
                pass
            #if line.startswith(" PROV"):
            else:
                prov = ProvName(line.split("\"")[0])
                prov.ID = line.split("\"")[0]
                prov.Name = line.split("\"")[1]
                prov.Language = lang
                #print(prov.ID)
                InputList.append(prov)
                if not provNames:
                    provNames.append(prov.Name)
                elif prov.Name not in provNames:
                    provNames.append(prov.Name)
        #print(provNames)
    i=0

#output all localizations and error log
def writeLocals(InputList):
    TranslationOutput = glob.glob("Base\\*\\*.yml")
    ErrorFile = codecs.open("error.txt", 'w', 'utf-8-sig')
    ErrorFile.write("The following languages are missing localizations for these province names, so they will not appear in those outputs.")

    for file in TranslationOutput:
        tmpLocalString = "Output" + file.lstrip("Base")
        tmpOutPut = codecs.open(tmpLocalString, 'w', 'utf-8-sig')
        InputLanguate = InputList[0].Language
        TranslateLanguage = file.split("\\")[1] #grabs language
        tmpOutPut.write("l_%s:"%TranslateLanguage)
        #print(TranslateLanguage)
        ErrorFile.write("\n\n%s:"%TranslateLanguage)
        errorList = []

        for name in InputList:
            for lang in translateList:
                if name.Name.startswith("$PROV"):#If it callis for a name by ProvID then it the ID.
                    tmpOutPut.write("\n%s\"%s\""%(name.ID,name.Name))
                    break
                else:
                    try:
                        if lang.NameList[lang.LanguageList.index(InputLanguate)] == name.Name:
                            try:
                                tmpOutPut.write("\n%s\"%s\""%(name.ID,(lang.NameList[lang.LanguageList.index(TranslateLanguage)])))
                            except ValueError:
                                #ErrorFile.write("\n" + name.Name)
                                continue     
                            break
                    except ValueError:
                        #ErrorFile.write("\n" + name.Name)
                        continue  
            else:
                if not name.Name in errorList:
                    errorList.append(name.Name)
        for line in errorList:
            ErrorFile.write("\n" + line)
        tmpOutPut.close()
    ErrorFile.write("\n\n\nThe following keys only contain the following languages:")
    for line in translateList:
        if len(line.NameList) < len(combinedLangList):
            ErrorFile.write("\n\t%s"%line.ID)
            ErrorFile.write("\n\t%s"%line.LanguageList)
            ErrorFile.write("\n\t%s\n"%line.NameList)

    ErrorFile.close()

getProvNames()
matchProvNames()
getInputLocal()
writeLocals(InputList)
