# Charity Commission Data

Python library to download charity commission data into usable objects or files.

### Installation

`pip install charitycommissionew`

### Getting Started

How to get data from the charity commission with this library:

```python
from charitycommissionew import CharityCommissionEW as ccew

# To a CSV file

ccew().to_file(entity='charity', filetype='csv', folder='./data')

# To a dict 

charitydata = ccew()
charitydata.to_dict(entity='charity')

# To a CSV Reader object

charitydata = ccew()
charitydata.to_csv_reader(entity='charity')

```

### Available Entities

The [charity commission data](http://data.charitycommission.gov.uk/) is available in a normalised structure, resulting in lots of files. 
Most functions take an entity parameter. The following entities are currently supported:

 - charity
 - charity_annual_return_history
 - charity_annual_return_parta
 - charity_annual_return_partb
 - charity_area_of_operation
 - charity_classification
 - charity_event_history
 - charity_governing_document
 - charity_other_names
 - charity_other_regulators
 - charity_policy
 - charity_published_report
 - charity_trustee