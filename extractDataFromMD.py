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
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    descriptions = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Description" % entityType, namespaces)

    if (len(descriptions) != 0):
       for desc in descriptions:
           descriptions_dict = dict()
           descriptions_dict['value'] = desc.text
           descriptions_dict['lang'] = desc.get("{http://www.w3.org/XML/1998/namespace}lang")
           description_list.append(descriptions_dict)
    
    return description_list


# Get MDUI Logo BIG
def getLogoBig(EntityDescriptor,namespaces,entType='idp'):

    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"
    
    logoUrl = ""
    logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo[@xml:lang='it']" % entityType,namespaces)
    if (len(logos) != 0):
       for logo in logos:
           logoHeight = logo.get("height")
           logoWidth = logo.get("width")
           if (logoHeight != logoWidth):
              # Avoid "embedded" logos
              if ("data:image" in logo.text):
                 logoUrl = "embeddedLogo"
                 return logoUrl
              else:
                 logoUrl = logo.text
                 return logoUrl
    else:
       logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo[@xml:lang='en']" % entityType,namespaces)
       if (len(logos) != 0):
          for logo in logos:
              logoHeight = logo.get("height")
              logoWidth = logo.get("width")
              if (logoHeight != logoWidth):
                 # Avoid "embedded" logos
                 if ("data:image" in logo.text):
                    logoUrl = "embeddedLogo"
                    return logoUrl
                 else:
                    logoUrl = logo.text
                    return logoUrl
       else:
           logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo" % entityType,namespaces)
           if (len(logos) != 0):
              for logo in logos:
                  logoHeight = logo.get("height")
                  logoWidth = logo.get("width")
                  if (logoHeight != logoWidth):
                     # Avoid "embedded" logos
                     if ("data:image" in logo.text):
                        logoUrl = "embeddedLogo"
                        return logoUrl
                     else:
                        logoUrl = logo.text
                        return logoUrl
           else:
              return ""


# Get MDUI Logo SMALL
def getLogoSmall(EntityDescriptor,namespaces,entType='idp'):
    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"
    
    logoUrl = ""
    logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo[@xml:lang='it']" % entityType,namespaces)
    if (len(logos) != 0):
       for logo in logos:
           logoHeight = logo.get("height")
           logoWidth = logo.get("width")
           if (logoHeight == logoWidth):
              # Avoid "embedded" logos
              if ("data:image" in logo.text):
                 logoUrl = "embeddedLogo"
                 return logoUrl
              else:
                 logoUrl = logo.text
                 return logoUrl
    else:
       logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo[@xml:lang='en']" % entityType,namespaces)
       if (len(logos) != 0):
          for logo in logos:
              logoHeight = logo.get("height")
              logoWidth = logo.get("width")
              if (logoHeight == logoWidth):
                 # Avoid "embedded" logos
                 if ("data:image" in logo.text):
                    logoUrl = "embeddedLogo"
                    return logoUrl
                 else:
                    logoUrl = logo.text
                    return logoUrl
       else:
           logos = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:Logo" % entityType,namespaces)
           if (len(logos) != 0):
              for logo in logos:
                  logoHeight = logo.get("height")
                  logoWidth = logo.get("width")
                  if (logoHeight == logoWidth):
                     # Avoid "embedded" logos
                     if ("data:image" in logo.text):
                        logoUrl = "embeddedLogo"
                        return logoUrl
                     else:
                        logoUrl = logo.text
                        return logoUrl
           else:
              return ""


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


# Get DisplayName
def getDisplayName(EntityDescriptor, namespaces, entType='idp'):

    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    orgName = EntityDescriptor.find("%s/md:Extensions/mdui:DisplayName[@xml:lang='it']" % entityType,namespaces)

    if (orgName != None):
       return orgName.text
    else:
       orgName = EntityDescriptor.find("%s/md:Extensions/mdui:DisplayName[@xml:lang='en']" % entityType,namespaces)
       if (orgName != None):
          return orgName.text
       else:
          if (entType == 'sp'):
             orgName = getServiceName(EntityDescriptor,namespaces)
             if (orgName != None):
                return orgName
             else:
                return ""
          else:
             orgName = getOrgName(EntityDescriptor,namespaces)
             return orgName

    
