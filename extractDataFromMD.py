#!/usr/bin/env python3 
#-*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from operator import itemgetter
from collections import OrderedDict

import sys, getopt
import json


# Get entityID
def getEntityID(EntityDescriptor, namespaces):
    return EntityDescriptor.get('entityID')


# Get MDUI Descriptions
def getDescriptions(EntityDescriptor,namespaces,entType='idp'):

    description_list = list()
    if (entType.lower() == 'idp'):
       descriptions = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Description", namespaces)
    if (entType.lower() == 'sp'):
       descriptions = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Description", namespaces)

    for desc in descriptions:
        descriptions_dict = dict()
        descriptions_dict['value'] = desc.text
        descriptions_dict['lang'] = desc.get("{http://www.w3.org/XML/1998/namespace}lang")
        description_list.append(descriptions_dict)
    
    return description_list


# Get MDUI Logos
def getLogos(EntityDescriptor,namespaces,entType='idp'):

    logos_list = list()
    if (entType.lower() == 'idp'):
       logo_urls = EntityDescriptor.findall("./md:IDPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Logo", namespaces)
    if (entType.lower() == 'sp'):
       logo_urls = EntityDescriptor.findall("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:Logo", namespaces)

    for logo in logo_urls:
        logo_dict = dict()
        logo_dict['value'] = logo.text
        logo_dict['width'] = logo.get("width")
        logo_dict['height'] = logo.get("height")
        logo_dict['lang'] = logo.get("{http://www.w3.org/XML/1998/namespace}lang")
        logos_list.append(logo_dict)

    return logos_list

# Get ServiceName
def getServiceName(EntityDescriptor,namespaces):
    serviceName = EntityDescriptor.find("./md:SPSSODescriptor/md:AttributeConsumingService/md:ServiceName[@xml:lang='it']", namespaces)
    if (serviceName != None):
       return serviceName.text
    else:
       serviceName = EntityDescriptor.find("./md:SPSSODescriptor/md:AttributeConsumingService/md:ServiceName[@xml:lang='en']", namespaces)
       if (serviceName != None):
          return serviceName.text
       else:
          return ""


# Get Organization Name
def getOrgName(EntityDescriptor, namespaces):
    orgName = EntityDescriptor.find("./md:Organization/md:OrganizationName[@xml:lang='it']",namespaces)

    if (orgName != None):
       return orgName.text
    else:
       orgName = EntityDescriptor.find("./md:Organization/md:OrganizationName[@xml:lang='en']",namespaces)
       if (orgName != None):
          return orgName.text
       else:
          return ""

# Get Information Page URL
def getInformationURL(EntityDescriptor,namespaces):
    info = EntityDescriptor.find("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:InformationURL[@xml:lang='it']",namespaces)
    if (info != None):
       return info.text
    else:
       info = EntityDescriptor.find("./md:SPSSODescriptor/md:Extensions/mdui:UIInfo/mdui:InformationURL[@xml:lang='en']",namespaces)
       if (info != None):
          return info.text
       else:
          return ""


# Get Organization page URL
def getOrganizationURL(EntityDescriptor,namespaces):

    orgUrl = EntityDescriptor.find("./md:Organization/md:OrganizationURL[@xml:lang='it']",namespaces)
    if (orgUrl != None):
       return orgUrl.text
    else:
       orgUrl = EntityDescriptor.find("./md:Organization/md:OrganizationURL[@xml:lang='en']",namespaces)
       if (orgUrl != None):
          return orgUrl.text
       else:
          return ""


# Get RequestedAttribute
def getRequestedAttribute(EntityDescriptor,namespaces):
    reqAttr = EntityDescriptor.findall("./md:SPSSODescriptor/md:AttributeConsumingService/md:RequestedAttribute", namespaces)

    requestedAttributes = list()

    if (reqAttr != None):
       for ra in reqAttr:
           if (ra.get('isRequired') == "true"):
              requestedAttributes.append(ra.get('FriendlyName')+"(O)")
           else:
              requestedAttributes.append(ra.get('FriendlyName')+"(R)")

    return requestedAttributes


def main(argv):
   try:
      # 'm:o:hd' means that 'm' and 'o' needs an argument(confirmed by ':'), while 'h' and 'd' don't need it
      opts, args = getopt.getopt(sys.argv[1:], 'm:o:hd', ['metadata=','output=','help','debug' ])
   except getopt.GetoptError as err:
      print (str(err))
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The JSON content will be put in the output file")
      sys.exit(2)

   inputfile = None
   outputfile = None
   idp_outputfile = None

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
         print ("The JSON content will be put in the output file")
         sys.exit()
      elif opt in ('-m', '--metadata'):
         inputfile = arg
      elif opt in ('-o', '--output'):
         outputfile = arg
      elif opt == '-d':
         global _debug
         _debug = 1
      else:
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
         print ("The JSON content will be put in the output file")
         sys.exit()

   namespaces = {
      'xml':'http://www.w3.org/XML/1998/namespace',
      'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
      'mdrpi': 'urn:oasis:names:tc:SAML:metadata:rpi',
      'shibmd': 'urn:mace:shibboleth:metadata:1.0',
      'mdattr': 'urn:oasis:names:tc:SAML:metadata:attribute',
      'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
      'ds': 'http://www.w3.org/2000/09/xmldsig#',
      'mdui': 'urn:oasis:names:tc:SAML:metadata:ui'
   }

   if inputfile == None:
      print ("Metadata file is missing!\n")
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The JSON content will be put in the output file")
      sys.exit()

   if outputfile == None:
      print ("Output file is missing!\n")
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_file>")
      print ("The JSON content will be put in the output file")
      sys.exit()


   tree = ET.parse(inputfile)
   root = tree.getroot()
   sp = root.findall("./md:EntityDescriptor[md:SPSSODescriptor]", namespaces)

   sps = dict()

   list_sps = list()

   cont_id = 0

   for EntityDescriptor in sp:

      cont_id = cont_id + 1
      #pp_flag = "Privacy Policy assente"
      #info_flag = "Info Page assente"
      #logo_flag = "Logo non presente"

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get ServiceName ENG
      serviceName = getServiceName(EntityDescriptor,namespaces)

      # Get MDUI Privacy Policy
      #pp_list = getPrivacyStatementURLs(EntityDescriptor,namespaces,'idp')

      #if (len(pp_list) != 0):
      #   pp_flag = 'Privacy Policy presente'

      # Get SP Information Page
      #infoUrl = getInformationURL(EntityDescriptor,namespaces)

      # Get Organization Page     
      orgUrl = getOrganizationURL(EntityDescriptor,namespaces)

      # Get MDUI Logos
      #logos_list = getLogos(EntityDescriptor,namespaces,'sp')

      #if (len(logos_list) != 0):
      #   logo_flag = 'Logo presente'

      # Get RequestedAttribute
      requestedAttributes = getRequestedAttribute(EntityDescriptor,namespaces)

      #Get Organization Name
      orgName = getOrgName(EntityDescriptor,namespaces)

      sp = OrderedDict([
        ('id',cont_id),
        ('IdemResource_name',serviceName),
        ('IdemResource_serviceUrlOne', orgUrl),
        ('IdemResource_uri',', '.join(requestedAttributes)),
        ('IdemAccession_name',orgName)
      ])

      list_sps.append(sp)

   
   result_sps = open(outputfile, "w",encoding=None)
   result_sps.write(json.dumps(sorted(list_sps,key=itemgetter('id')),sort_keys=False, indent=None, ensure_ascii=False,separators=(',', ':')))
   result_sps.close()


if __name__ == "__main__":
   main(sys.argv[1:])
