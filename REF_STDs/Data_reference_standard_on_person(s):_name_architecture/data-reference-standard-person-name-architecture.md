


Data Reference Standard on Person(s): name architecture - Canada.ca




















* [Skip to main content](#wb-cont)
* [Skip to "About government"](#wb-info)

## Language selection

* [Français
  fr](/fr/gouvernement/systeme/gouvernement-numerique/innovations-gouvernementales-numeriques/permettre-interoperabilite/normes-referentielles-pangouvernementales-relatives-donnees-gc/norme-referentielle-donnees-personnes-architecture-noms.html)



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




# Data Reference Standard on Person(s): name architecture


## 1. Preamble

* 1.1 This data reference standard is intended to ensure that departments and agencies of the Government of Canada use consistent fields for capturing the diverse set of names of persons.
* 1.2 This data reference standard is intended to ensure that person names are described, collected and stored consistently in datasets to enable data interoperability and improve data quality.
  + 1.2.1 The appendix outlines the required person name fields to capture primary, secondary and alternate names, as well as names that consist of only one word (that is, mononyms) or which cannot be divided into two parts.
* 1.3 This data reference standard will be reviewed as required by the data reference standard steward in consultation with the data reference standard custodian.
  + 1.3.1 Data reference standard steward: Immigration, Refugees and Citizenship Canada
  + 1.3.2 Data reference standard custodian: Treasury Board of Canada Secretariat
* 1.4 The elements of personal information contained in this standard should be collected, used, retained, disclosed and disposed of in accordance with the requirements of the *Privacy Act* and its underlying policy suite.

## 2. Effective date

* 2.1 This data reference standard takes effect on September 27, 2024.

## 3. Requirements

* 3.1 This data reference standard provides details on the requirements set out in subsection 4.3.1 of the [*Directive on Service and Digital*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601).
* 3.2 Service owners and data practitioners must:
  + 3.2.1 Apply the mandatory data fields (outlined in the appendix) to record a person name or names within the Government of Canada according to the data attributes required for your program.

## 4. Application

* 4.1 This data reference standard applies to organizations listed in section 6 of the *Directive on Service and Digital.*
* 4.2 This data reference standard applies to all datasets developed after the effective date of this standard.

## 5. References

* 5.1 This reference standard should be read in conjunction with the following:
  + [*Directive on Service and Digital*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32601)
  + [Appendix L: Standard for Managing Metadata *(Directive on Service and Digital)*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32786)
  + [*Policy on Service and Digital*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32603)
  + [*Policy on Access to Information*](https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=12453)
* 5.2 Related legislation
  + [*Access to Information Act*](https://laws-lois.justice.gc.ca/eng/ACTS/A-1/index.html)
  + [*Privacy Act*](https://laws-lois.justice.gc.ca/eng/ACTS/P-21/index.html)

## 6. Enquiries

* 6.1 For interpretation of any aspect of this reference standard, contact [ServiceDigital-ServicesNumerique@tbs-sct.gc.ca](mailto:ServiceDigital-ServicesNumerique@tbs-sct.gc.ca).

## Appendix: data architecture tables

Person name fields may be repeated to accommodate more than one value. If possible, the source of the name must be accounted for, either once for the entire table or as a field within the table. If a legal name is collected, it must be captured according to Table 1, and the collection of an alternate name must also be offered.

**Table 1: required primary and secondary person name fields** 
| Field name | Description |
| --- | --- |
| Primary name | May be the surname, family name, last name, maiden name or married name, main name, mononym (that is, a name consisting of only one word) and in some cases, the entire name where the holder’s name cannot be divided into two parts. |
| Secondary name | The portion of a person’s name that is not the primary name. All remaining portions of the name would be entered into this field. |
| Name type | A metadata field to describe a person name for classifying it for legal, administrative or other purposes (for example, legal name, mononym). |
| Name source | Where the name comes from (for example, an evidence of identity (EOI) document, a court-issued document or an attestation by the person). Primary and secondary names should come from the same source. |
| Source date | The date of issuance of an EOI document or other name source. |
| Name collection date | The date the person name is captured in the dataset. |
| Last modified date | The most recent date any person name field was updated or changed. |

**Table 2: alternate person name fields (required if applicable)** 
| Field name | Description |
| --- | --- |
| Alternate primary name | An alternate surname, chosen name, preferred name or alias name of a client. |
| Alternate secondary name | Alternate given name or names of a client that can be used to identify which names in the secondary name field should be used for correspondence (for example, a chosen or preferred name or alias). |
| Alternate name type | A metadata field to describe an alternate name for classifying it for legal, administrative or other purposes (for example, a chosen or preferred name, alias or mononym). |
| Alternate name source | Where the name comes from (for example, an EOI document, a court-issued document or an attestation by the person). For each alternate name, the alternate primary and alternate secondary names should come from the same source. |
| Alternate source date | The date of issuance of a document or other name source. |
| Alternate name collection date | The date the name is captured in the dataset. |



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













