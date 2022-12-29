import datetime
import os.path

class Mytime:
    def __init__(self, thisday):
        self.thisday = thisday
        self.path1 = os.path.join('', 'CleanList.txt')
        self.todaylist = list()
        self.selected_action = list()

    def __repr__(self):
        return f'{self.thisday}'

    def get_tasks_today(self, thisday, todaylist):   # повертає список сьогоднішніх справ
        file1 = open(self.path1, "r")
        list1 = file1.readlines()
        for element1 in list1:
            if thisday == "Monday":
                if element1.startswith("Monday"):
                    self.todaylist.append(element1)
            elif thisday == "Tuesday":
                if element1.startswith("Tuesday"):
                    self.todaylist.append(element1)
            elif thisday == "Wednesday":
                if element1.startswith("Wednesday"):
                    self.todaylist.append(element1)
            elif thisday == "Thursday":
                if element1.startswith("Thursday"):
                    self.todaylist.append(element1)
            elif thisday == "Friday":
                if element1.startswith("Friday"):
                    self.todaylist.append(element1)
            elif thisday == "Saturday":
                if element1.startswith("Saturday"):
                    self.todaylist.append(element1)
            elif thisday == "Sunday":
                if element1.startswith("Sunday"):
                    self.todaylist.append(element1)
        file1.close()
        return self.todaylist

    def get_high(self, todaylist, myid):
        nowtime = (datetime.datetime.now()).strftime("%x")
        for element2 in todaylist:
            elementS = element2.split(" - ")
            if elementS[1] == "High":
                elementS.remove(elementS[0])
                elementS.remove(elementS[0])
                for element21 in elementS:
                    path2 = os.path.join("", myid + "now.txt")
                    file2 = open(path2, "a")
                    file2.write(element21 + "\n")
                    file2.close()
            else:
                if elementS[1] == "Medium" or elementS[1] == "Low":
                    elementS.remove(elementS[0])
                    elementS.remove(elementS[0])
                    for element22 in elementS:
                        element23 = element22.rstrip("\n")
                        path2 = os.path.join("", myid + "future.txt")
                        file2 = open(path2, "a")
                        file2.write(element23 + " - Not done since: " + ((datetime.datetime.now()).strftime("%x")) + "\n")
                        file2.close()
        self.todaylist.clear()
        return self.todaylist

    def get_medium(self, todaylist, myid):
        for element2 in todaylist:
            element16 = element2.split(" - ")
            if element16[1] == "High" or element16[1] == "Medium":
                element16.remove(element16[0])
                element16.remove(element16[0])
                for element21 in element16:
                    element23 = element21.rstrip("\n")
                    path2 = os.path.join("", myid + "now.txt")
                    file2 = open(path2, "a")
                    file2.write(element23 + "\n")
                    file2.close()
            else:
                if element16[1] == "Low":
                    element16.remove(element16[0])
                    element16.remove(element16[0])
                    for element22 in element16:
                        element23 = element22.rstrip("\n")
                        path2 = os.path.join("", myid + "future.txt")
                        file2 = open(path2, "a")
                        file2.write(element23 + " - Not done since: " + ((datetime.datetime.now()).strftime("%x")) + "\n")
                        file2.close()
        self.todaylist.clear()
        return self.todaylist

    def get_low(self, todaylist, myid):
        for element2 in todaylist:
            element17 = element2.split(" - ")
            element17.remove(element17[0])
            element17.remove(element17[0])
            for element21 in element17:
                element23 = element21.rstrip("\n")
                path2 = os.path.join("", myid + "now.txt")
                file2 = open(path2, "a")
                file2.write(element23 + "\n")
                file2.close()
        self.todaylist.clear()
        return self.todaylist

    def get_selected_action(self, selected_action, myid):
        path2 = os.path.join("", myid + "now.txt")
        file2 = open(path2, "r")
        self.selected_action = file2.readlines()
        file2.close()
        return self.selected_action


mytime = Mytime((datetime.datetime.now()).strftime("%A"))

