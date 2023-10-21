from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import calendar, pickle, pydrive2.auth, json
from datetime import *

class ScheduleGoogleDrive():
    def __init__(self):
        try:
            self.gauth = GoogleAuth()
            self.gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(self.gauth)
        except pydrive2.auth.RefreshError:
            with open("./credentials.json", "r+") as path: path.truncate(0)
            self.gauth = GoogleAuth()
            self.gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(self.gauth)

        toplist = self.drive.ListFile({"q": "title = 'Scheduler' and trashed=false"}).GetList()
        if len(toplist)==0:
            metadata = {
                "title": "Scheduler",
                "mimeType": "application/vnd.google-apps.folder"
            }
            f = self.drive.CreateFile(metadata)
            f.Upload() 
            

    def getPickleFile(self, YearMonthDay):
        dateList = str(YearMonthDay).split("-")
        files = self.drive.ListFile({'q': "title='%s' and trashed=false" % f"{dateList[0]}/{dateList[1]}/{dateList[2]}.pickle"}).GetList()
        folders = self.drive.ListFile({'q': "title='%s' and mimeType='application/vnd.google-apps.folder' and trashed=false" % f"{dateList[0]}"}).GetList()
        day = "defaultScheduleData"
        # calendar.day_name[datetime.strptime(YearMonthDay, "%Y-%m-%d").date().weekday()].lower()
        # When the folder for the year hasn't been made and thus no file for the day exists
        if len(folders) == 0:
            toplist = self.drive.ListFile({"q": "title = 'Scheduler' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
            assert len(toplist) == 1
            self.scheduleID = toplist[0]["id"]
            f = self.drive.CreateFile({"title": f"{dateList[0]}",
                                   "parents": [{"id": self.scheduleID}],
                                   "mimeType": 'application/vnd.google-apps.folder'})
            f.Upload()
            p = self.drive.CreateFile({"title": f"{dateList[0]}/{dateList[1]}/{dateList[2]}.pickle",
                                   "parents": [{"id": f["id"]}]})
            p.SetContentFile(day+".pickle")
            p.Upload()
        # When the pickle file for the day doesn't exist
        elif len(files)==0:
            if len(folders) != 1: print(F"\n\n\nError with loading from drive, multiple duplicates of a folder")
            p = self.drive.CreateFile({"title": f"{dateList[0]}/{dateList[1]}/{dateList[2]}.pickle",
                                   "parents": [{"id": folders[0]["id"]}]})
            p.SetContentFile(day+".pickle")
            p.Upload()
        # If the file exists, get the file
        else:
            if len(files) != 1: print(F"\n\n\nError with loading from drive, multiple duplicates of a file")
            p = files[0]
        return p
    