


Data Reference Standard on Date and Time Format - Canada.ca




















* [Skip to main content](#wb-cont)
* [Skip to "About government"](#wb-info)

## Language selection

* [Français
  fr](/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc/norme-referentielle-donnees-format-date-heure.html)



[![Government of Canada](/etc/designs/canada/wet-boew/assets/sig-blk-en.svg)
 /
Gouvernement du Canada](/en.html)



## Search

Search Canada.ca



Search





---


## Menu

Main Menu 

* [Jobs and the workplace](https://www.canada.ca/en/services/jobs.html)
* [Immigration and citizenship](https://www.canada.ca/en/services/immigration-citizenship.html)
* [Travel and tourism](https://travel.gc.ca/)
* [Business and industry](https://www.canada.ca/en/services/business.html)
* [Benefits](https://www.canada.ca/en/services/benefits.html)
* [Health](https://www.canada.ca/en/services/health.html)
* [Taxes](https://www.canada.ca/en/services/taxes.html)
* [Environment and natural resources](https://www.canada.ca/en/services/environment.html)
* [National security and defence](https://www.canada.ca/en/services/defence.html)
* [Culture, history and sport](https://www.canada.ca/en/services/culture.html)
* [Policing, justice and emergencies](https://www.canada.ca/en/services/policing.html)
* [Transport and infrastructure](https://www.canada.ca/en/services/transport.html)
* [Canada and the world](https://www.international.gc.ca/world-monde/index.aspx?lang=eng)
* [Money and finances](https://www.canada.ca/en/services/finance.html)
* [Science and innovation](https://www.canada.ca/en/services/science.html)



## You are here:

1. [Canada.ca](/en.html)
2. [About government](/en/government/system.html)
3. [Government in a digital age](/en/government/system/digital-government.html)
4. [Digital government innovation](/en/government/system/digital-government/digital-government-innovations.html)
5. [Enabling Interoperability](/en/government/system/digital-government/digital-government-innovations/enabling-interoperability.html)
6. [GC Enterprise Data Reference Standards](/en/government/system/digital-government/digital-government-innovations/enabling-interoperability/gc-enterprise-data-reference-standards.html)




# Data Reference Standard on Date and Time Format


## 1. Preamble

* 1.1 This data reference standard is intended to ensure that departments and agencies use a consistent numeric format for date and time to enable the interchange of machine-readable data.
* 1.2 This list is intended to standardize the way date and time are formatted in datasets to enable data interoperability and improve data quality.
* 1.3 This data reference standard is based on the International Organization for Standardization (ISO) 8601 *Date and time — Representations for Information Interchange*.
  + 1.3.1 Appendix A outlines the required format that will be updated accordingly to include additional date and time formats.
  + 1.3.2 Appendix A is copied by Treasury Board of Canada Secretariat with the permission of the Standards Council of Canada (SCC) on behalf of ISO. The French translation of this standard is not official. The standard can be purchased from the national ISO member in your country or the ISO Store. Copyright remains with ISO.
* 1.4 This data reference standard will be reviewed as required by the data reference standard steward in consultation with the data reference standard custodian.
  + 1.4.1 Data reference standard steward: National Research Council Canada
  + 1.4.2 Data reference standard custodian: Treasury Board of Canada Secretariat

## 2. Effective date

* 2.1 This data reference standard takes effect on September 27, 2024.

## 3. Requirements

* 3.1 This data reference standard provides details on the requirements set out in subsection 4.3.1 of the *Directive on Service and Digital*.
* 3.2 Service owners and data practitioners must:
  + 3.2.1 apply the required format (Appendix A) to format date and time in datasets to the extent that they can.

## 4. Application

* 4.1 This data reference standard applies to organizations listed in section 6 of the *Directive on Service and Digital*.
* 4.2 This data reference standard applies to all datasets and systems developed after the effective date of this data reference standard.

## 5. References

* 5.1 This reference standard should be read in conjunction with the following:
  + [**Directive on Service and Digital**](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601)
  + [*Standard for Managing Metadata*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32786)
  + [Standards Council of Canada: All-Numeric Dates and Times](https://scc-ccn.ca/standardsdb/standards/8164109) (only available in English; all the required information from ISO 8601-1:2019 is reproduced in Appendix A).
* 5.2 Related policy instruments:
  + [*Policy on Service and Digital*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32603)

## 6. Enquiries

* 6.1 For interpretation of any aspect of this reference standard, contact [ServiceDigital-ServicesNumerique@tbs-sct.gc.ca](mailto:ServiceDigital-ServicesNumerique@tbs-sct.gc.ca).

## Appendix A: date and time format requirement

This section is reproduced from ISO 8601-1:2019 *Date and time – Representations for information interchange Part 1: Basic Rules* sections 5.2.2.1, 5.2.3.1, 5.3.1.2, 5.3.4.1 and 5.3.4.2 and reorganized under Appendix A.

**A.1 Date sequence**

* A.1.1 An all-numeric date consists of the following data elements from left to right:
  + A.1.1.1 (Calendar) year-month-day
  + A.1.1.2 (Ordinal) year-day of year

**A.2 Characters**

* A.1.2.1 Arabic numerals from set 0, 1, 2, ... 9 are used.

**A.3 Date elements**

* A.3.1 A calendar date consists of three elements:
  + A.3.1.1 four digits to represent “year”
  + A.3.1.2 two digits to represent “month”
  + A.3.1.3 two digits to represent “day”
* A.3.2 An ordinal date consists of two elements:
  + A.3.2.1 four digits to represent “year”
  + A.3.2.2 three digits to represent “day of the year”

**A.4 Date separators**

* A.4.1 A hyphen “-” is to be used as a delimitator, when required.

**A.5 Time elements**

* A.5.1 An all-numeric time consists of the following time elements from left to right:
  + A.5.1.1 Two digits between 00 and 23 to represent “hour”
  + A.5.1.2 Two digits between 00 and 59 to represent “minute”
  + A.5.1.3 Two digits between 00 and 59 to represent “second”
* A.5.2 If a time zone is needed for the recording of time, the offset from the UTC standard consists of:
  + A.5.2.1 A “+” if the time zone comes before UTC
  + A.5.2.2 A “–” if the time zone is after UTC (all of Canada is after UTC)
  + A.5.2.3 Two digits to represent “hour”
  + A.5.2.4 Two digits to represent “minute”

**A.6 Time separators**

* A.6.1 A colon “:” is to be used as a delimitator. If it is not used, then a capital “T” shall be inserted at the beginning of the string.


## Page details



Date modified:
2024-09-27






## About this site

### Government of Canada

* [All contacts](/en/contact.html)
* [Departments and agencies](/en/government/dept.html)
* [About government](/en/government/system.html)

#### Themes and topics

* [Jobs](/en/services/jobs.html)
* [Immigration and citizenship](/en/services/immigration-citizenship.html)
* [Travel and tourism](https://travel.gc.ca/)
* [Business](/en/services/business.html)
* [Benefits](/en/services/benefits.html)
* [Health](/en/services/health.html)
* [Taxes](/en/services/taxes.html)
* [Environment and natural resources](/en/services/environment.html)
* [National security and defence](/en/services/defence.html)
* [Culture, history and sport](/en/services/culture.html)
* [Policing, justice and emergencies](/en/services/policing.html)
* [Transport and infrastructure](/en/services/transport.html)
* [Canada and the world](https://www.international.gc.ca/world-monde/index.aspx?lang=eng)
* [Money and finances](/en/services/finance.html)
* [Science and innovation](/en/services/science.html)
* [Indigenous Peoples](/en/services/indigenous-peoples.html)
* [Veterans and military](/en/services/veterans-military.html)
* [Youth](/en/services/youth.html)



### Government of Canada Corporate

* [Social media](https://www.canada.ca/en/social.html)
* [Mobile applications](https://www.canada.ca/en/mobile.html)
* [About Canada.ca](https://www.canada.ca/en/government/about.html)
* [Terms and conditions](/en/transparency/terms.html)
* [Privacy](/en/transparency/privacy.html)

![Symbol of the Government of Canada](/etc/designs/canada/wet-boew/assets/wmms-blk.svg)













