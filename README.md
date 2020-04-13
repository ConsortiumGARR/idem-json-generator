# IDEM JSON Generator
Small python3 script that converts Metadata XML to DiscoFeed JSON format for Shibboleth Embedded Discovery Service

# Instructions

* `sudo apt install python3`

* `cd /opt ; sudo git clone https://git.garr.it/IDEM/idem-json-generator.git`

* Configure your Apache:
  * `sudo cp /opt/idem-json-generator/idem-json-generator.conf /etc/apache2/sites-available`

* Put the following command into your preferred CRON Jobs:
  * Choose ONE of the following command to consider only ONE metadata stream:
    * IDEM Test Metadata: 
      * `/usr/bin/wget http://md.idem.garr.it/metadata/idem-test-metadata-sha256.xml -O /opt/idem-json-generator/input/idem-test-metadata-sha256.xml >> /opt/idem-json-generator/wget.log 2>&1`
    * IDEM Production Metadata:
      * `/usr/bin/wget http://md.idem.garr.it/metadata/idem-metadata-sha256.xml -O /opt/idem-json-generator/input/idem-metadata-sha256.xml >> /opt/idem-json-generator/wget.log 2>&1`

  * Use one of the following commands to generate EDS JSON files `idem-resources.json` & `idem-idps.json` for the specific stream:
    * IDEM Test Metadata:
      * `/usr/bin/python3 /opt/idem-json-generator/extractDataFromMD.py -m /opt/idem-json-generator/input/idem-test-metadata-sha256.xml -o /opt/idem-json-generator/output > /opt/idem-json-generator/idem-json-generator.log 2>&1`
    * IDEM Production Metadata:
      * `/usr/bin/python3 /opt/idem-json-generator/extractDataFromMD.py -m /opt/idem-json-generator/input/idem-metadata-sha256.xml -o /opt/idem-json-generator/output > /opt/idem-json-generator/idem-json-generator.log 2>&1`

  Example Crontab:
  ```bash
  20 * * * * /usr/bin/wget http://md.idem.garr.it/metadata/idem-metadata-sha256.xml -O /opt/idem-json-generator/input/idem-metadata-sha256.xml >> /opt/idem-json-generator/wget.log 2>&1

  21 * * * * /usr/bin/python3 /opt/idem-json-generator/extractDataFromMD.py -m /opt/idem-json-generator/input/idem-metadata-sha256.xml -o /opt/idem-json-generator/output > /opt/idem-json-generator/idem-json-generator.log 2>&1
  ```

* Enable IDEM JSON Generator site:
  * `sudo a2ensite idem-json-generator.conf`
  * `sudo systemctl reload apache2.service`
