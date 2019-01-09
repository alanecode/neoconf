#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for neoconf.py
"""

import unittest
import os
import warnings
from neoconf.neoconf import Neo4jConfigReader, ConfigLine

class Neo4jConfigReaderTestCase(unittest.TestCase):
    
    def test_default_conf_data_dir(self):
        with open(os.path.join('tests', 'resources', 'default.conf'), 
                      'r') as f:
            reader = Neo4jConfigReader(f)
            self.assertEqual(reader.get_setting("dbms.directories.data"),
                             "/var/lib/neo4j/data",
                             "Wrong data directory setting")
           
    
    def test_default_conf_active_db(self):
        """Should infer default database if no dbms.active_database setting."""
        with open(os.path.join('tests', 'resources', 'default.conf'), 
                      'r') as f:
            with warnings.catch_warnings(): 
                warnings.simplefilter("ignore")
                reader = Neo4jConfigReader(f)   
                self.assertEqual(reader.get_setting("dbms.active_database"),
                                 "graph.db",
                                 "Wrong active database")                           
                

    def test_warning_generated_if_database_not_specified(self):
        """A warning should be thrown if no dbms.active_database setting."""
        with open(os.path.join('tests', 'resources', 'default.conf'), 
                      'r') as f:
            with warnings.catch_warnings(record=True) as w:
                reader = Neo4jConfigReader(f)   
                reader.get_setting("dbms.active_database")                          
                assert len(w) == 1
                assert issubclass(w[-1].category, UserWarning)
                assert "Assumed to be default value" in str(w[-1].message)
            
    
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

class ConfigLineTestCase(unittest.TestCase):
    
    def test_error_thrown_if_status_invalid(self):
        """Should throw error is status isn't either active or commented."""
        self.assertRaises(ValueError, ConfigLine, "BAD_STATUS", "whatever",
                          "whatever")
        
