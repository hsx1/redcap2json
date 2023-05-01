# redcap2json

Handling data dictionaries from REDCap. REDCap is used for electronic data 
collection.

Oftentimes, experimenters will only download a CSV will the raw data. To access 
the labels of many Recap question types. Download the code dictionary along 
with the raw data. This script allows to parse the data dictionary into an 
object that can either be used during data analysis or saved into a json 
structure.

## Requirements

* pandas
* jsonpickle

## Usage

### Save answer as json
```python
from redcap2json import Project

file_path = "/Users/Path/To/CivibeScreening_DataDictionary_2023-04-30.csv"
proj = Project(file_path)

json_path = "/Users/Path/To/CivibeScreening_DataDictionary_2023-04-30.json"
proj.save_as_json(json_path)
```

### Use project object in script

```python
# load data dictionary in object structure
file_path = "/Users/Path/To/CivibeScreening_DataDictionary_2023-04-30.csv"
proj = Project(file_path)

# get overview of all form/survey names
overview_forms = proj.get_forms()
print(overview_forms)

# overview of all item/question names
overview_items = proj.get_questions()
print(overview_items)

# options/content for one single item
# 
# option 1 - from specific form/survey
single_item = proj.forms["online_screening_consent_form"].get_content(
    content="screening_language")
print(single_item)
# option 2 - from whole project
single_item = proj.get_content("screening_language")
print(single_item)
```

## Further Resources

* [How to download raw data](https://www.ctsi.ufl.edu/files/2017/06/Exporting-Data-from-REDCap-%E2%80%93-How-1.pdf)
* [How to download the data dictionary](https://redcap.smhs.gwu.edu/sites/g/files/zaskib651/files/2021-07/Download%20the%20Data%20Dictionary.pdf)