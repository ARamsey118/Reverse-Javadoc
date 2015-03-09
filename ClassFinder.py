#!/usr/bin/python3
import ReverseDoc
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error


class Java():
    """
    Holds a java class with its location.
    """
    def __init__(self):
        self.name = ""
        self.location = ""

    def __str__(self):
        return self.location


def findClasses(soup):
    """
    Used to locate all classes in the javadoc. Also keeps track of each classes location to determine packages.
    :param soup: HTML of the overview-tree page.
    :return: list containing Java class objects
    """
    classes = soup.find("h2", {"title": "Class Hierarchy"}) #gets the tag for the class list
    java_class_list = list()
    if classes:
        classes = classes.findNext("ul").findNext('ul') #move down to the class list, skipping the object subsection
        class_list = classes.find_all("li") #list of classes
        for java_class in class_list:
            new_class = Java()
            new_class.name = str(java_class.find("span", {"class": "typeNameLink"}).text)
            new_class.location = str(java_class.find("a").get("href"))
            java_class_list.append(new_class)
    return java_class_list


def findInterfaces(soup):
    """
    Just like findClasses, but for interfaces
    :param soup: HTML of the overview-tree page.
    :return: list containing java class objects.
    """
    #TODO combine with findClasses
    interfaces = soup.find("h2", {"title": "Interface Hierarchy"})
    interface_list = list()
    if interfaces:
        interfaces = interfaces.findNext("ul")
        temp_list = interfaces.find_all("li")
        for temp_class in temp_list:
            new_class = Java()
            new_class.name = str(temp_class.find("span", {"class": "typeNameLink"}).text)
            new_class.location = str(temp_class.find("a").get("href"))
            interface_list.append(new_class)
    return interface_list


def main():
    # htmlfile = input("Enter url to main doc page: ")
    # output = input("Enter complete location to output src files: ")
    # htmlfile = "http://www.cs.rit.edu/~csci142/Projects/01/doc/"
    htmlfile = "http://www.cs.rit.edu/~csci142/Labs/03/Doc/"
    output = "/home/andrew/java"
    # output = "/home/andrew/school/CS142/4BankAccount/Lab4"
    # output = "/home/andrew/school/CS142/1Perp/Project1"
    javafile = htmlfile.replace("doc", "src") #look for any given code
    if htmlfile[-1] != "/": #add slashes as appropriate
        htmlfile += "/"
    if output[-1] != "/":
        output += "/"
    output += "src/" # put the output in a directory called src
    htmltext = urllib.request.urlopen(htmlfile + "overview-tree.html").read()
    soup = BeautifulSoup(htmltext)
    class_list = findClasses(soup)
    interface_list = findInterfaces(soup)
    #TODO make this a function and pass it interface or class as appropriate
    for java_class in class_list:
        try: #check if source is given
            new_class = (urlopen(javafile + java_class.location.replace("html", "java")).read(), "try") #tuple to tell it which type of printing is required
        except:
            new_class = (
                ReverseDoc.ReverseDoc(urllib.request.urlopen(htmlfile + java_class.location).read(), htmlfile), "except")
        path = os.path.join(output, java_class.location.replace(".html", "") + ".java")
        dirpath = path.rsplit("/", 1)[0] + "/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(path, "w") as f:
            #TODO see if the decoding or printing can be done at creation to remove if else
            if new_class[1] == "try":
                f.write(new_class[0].decode("utf-8"))
            else:
                f.write(new_class[0].__repr__(False)) #telling it to print as a class
    for interface in interface_list:
        try:
            new_interface = (urlopen(javafile + interface.location.replace("html", "java")).read(), "try")
        except urllib.error.HTTPError:
            new_interface = (
                ReverseDoc.ReverseDoc(urllib.request.urlopen(htmlfile + interface.location).read(), htmlfile), "except")
        path = os.path.join(output, interface.location.replace(".html", "") + ".java")
        dirpath = path.rsplit("/", 1)[0] + "/"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(path, "w") as f:
            if new_interface[1] == "try":
                f.write(new_interface[0].decode("utf-8"))
            else:
                f.write(new_interface[0].__repr__(True)) #telling it to print as an interface


if __name__ == '__main__':
    main()