# Get MDUI InformationURLs
def getInformationURLs(EntityDescriptor,namespaces,entType='idp'):
    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    info_list = list()
    info_pages = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:InformationURL" % entityType, namespaces)

    for infop in info_pages:
        info_dict = dict()
        lang = infop.get("{http://www.w3.org/XML/1998/namespace}lang")
        info_dict[lang] = infop.text
        info_list.append(info_dict)

    return info_list


# Get MDUI PrivacyStatementURLs
def getPrivacyStatementURLs(EntityDescriptor,namespaces,entType='idp'):
    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    privacy_list = list()
    privacy_pages = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementURL" % entityType, namespaces)

    for pp in privacy_pages:
        privacy_dict = dict()
        lang = pp.get("{http://www.w3.org/XML/1998/namespace}lang")
        privacy_dict[lang] = pp.text
        privacy_list.append(privacy_dict)

    return privacy_list


# Gen InformationURL
def getInformationURL(EntityDescriptor,namespaces,entType='sp'):

    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    info = EntityDescriptor.find("%s/md:Extensions/mdui:UIInfo/mdui:InformationURL[@xml:lang='it']" % entityType,namespaces)
    if (info != None):
       return info.text
    else:
       info = EntityDescriptor.find("%s/md:Extensions/mdui:UIInfo/mdui:InformationURL[@xml:lang='en']" % entityType,namespaces)
       if (info != None):
          return info.text
       else:
          return ""


# Gen PrivacyStatementURL
def getPrivacyStatementURL(EntityDescriptor,namespaces,entType='sp'):

    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    info = EntityDescriptor.find("%s/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementURL[@xml:lang='it']" % entityType,namespaces)
    if (info != None):
       return info.text
    else:
       info = EntityDescriptor.find("%s/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementeURL[@xml:lang='en']" % entityType,namespaces)
       if (info != None):
          return info.text
       else:
          return ""


# GET OrganizationURL
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

    if (len(reqAttr) != 0):
       for ra in reqAttr:
           if (ra.get('isRequired') == "true"):
              requestedAttributes.append(ra.get('FriendlyName')+"(O)")
           else:
              requestedAttributes.append(ra.get('FriendlyName')+"(R)")

    return requestedAttributes

# Get Contacts
def getContacts(EntityDescriptor,namespaces,contactType='technical'):
    contactsList = list()

    if (contactType.lower() == 'technical'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='technical']/md:EmailAddress", namespaces)
    if (contactType.lower() == 'support'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='support']/md:EmailAddress", namespaces)
    if (contactType.lower() == 'administrative'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='administrative']/md:EmailAddress", namespaces)

    if (len(contacts) != 0):
       for ctc in contacts:
           if ctc.text.startswith("mailto:"):
              contactsList.append(ctc.text)
           else:
              contactsList.append("mailto:" + ctc.text)
              contactList.append(ctc.text)

    return contactsList


