# Copyright (c) 2022, Ora Lassila & So Many Aircraft
# All rights reserved.
#
# See LICENSE for licensing information
#
# This module implements some useful stuff when programming with RDFLib.

from rdfhelpers.rdfhelpers import graphFrom, expandQName, getvalue, setvalue, addvalues, setvalues
from rdfhelpers.rdfhelpers import diff, getContainerItems, setContainerItems
from rdfhelpers.rdfhelpers import SPARQLRepository, JournaledGraph, FocusedGraph
from rdfhelpers.templated import mapDict, Templated, TemplatedQueryMixin
from rdfhelpers.constructor import Constructor

__all__ = [
    'graphFrom', 'expandQName', 'getvalue', 'setvalue', 'addvalues', 'setvalues',
    'diff', 'getContainerItems', 'setContainerItems',
    'SPARQLRepository', 'JournaledGraph', 'FocusedGraph',
    'mapDict', 'Templated', 'TemplatedQueryMixin',
    'Constructor'
]
