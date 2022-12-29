import datetime
import os.path

class Delayed:
    def __init__(self, status):
        self.status = status
        self.delayed_today_list = list()
        self.list_notdone = list()

    def get_delayed_list(self, delayed_today_list, myid):             #повертає список незроблених сьогодні справ з датою
        path2 = os.path.join("", myid + "future.txt")
        file2 = open(path2, "a")
        for element in delayed_today_list:
            elem = element.rstrip("\n")
            not_done = elem + " - Not done since: " + ((datetime.datetime.now()).strftime("%x"))
            self.list_notdone.append(not_done)
            self.list_notdone = list(set(self.list_notdone))
        for x in self.list_notdone:
            file2.write(x + " - Not done since: " + ((datetime.datetime.now()).strftime("%x")) + "\n")
        file2.close()
        return self.list_notdone

    def append_to_delayed(self, myid, delayed_today_list):
        path2 = os.path.join("", myid + "now.txt")
        file2 = open(path2, "r")
        list2 = file2.readlines()
        file2.close()
        path2 = os.path.join("", myid + "now.txt")
        file2 = open(path2, "r+")
        file2.truncate()
        file2.close()
        for element in list2:
            self.delayed_today_list.append(element)
        self.delayed_today_list = list(set(self.delayed_today_list))
        return self.delayed_today_list

    def common_report(self, myid): #43
        list5 = list()
        path = os.path.join("", myid + "future.txt")
        file = open(path, "r")
        list4 = file.readlines()
        file.close()
        for element1 in list4:
            element2 = element1.split(" - ")
            element3 = element2[0] + " - " + element2[1]
            element4 = element3.rstrip("\n")
            list5.append(element4)
        status_list = list(set(list5))
        if len(status_list) == 0:
            self.status = "Your place is perfectly clean"
        elif len(status_list) > 0 and len(status_list) <= 10:
            self.status = "Your place is clean, but there are some details to be done"
        elif len(status_list) >= 11 and len(status_list) <= 20:
            self.status = "Your close isn't clean. Not also dirty"
        elif len(status_list) >=21 and len(status_list) <=30:
            self.status = "You have to clean your place immediately!!!"
        else:
            self.status = "Call to cleaning service. You won't manage it yourself"
        return self.status



delayed = Delayed(None)