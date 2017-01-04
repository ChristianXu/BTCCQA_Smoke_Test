__author__ = 'sara'
import os
import yaml
from xml.etree import ElementTree as elementTree

activity = {}


def set_xml():
    """
    get the xml file's value
    :use:
    a = getXml(path)

    print(a.get(".module.GuideActivity").get("skip").get("type"))
    :param: xmlPath
    :return:activity
    """
    if len(activity) == 0:

        xml_path = os.path.join("/Users/sara/PycharmProjects/autoTest", "config", "spot_usd", "element.xml")
        # open the xml file
        per = elementTree.parse(xml_path)
        all_element = per.findall('web_page')

        for firstElement in all_element:
            activity_name = firstElement.get("name")

            element = {}

            for secondElement in firstElement.getchildren():
                element_name = secondElement.get("name")

                element_child = {}
                for thirdElement in secondElement.getchildren():

                    element_child[thirdElement.tag] = thirdElement.text

                element[element_name] = element_child
            activity[activity_name] = element


set_xml()

print(activity)
stream = open("element.yaml", 'w')

yaml.dump(activity, stream)

stream.close()
