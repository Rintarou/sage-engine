# rdf_config.py
# Author: Thomas MINIER - MIT License 2017-2018
from rdflib import Graph, Namespace, RDF, XSD, Literal
from rdflib.util import guess_format
from database.datasets import Dataset
from database.rdf_file_connector import RDFFileConnector
from database.hdt_file_connector import HDTFileConnector
# from database.hdt_server_factory import HDTServerFactory

# some usefull namespaces
sage = Namespace('http://sage.github.io#')
dcterms = Namespace('<http://purl.org/dc/terms/')
void = Namespace('http://rdfs.org/ns/void#')

DB_CONNECTORS = dict()
DB_CONNECTORS[sage['HdtFile']] = HDTFileConnector
DB_CONNECTORS[sage['RdfFile']] = RDFFileConnector


class RDFConfig(object):
    """A configuration object loaded from a RDF file"""
    def __init__(self, filename):
        super(RDFConfig, self).__init__()
        self._filename = filename
        self._graph = Graph()
        self._graph.parse(self._filename, format=guess_format(file))
        self._datasets = dict()
        for s, p, o in self._graph.triples((None, sage['datasets'], None)):
            (title, dataset) = self.__load_dataset(s)
            self._datasets[k] = dataset

    def __load_dataset(self, dataset_uri):
        time_quota = self._graph.value(dataset_uri, sage['timeQuota'], default=Literal(20))
        backend = self._graph.value(dataset_uri, sage['backend'])
        backend_type = self._graph.value(backend, RDF['type'])
        backend_source = self._graph.value(backend, dcterms['source'])

        # build datasets
        datasets = {c["name"]: Dataset(c) for c in config["datasets"]}
        return (config, datasets)
