import csv
from io import BytesIO, StringIO
import json
import os.path
import requests
from zipfile import ZipFile

#non standard libraries


class CharityCommissionEW:

    def __init__(self, debug=False):
        """
        A class to represent charity commission dataset(s).

        :param debug: Enable debug mode providing additional information
        :type debug: bool

        """
        self._debug = debug
        self._cc = {
            "base_url": "https://ccewuksprdoneregsadata1.blob.core.windows.net/data/",
            "json_url": "json/publicextract.",
            "txt_url": "txt/publicextract.",
            "json_ext": ".json",
            "txt_ext": ".txt",
            "zip_ext": ".zip",
            "entities": [
                "charity",
                "charity_annual_return_history",
                "charity_annual_return_parta",
                "charity_annual_return_partb",
                "charity_area_of_operation",
                "charity_classification",
                "charity_event_history",
                "charity_governing_document",
                "charity_other_names",
                "charity_other_regulators",
                "charity_policy",
                "charity_published_report",
                "charity_trustee"
            ]
        }

    def _list_entities(self):
        """ List available entities

        :return: Available entities
        :rtype: array
        """
        return self._cc['entities']
    
    def _entity_exists(self, entity):
        """
        
        Check if entity exists in available entities

        :param entity: Select charity data entity.
        :type entity: string

        :return: Entity status
        :rtype: bool
        """

        return True if entity in self._list_entities() else False

    def _gen_url(self, entity, json=True):
        """

        Helper function:
        Generate URL for entity and filetype selected

        :param entity: Select charity data entity.
        :type entity: string

        :param json: Select json or csv URL.
        :type json: bool, optional

        :return: The generated URL.
        :rtype: string
        """
        if entity in self._cc['entities']:
            if json:
                typeurl = self._cc['json_url']
            else:
                typeurl = self._cc['txt_url']

            return self._cc['base_url'] + \
                    typeurl + \
                    entity + \
                    self._cc['zip_ext']
    
    def _test_url(self, entity, json=True):
        """

        Helper Function: 
        Check URL from _gen_url is available.

        :param entity: Select charity data entity.
        :type entity: string

        :param json: Select json or csv URL.
        :type json: bool, optional

        :return: The URLs availability
        :rtype: bool
        """
        url = self._gen_url(entity=entity, json=json)

        return True if requests.head(url).status_code == 200 else False

    def _gen_filename(self, entity, json=True):
        """

        Helper function:
        Generate expected filename for entity and filetype selected

        :param entity: Select charity data entity.
        :type entity: string

        :param json: Select json or csv URL.
        :type json: bool, optional
        
        :return: The generated URL
        :rtype: string
        """
        if entity in self._cc['entities']:
            if json:
                fileext = self._cc['json_ext']
            else:
                fileext = self._cc['txt_url']
            
            return 'publicextract.' + \
                    entity + \
                    fileext

    def _get_entity(self, entity, json=True):
        """
        
        Helper function: 
        Download file for selected entity and filetype, unzip
        and return.

        :param entity: Select charity data entity.
        :type entity: string

        :param json: Select json or csv URL.
        :type json: bool, optional

        :return: Returns a StringIO object with the selected entities data
            in the filetype selected
        :rtype: StringIO
        """
    
        downloadfile = self._gen_url(entity, json)
        targetfile = self._gen_filename(entity, json)
        outfile = StringIO()
        resp = requests.get(downloadfile).content
        zipfile = ZipFile(BytesIO(resp))
        outfile.write(zipfile.read(targetfile).decode('utf-8'))
        outfile.seek(0)

        return outfile

    def to_file (self, entity, filetype='csv', folder='./data'):
        """

        Save file for the selected entity and filetype

        :param entity: Select charity data entity.
        :type entity: string

        :param filetype: Select filetype for save file.
        :type json: bool, optional

        :param folder: Target folder for save file, defaults to './data'
        :type folder: str, optional

        """
        outfile = os.path.join(folder, entity + '.' + filetype)
        delimited_exts = {
            'csv': ',',
            'tsv': '\t',
            'psv': '|'
        }
        # handle delimited tabular filetypes
        if filetype.lower() in ['csv','tsv','psv']:
            entitydata = csv.reader(self._get_entity(entity=entity, json=False), delimiter='\t', quoting=csv.QUOTE_NONE)
            with open(outfile, 'w', newline='') as tempfile:
                cw = csv.writer(tempfile, quotechar='"', escapechar='\\', delimiter=delimited_exts[filetype])
                cw.writerows(entitydata)
        # handle json
        elif filetype.lower() in ['json']:
            entitydata = self._get_entity(entity=entity, json=True)
            with open(outfile, 'w', encoding="utf-8", newline='') as tempfile:
                print(type(entitydata.getvalue()))
                tempfile.write(entitydata.getvalue())
        else:
            print('Invalid filetype. Valid types: csv, tsv, psv, json')


    def to_csv_reader(self, entity):
        """
        Transform data for selected entity to csv.reader

        :param entity: Select charity data entity.
        :type entity: string

        :return: The result of the transformation
        :rtype: csv.reader
        """
        return csv.reader(self._get_entity(entity=entity, json=False), delimiter='\t', quoting=csv.QUOTE_NONE)

    def to_dict(self, entity):
        """
        Transform data for selected entity to dict

        :param entity: Select charity data entity.
        :type entity: string

        :return: The result of the transformation
        :rtype: dict
        """
        return json.loads(self._get_entity(entity=entity, json=True).read().encode())

    def all_to_dict(self):
        """
        Download all entities and transform into dict of dicts

        :return: All entities as a dict of dicts
        :rtype: dict
        """
        return_json = {}
        for entity in self._cc['entities']:
            return_json[entity] = json.loads(self._get_entity(entity=entity, json=True).read().encode())
        return return_json