def main(argv):
   try:
      # 'm:o:hd' means that 'm' and 'o' needs an argument(confirmed by ':'), while 'h' and 'd' don't need it
      opts, args = getopt.getopt(sys.argv[1:], 'm:o:hd', ['metadata=','output=','help','debug' ])
   except getopt.GetoptError as err:
      print (str(err))
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
      print ("The JSON content will be put in the output directory")
      sys.exit(2)

   inputfile = None
   outputpath = None

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
         print ("The JSON content will be put in the output directory")
         sys.exit()
      elif opt in ('-m', '--metadata'):
         inputfile = arg
      elif opt in ('-o', '--output'):
         outputpath = arg
      elif opt == '-d':
         global _debug
         _debug = 1
      else:
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
         print ("The JSON content will be put in the output directory")
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
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
      print ("The JSON content will be put in the output directory")
      sys.exit()

   if outputpath == None:
      print ("Output path is missing!\n")
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
      print ("The JSON content will be put in the output directory")
      sys.exit()


   tree = ET.parse(inputfile)
   root = tree.getroot()
   sp = root.findall("./md:EntityDescriptor[md:SPSSODescriptor]", namespaces)
   idp = root.findall("./md:EntityDescriptor[md:IDPSSODescriptor]", namespaces)

   sps = dict()
   idps = dict()

   list_sps = list()
   list_idps = list()

   cont_id = 0

   for EntityDescriptor in sp:

      cont_id = cont_id + 1

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get ServiceName ENG
      #serviceName = getServiceName(EntityDescriptor,namespaces)
      serviceName = getDisplayName(EntityDescriptor,namespaces,'sp')

      # Get Organization Page
      orgUrl = getOrganizationURL(EntityDescriptor,namespaces)
     
      # Get Requested Attributes
      requestedAttributes = getRequestedAttribute(EntityDescriptor,namespaces)

      # Get Organization Name
      orgName = getOrgName(EntityDescriptor,namespaces)

      sp = OrderedDict([
        ('id',cont_id),
        ('IdemResource_name',serviceName),
        ('IdemResource_serviceUrlOne', orgUrl),
        ('IdemResource_uri',', '.join(requestedAttributes)),
        ('IdemAccession_name',orgName)
      ])

      list_sps.append(sp)

   
   result_sps = open("%s/idem-resources.json" % outputpath, "w",encoding=None)
   result_sps.write(json.dumps(sorted(list_sps,key=itemgetter('id')),sort_keys=False, indent=None, ensure_ascii=False,separators=(',', ':')))
   result_sps.close()

   cont_id = 0

   # JSON Output:
   # [ 
   #  {
   #    "entityID": "<entityID>",
   #    "orgName": "<nomeOrg>",
   #    "orgURL": "urlOrg",
   #    "logo": "logoOrg",
   #    "contacts": [
   #                  { "technical" : "<email-tecnichal>" },
   #                  { "support" : "<email-support>" },
   #                  { "administrative" : "<email-administr>" }
   #                ],
   #    "info": [
   #              { "it" : "<informationUrl-italiana.html>" },
   #              { "en" : "<informationUrl-inglese.html>" },
   #            ],
   #    "privacy": [
   #                 { "it" : "<privacyUrl-italiana.html>" },
   #                 { "en" : "<privacyUrl-inglese.html>" },
   #               ],
   #  } 
   # ] 

   for EntityDescriptor in idp:

      cont_id = cont_id + 1

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get DisplayName
      orgName = getDisplayName(EntityDescriptor, namespaces, 'idp')

      # Get OrganizationURL
      orgUrl = getOrganizationURL(EntityDescriptor,namespaces)

      # Get Logo URL
      logoUrl = getLogoBig(EntityDescriptor, namespaces, 'idp')

      # Get Contacts
      techContacts = getContacts(EntityDescriptor, namespaces, 'technical')
      suppContacts = getContacts(EntityDescriptor, namespaces, 'support')
      adminContacts = getContacts(EntityDescriptor, namespaces, 'administrative')

      contacts = OrderedDict([
         ('technical', techContacts),
         ('support', suppContacts),
         ('administrative', adminContacts),
      ])

      # Get InformationURL
      info = getInformationURLs(EntityDescriptor, namespaces, 'idp')
      
      # Get PrivacyStatementURL
      privacy = getPrivacyStatementURLs(EntityDescriptor, namespaces, 'idp')
      
      idp = OrderedDict([
        ('id',cont_id),
        ('entityID',entityID),
        ('orgName', orgName),
        ('orgUrl', orgUrl),
        ('logo', logoUrl),
        ('contacts', contacts),
        ('info', info),
        ('privacy', privacy)
      ])

      list_idps.append(idp)

   
   result_idps = open("%s/idem-idps.json" % outputpath, "w",encoding=None)
   result_idps.write(json.dumps(sorted(list_idps,key=itemgetter('id')),sort_keys=False, indent=None, ensure_ascii=False,separators=(',', ':')))
   result_idps.close()



if __name__ == "__main__":
   main(sys.argv[1:])
