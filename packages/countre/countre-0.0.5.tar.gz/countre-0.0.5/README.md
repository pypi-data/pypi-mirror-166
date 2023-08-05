# Country Regex Package

**countre** is a package with functions to get standardised names or codes from country names, as well as additional country information. Country names often differ between data sources, therefore having standardised codes for each country makes it easy to merge data from multiple sources.

The countries included are those defined by the International Organization for Standardization. The list can be found
[here](https://www.iso.org/iso-3166-country-codes.html). The sources of the country data can be found [here](https://github.com/mwtb47/countre/country_data).

<br>

## Installation

**countre** can be installed via pip from PyPi:

```
pip install countre
```

<br>

## Functions

### countre.country_info(*countries*, *attributes*, *no_match='no_match'*)  
&nbsp;&nbsp;&nbsp;&nbsp; **Parameters**:   
          **countries** : *iterable*  
              Country names, ISO 3166-1 alpha-2 codes, or ISO 3166-1 alpha-3 codes.  
          **variables** : *countre.enums.Attribute* | *list{countre.enums.Attribute}*  
              Specify either a single attribute or a list containing multiple attributes.  
          **no_match** : *str, default 'no match'*  
              String returned for a country if no match is found.  
    **Returns**:  
          A list of values if only one attribute is given. A dictionary if more than  
          one variable is given. The dictionary keys are the attribute names and the  
          values are lists of values.
        

*Note: The country_info function finds data via regex pattern matching for each unique country in the countries iterable and then returns the respective value for each element of countries. This means there is relatively little difference in performace between a list of unique countries and that same list repeated multiple times.*

<br>

### countre.member_countries(*organisation*, *attribute=countre.enums.Attribute.COUNTRY*)

&nbsp;&nbsp;&nbsp;&nbsp; **Parameters**:   
          **organisation** : *countre.enums.Organisation*  
              Specify the organisation to get members of. Select from EU, EU_EEA, OECD, and OPEC.  
          **attrribute** : *countre.enums.Attribute*  
              To get member country names or ISO codes, specify COUNTRY, COUNTRY_SHORT, ISO2 or ISO3.  
    **Returns**:  
          List of either country names, ISO 3166-1 alpha-2 codes or ISO 3166-1 alpha-3  
          codes for the members of the specified organisation.

<br>

## Examples

```
>>> import countre
>>> from countre.enums import Attribute, Organisation
>>>
>>> countries = ['Australia', 'Germany', 'Sweden']
>>> attributes = [Attribute.ISO3, Attribute.CAPITAL, Attribute.CURRENCY_NAME]
```

#### Get a single attribute for a list of countries
```
>>> countre.country_info(countries=countries, attributes=Attribute.ISO3)

['AUS', 'DEU', 'SWE']
```

#### Get multiple attributes for a list of countries
```
>>> countre.country_info(countries=countries, attributes=attributes)

{
    'iso3': ['AUS', 'DEU', 'SWE'],
    'capital_city': ['Canberra', 'Berlin', 'Stockholm'],
    'currency_name': ['Australian dollar', 'Euro', 'Swedish krona']
}
```

#### When using multiple attributes, the output can easily be converted to a Pandas DataFrame
```
>>> import pandas as pd
>>> pd.DataFrame(countre.country_info(countries, attributes))

   iso3   country     capital_city
0  AUS    Australia   Canberra
1  DEU    Germany     Berlin
2  SWE    Sweden      Stockholm
```

#### Get organisation member countries. Not specifying an attribute will return the country names.
```
>>> countre.member_countries(Organisation.EU)

['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', ...
```

#### Get organisation member countries with attribute specification
```
>>> countre.member_countries(Organisation.EU, Attribute.ISO3)

['AUT', 'BEL', 'BGR', 'HRV', 'CYP', ...
```
