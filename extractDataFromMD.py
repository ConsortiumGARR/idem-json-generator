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
def getOrganizationName(EntityDescriptor, namespaces,lang='it'):
    orgName = EntityDescriptor.find("./md:Organization/md:OrganizationName[@xml:lang='%s']" % lang,namespaces)

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

    displayName = EntityDescriptor.find("%s/md:Extensions/mdui:DisplayName[@xml:lang='it']" % entityType,namespaces)

    if (displayName != None):
       return displayName.text
    else:
       displayName = EntityDescriptor.find("%s/md:Extensions/mdui:DisplayName[@xml:lang='en']" % entityType,namespaces)
       if (displayName != None):
          return displayName.text
       else:
          if (entType == 'sp'):
             displayName = getServiceName(EntityDescriptor,namespaces)
             if (displayName != None):
                return displayName
             else:
                return ""
          else:
             displayName = getOrganizationName(EntityDescriptor,namespaces)
             return displayName

    
# Get MDUI InformationURLs
def getInformationURLs(EntityDescriptor,namespaces,entType='idp'):
    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    info_pages = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:InformationURL" % entityType, namespaces)

    info_dict = dict()
    for infop in info_pages:
        lang = infop.get("{http://www.w3.org/XML/1998/namespace}lang")
        info_dict[lang] = infop.text

    if ('it' not in info_dict):
       info_dict['it'] = ""

    if ('en' not in info_dict):
       info_dict['en'] = ""

    return info_dict


# Get MDUI PrivacyStatementURLs
def getPrivacyStatementURLs(EntityDescriptor,namespaces,entType='idp'):
    entityType = ""
    if (entType.lower() == 'idp'):
       entityType = "./md:IDPSSODescriptor"
    if (entType.lower() == 'sp'):
       entityType = "./md:SPSSODescriptor"

    privacy_pages = EntityDescriptor.findall("%s/md:Extensions/mdui:UIInfo/mdui:PrivacyStatementURL" % entityType, namespaces)

    privacy_dict = dict()
    for pp in privacy_pages:
        lang = pp.get("{http://www.w3.org/XML/1998/namespace}lang")
        privacy_dict[lang] = pp.text

    if ('it' not in privacy_dict):
       privacy_dict['it'] = ""

    if ('en' not in privacy_dict):
       privacy_dict['en'] = ""

    return privacy_dict


# Get OrganizationURL
def getOrganizationURL(EntityDescriptor,namespaces,lang='it'):
    orgUrl = EntityDescriptor.find("./md:Organization/md:OrganizationURL[@xml:lang='%s']" % lang,namespaces)

    if (orgUrl != None):
       return orgUrl.text
    else:
       return ""


# Get RequestedAttribute
def getRequestedAttribute(EntityDescriptor,namespaces):
    reqAttr = EntityDescriptor.findall("./md:SPSSODescriptor/md:AttributeConsumingService/md:RequestedAttribute", namespaces)

    requireList = list()
    requestedList = list()
    requestedAttributes = dict()

    if (len(reqAttr) != 0):
       for ra in reqAttr:
           if (ra.get('isRequired') == "true"):
              requireList.append(ra.get('FriendlyName'))
           else:
              requestedList.append(ra.get('FriendlyName'))

    requestedAttributes['required'] = requireList
    requestedAttributes['requested'] = requestedList

    return requestedAttributes


# Get Contacts
def getContacts(EntityDescriptor,namespaces,contactType='technical'):
    contactsList = list()

    if (contactType.lower() == 'technical'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='technical']/md:EmailAddress", namespaces)
    elif (contactType.lower() == 'support'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='support']/md:EmailAddress", namespaces)
    elif (contactType.lower() == 'administrative'):
       contacts = EntityDescriptor.findall("./md:ContactPerson[@contactType='administrative']/md:EmailAddress", namespaces)

    if (len(contacts) != 0):
       for ctc in contacts:
           if ctc.text.startswith("mailto:"):
              contactsList.append(ctc.text.replace("mailto:", ""))
           else:
              contactList.append(ctc.text)

    return '<br/>'.join(contactsList)


