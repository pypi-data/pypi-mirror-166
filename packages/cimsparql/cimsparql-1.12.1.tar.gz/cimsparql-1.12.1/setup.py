# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cimsparql']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper',
 'StrEnum',
 'deprecated',
 'networkx',
 'numpy',
 'pandas',
 'requests',
 'tables']

extras_require = \
{'parse_xml': ['defusedxml', 'lxml', 'pendulum']}

setup_kwargs = {
    'name': 'cimsparql',
    'version': '1.12.1',
    'description': 'CIM query utilities',
    'long_description': '[![PyPI version](https://img.shields.io/pypi/v/cimsparql)](https://pypi.org/project/cimsparql/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/cimsparql)](https://pypi.org/project/cimsparql/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![](https://github.com/statnett/data_cache/workflows/Tests/badge.svg)](https://github.com/statnett/cimsparql/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/statnett/cimsparql/branch/master/graph/badge.svg)](https://codecov.io/gh/statnett/cimsparql)\n\n# CIMSPARQL Query CIM data using sparql\n\nThis Python package provides functionality for reading/parsing cim data from\neither xml files or GraphDB into Python memory as pandas dataframes.\n\nThe package provides a set of predefined functions/queries to load CIM data\nsuch generator or branch data, though the user can easiliy extend or define\ntheir own queries.\n\n## Usage\n\n### Load data using predefined functions/queries\n\n```python\n>>> from cimsparql.graphdb import GraphDBClient\n>>> from cimsparql.url import service\n>>> gdbc = GraphDBClient(service(repo=\'<repo>\', server=127.0.0.1:7200))\n>>> ac_lines = gdbc.ac_lines(limit=3)\n>>> print(ac_lines[[\'name\', \'x\', \'r\', \'bch\']])\n         name       x       r       bch\n0  <branch 1>  1.9900  0.8800  0.000010\n1  <branch 2>  1.9900  0.8800  0.000010\n2  <branch 3>  0.3514  0.1733  0.000198\n```\n\nIn the example above the client will query repo "<repo>" in the default server\n[GraphDB](https://graphdb.ontotext.com) for AC line values.\n\n### Inspect/view predefined queries\n\nTo see the actual sparql use the `dry_run` option:\n\n```python\n>>> from cimsparql.queries import ac_line_query\n>>> print(ac_line_query(limit=3, dry_run=True))\n```\n\nThe resulting string contains all the prefix\'s available in the Graphdb repo\nmaking it easier to copy and past to graphdb. Note that the prefixes are *not*\nrequired in the user specified quires described below.\n\nThe `dry_run` option is available for all the predefined queries.\n\n### Load data using user specified queries\n\n```python\n>>> query = \'SELECT ?mrid where { ?mrid rdf:type cim:ACLineSegment } limit 2\'\n>>> query_result = gdbc.get_table(query)\n>>> print(query_result)\n```\n\n### List of available repos at the server\n\n```python\n>>> from cimsparql.url import GraphDbConfig\n>>> print(GraphDbConfig().repos)\n```\n\n### Prefix and namespace\n\nAvailable namespace for current graphdb client (`gdbc` in the examples above),\nwhich can be used in queries (such as `rdf` and `cim`) can by found by\n\n```python\n>>> print(gdbc.ns)\n{\'wgs\': \'http://www.w3.org/2003/01/geo/wgs84_pos#\',\n \'rdf\': \'http://www.w3.org/1999/02/22-rdf-syntax-ns#\',\n \'owl\': \'http://www.w3.org/2002/07/owl#\',\n \'cim\': \'http://iec.ch/TC57/2010/CIM-schema-cim15#\',\n \'gn\': \'http://www.geonames.org/ontology#\',\n \'xsd\': \'http://www.w3.org/2001/XMLSchema#\',\n \'rdfs\': \'http://www.w3.org/2000/01/rdf-schema#\',\n \'SN\': \'http://www.statnett.no/CIM-schema-cim15-extension#\',\n \'ALG\': \'http://www.alstom.com/grid/CIM-schema-cim15-extension#\'}\n```\n\n### Running Tests Against Docker Databases\n\nTests can be run agains RDF4J and/or BlazeGraph databases if a container with the correct images are available.\n\n```\ndocker pull eclipse/rdf4j-workbench\ndocker pull openkbs/blazegraph\n```\n\nLaunch one or both containers and specify the following environment variables\n\n```\nRDF4J_URL = "localhost:8080/rdf4j-server"\nBLAZEGRAPH_URL = "localhost:9999/blazegraph/namespace\n```\n**Note 1**: The port numbers may differ depending on your local Docker configurations.\n**Note 2**: You don\'t *have* to install RDF4J or BlazeGraph. Tests requiring these will be skipped in case\nthey are not available. They will in any case be run in the CI pipeline on GitHub (where both always are available).\n\n### Data Assumptions\n\nCimSPARQL makes certain assumptions about the data which is required to be present for the queries to work. The script `modify_xml` should be able to modify\nthe XML files such that they are compliant with CimSPARQL.\n\n1. There is a valid `xml:base` attribute in the top-level `rdf:RDF` element. This is required for uploading files (at least for RDF4J which is used in the CI pipeline)\n2. All items `cimsparql.constants.CIM_TYPES_WITH_MRID` has `cim:IdentifiedObject:mRID`\n3. `cim:Terminal.endNumber` is of type `xsd:integer`\n\n```bash\npoetry run python scripts/modify.xml -h\n\nusage: Program that modifies XML files to be compatible with cimsparql [-h] [--baseURI BASEURI] [--suffix SUFFIX] file\n\npositional arguments:\n  file               File or glob pattern for files to modify\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --baseURI BASEURI  Base URI to insert in all XML files. For example: http://iec.ch/TC57/2013/CIM-schema-cim16\n  --suffix SUFFIX    Suffix to the filename after modifying them. If given as an empty string the original files will be overwritten. Default \'mod\'\n```\n\nIn order to use the script to convert XML files into a format that can be used with `cimsparql`\n\n``` bash\npoetry run scripts/modify_xml.py "path/to/model/*.xml"\n```\n\n### Ontology (for developers)\n\nOntologies for the CIM model can be found at (ENTSOE\'s webpages)[https://www.entsoe.eu/digital/common-information-model/cim-for-grid-models-exchange/].\nFor convenience and testing purposes the ontology are located under `tests/data/ontology`. CIM models used for testing purposes in Cimsparql should\nbe stored in N-quads format. In case you have a model in XML format it can be converted to N-quads by launching a DB (for example RDF4J) and upload\nall the XML files and the ontology.\n\nExecute\n\n```sparql\nPREFIX cims: <http://iec.ch/TC57/1999/rdf-schema-extensions-19990926#>\n\nDELETE {?s ?p ?o}\nINSERT {?s ?p ?o_cast} WHERE {\n  ?s ?p ?o .\n  ?p cims:dataType ?_dtype .\n  ?_dtype cims:stereotype ?stereotype .\n  BIND(IF(?stereotype = "Primitive",\n    URI(concat("http://www.w3.org/2001/XMLSchema#", lcase(strafter(str(?_dtype), "#")))),\n    ?_dtype) as ?dtype)\n  BIND(STRDT(?o, ?dtype) as ?o_cast)\n}\n```\nand export as N-quads.\n\n**Note**: Make sure the base URI is either specified in the XML-files or when you upload. It should be set to\n\n```xml\n<rdf:RDF xml:base="http://iec.ch/TC57/2013/CIM-schema-cim16">\n```\n\n\n### Test models\n\n1. *micro_t1_nl*: `MicroGrid/Type1_T1/CGMES_v2.4.15_MicroGridTestConfiguration_T1_NL_Complete_v2`\n\n\n### Rest APIs\n\nCimSparql mainly uses `SparqlWrapper` to communicate with the databases. However, there are certain operations which are performed\ndirectly via REST calls. Since there are small differences between different APIs you may have to specify which API you are using.\nThis can be done when initializing the `ServiceCfg` class or by specifying the `SPARQL_REST_API` environment variable. Currently,\n`RDF4J` and `blazegraph` is supported (if not given `RDF4J` is default).\n\n```bash\nexport SPARQL_REST_API=RDF4J  # To use RDF4J\nexport SPARQL_REST_API=BLAZEGRAPH  # To use BlazeGraph\n```\n',
    'author': 'Statnett Datascience',
    'author_email': 'Datascience.Drift@Statnett.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/statnett/cimsparql.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
