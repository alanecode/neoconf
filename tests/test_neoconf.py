#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for neoconf.py
"""

import unittest
import os
from neoconf.neoconf import Neo4jConfigReader

class Neo4jConfigReaderTestCase(unittest.TestCase):
    
    def test_default_conf_data_dir(self):
        with open(os.path.join('tests', 'resources', 'default.conf'), 
                      'r') as f:
            reader = Neo4jConfigReader(f)
            self.assertEqual(reader.get_setting("dbms.directories.data"),
                             "/var/lib/neo4j/data",
                             "Wrong data directory setting")
            
    
    def test_default_conf_active_db(self):
        with open(os.path.join('tests', 'resources', 'default.conf'), 
                      'r') as f:
            reader = Neo4jConfigReader(f)
            self.assertEqual(reader.get_setting("dbms.active_database"),
                             "graph.db",
                             "Wrong active database")
            
    
    def test_custom_conf_active_db(self):
        with open(os.path.join('tests', 'resources', 'custom.conf'), 'r') as f:
            reader = Neo4jConfigReader(f)
            self.assertEqual(reader.get_setting("dbms.active_database"),
                             "custom.db",
                             "Wrong active database")
            
    
    def test_error_if_setting_other_than_active_db_not_found(self):
        """Should throw ValueError error if setting isn't found in file."""
        with open(os.path.join('tests', 'resources', 'custom.conf'), 'r') as f:    
            reader = Neo4jConfigReader(f)   
            self.assertRaises(ValueError, 
                              reader.get_setting, "nonsense_setting")      
            
            
    def test_error_conf_active_db(self):
        """Should detect active database is defined twice"""
        with open(os.path.join('tests', 'resources', 'error.conf'), 'r') as f:
            reader = Neo4jConfigReader(f)
            self.assertRaises(ValueError, reader.get_setting, 
                              "dbms.active_database")