def main(argv):
   try:
      # 'm:o:hd' means that 'm' and 'o' needs an argument(confirmed by ':'), while 'h' and 'd' don't need it
      opts, args = getopt.getopt(sys.argv[1:], 'm:o:hd', ['metadata=','output=','help','debug' ])
   except getopt.GetoptError as err:
      print (str(err))
      print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
      print ("The idem-sps.json and idem-idps.json files will be put in the output directory")
      sys.exit(2)

   inputfile = None
   outputpath = None

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print ("Usage: ./extractDataFromMD.py -m <md_inputfile> -o <output_path>")
         print ("The idem-sps.json and idem-idps.json files will be put in the output directory")
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
         print ("The idem-sps.json and idem-idps.json files will be put in the output directory")
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

   # JSON SP Output:
   # [
   #   {
   #     "id": #_number_#,
   #     "resourceName": "#_resource-display-name_#",
   #     "resourceProvider": "#_organization-name-linked_#",
   #     "resourceAttributes": {
   #        "required": [
   #                      "eduPersonPrincipalName",
   #                      "email",
   #                      "givenName",
   #                      "surname"
   #                    ],
   #        "requested": []
   #     },
   #     "entityID": "#_entityID-resource_#",
   #     "resourceContacts": {
   #        "technical": [
   #                       "#_email-address-list_#"
   #                     ],
   #        "support": [],
   #        "administrative": []
   #     },
   #     "info": "<a href='#_info-url-it_#'>IT</a>, <a href='#_info-url-en_#'>EN</a>",
   #     "privacy": "<a href='#_privacy-url-it_#'>IT</a>, <a href='#_privacy-url-en_#'>EN</a>"
   #   }
   # ]
   for EntityDescriptor in sp:

      cont_id = cont_id + 1
      info = ""
      privacy = ""

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get InformationURL
      infoDict = getInformationURLs(EntityDescriptor, namespaces, 'sp')

      # Get PrivacyStatementURL
      privacyDict = getPrivacyStatementURLs(EntityDescriptor, namespaces, 'sp')

      # Get ServiceName
      serviceName = getDisplayName(EntityDescriptor,namespaces,'sp')

      # Build Resource Info Pages
      if (infoDict['it'] != "" and infoDict['en'] != ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>&nbsp;&nbsp;&nbsp;<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (infoDict['it'],infoDict['en'])
      elif (infoDict['it'] != "" and infoDict['en'] == ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>" % (infoDict['it'])
      elif (infoDict['it'] == "" and infoDict['en'] != ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (infoDict['en'])
      elif (infoDict['it'] == infoDict['en'] == ""):
         info = ""

      # Build Resource Privacy Pages
      if (privacyDict['it'] != "" and privacyDict['en'] != ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>&nbsp;&nbsp;&nbsp;<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (privacyDict['it'],privacyDict['en'])
      elif (privacyDict['it'] != "" and privacyDict['en'] == ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>" % (privacyDict['it'])
      elif (privacyDict['it'] == "" and privacyDict['en'] != ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (privacyDict['en'])
      elif (privacyDict['it'] == privacyDict['en'] == ""):
         privacy = ""

      # Get Requested Attributes
      requestedAttributes = getRequestedAttribute(EntityDescriptor,namespaces)

      # Get Organization Name

      orgName = getOrganizationName(EntityDescriptor,namespaces,'it')
      if (orgName == ""):
         orgName = getOrganizationName(EntityDescriptor,namespaces,'en')

      # Get Organization Page
      orgUrl = getOrganizationURL(EntityDescriptor,namespaces,'it')
      if (orgUrl == ""):
         orgUrl = getOrganizationURL(EntityDescriptor,namespaces,'en')
     
      orgName = "<a href='%s' target='_blank'>%s</a>" % (orgUrl,orgName)

      # Get Contacts
      techContacts = getContacts(EntityDescriptor, namespaces, 'technical')
      suppContacts = getContacts(EntityDescriptor, namespaces, 'support')
      adminContacts = getContacts(EntityDescriptor, namespaces, 'administrative')

      contacts = OrderedDict([
         ('technical', techContacts),
         ('support', suppContacts),
         ('administrative', adminContacts),
      ])

      # Build SP JSON Dictionary
      sp = OrderedDict([
        ('id',cont_id),
        ('resourceName',serviceName),
        ('resourceProvider', orgName),
        ('resourceAttributes',requestedAttributes),
        ('entityID',entityID),
        ('resourceContacts',contacts),
        ('info', info),
        ('privacy', privacy)
      ])     

      list_sps.append(sp)

   result_sps = open("%s/idem-sps.json" % outputpath, "w",encoding=None)
   result_sps.write(json.dumps(sorted(list_sps,key=itemgetter('id')),sort_keys=False, indent=None, ensure_ascii=False,separators=(',', ':')))
   result_sps.close()


   info = ""
   privacy = ""
   cont_id = 0

   # JSON IdP Output:
   # [ 
   #  {
   #    "id":"<id>",
   #    "entityID": "<entityID>",
   #    "orgName": "<nomeOrgLinked>",
   #    "contacts": {
   #                  "technical" : ["<email-tecnichal>"],
   #                  "support" : ["<email-support>"],
   #                  "administrative" : ["<email-administr>"]
   #                },
   #    "info": "<informationUrls>",
   #    "privacy": "<privacyUrls>",
   #    "favicon": "<faviconUrl>",
   #    "logo": "<logoUrl>",
   #  } 
   # ] 
   for EntityDescriptor in idp:

      cont_id = cont_id + 1

      # Get entityID
      entityID = getEntityID(EntityDescriptor,namespaces)

      # Get DisplayName
      orgName = getDisplayName(EntityDescriptor, namespaces, 'idp')

      # Get Organization Page
      orgUrl = getOrganizationURL(EntityDescriptor,namespaces,'it')
      if (orgUrl == ""):
         orgUrl = getOrganizationURL(EntityDescriptor,namespaces,'en')
     
      orgName = "<a href='%s' target='_blank'>%s</a>" % (orgUrl,orgName)

      # Get Logo URL
      logo = getLogoBig(EntityDescriptor, namespaces, 'idp')

      # Get Favicon URL
      favicon = getLogoSmall(EntityDescriptor, namespaces, 'idp')

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
      infoDict = getInformationURLs(EntityDescriptor, namespaces, 'idp')

      # Get PrivacyStatementURL
      privacyDict = getPrivacyStatementURLs(EntityDescriptor, namespaces, 'idp')

      # Build Resource Info Pages
      if (infoDict['it'] != "" and infoDict['en'] != ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>&nbsp;&nbsp;&nbsp;<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (infoDict['it'],infoDict['en'])
      elif (infoDict['it'] != "" and infoDict['en'] == ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>" % (infoDict['it'])
      elif (infoDict['it'] == "" and infoDict['en'] != ""):
         info = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (infoDict['en'])
      elif (infoDict['it'] == infoDict['en'] == ""):
         info = ""

      # Build Resource Privacy Pages
      if (privacyDict['it'] != "" and privacyDict['en'] != ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>&nbsp;&nbsp;&nbsp;<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (privacyDict['it'],privacyDict['en'])
      elif (privacyDict['it'] != "" and privacyDict['en'] == ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/it.png' alt='Info ITA' height='18' width='18' /></a>" % (privacyDict['it'])
      elif (privacyDict['it'] == "" and privacyDict['en'] != ""):
         privacy = "<a href='%s' target='_blank'><img src='https://idem.garr.it/images/uk.png' alt='Info ENG' height='18' width='18' /></a>" % (privacyDict['en'])
      elif (privacyDict['it'] == privacyDict['en'] == ""):
         privacy = ""

      idp = OrderedDict([
        ('id',cont_id),
        ('entityID',entityID),
        ('orgName', orgName),
        ('contacts', contacts),
        ('info', info),
        ('privacy', privacy),
        ('favicon', favicon),
        ('logo', logo)
      ])

      list_idps.append(idp)

   
   result_idps = open("%s/idem-idps.json" % outputpath, "w",encoding=None)
   result_idps.write(json.dumps(sorted(list_idps,key=itemgetter('id')),sort_keys=False, indent=None, ensure_ascii=False,separators=(',', ':')))
   result_idps.close()



if __name__ == "__main__":
   main(sys.argv[1:])
