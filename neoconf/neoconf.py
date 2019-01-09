#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======
Neoconf
=======

Neoconf is a python library and cli for manipulating Neo4j server config files.

TODOs
-----

The objective is to be able to type the following:
    
% neo4j-helper list 
#dbms.active_database=graph.db
dbms.directories.data=/var/lib/neo4j/data
dbms.directories.plugins=/var/lib/neo4j/plugins
dbms.directories.certificates=/var/lib/neo4j/certificates
dbms.directories.logs=/var/log/neo4j
dbms.directories.lib=/usr/share/neo4j/lib
dbms.directories.run=/var/run/neo4j

    
$ neo4j-helper set --template /etc/neo4j/neo4j.conf --active-db test.db \
  --data-dir ~/home/andrew/graphs

- Add options to specify non-default neo4j config folders (consider using 
environment variavles)

- Create a backup directory in config dir called neo4j-helper-backup
- Print information explaining which files are being created/ changed
- How to check if user has write permissions?


"""
import re

class ConfigLine(object):
    
    def __init__(self, status, setting_name, setting_value):
        """Stores relevant components of the parts of a Neo4j config entry.
        
        Args:
            status (str): Either 'active' or 'commented'.
            setting_name (str): Name of config setting
            setting_value (str): Value of config setting
            
            
        """
        self.status = status
        self.setting_name = setting_name
        self.setting_value = setting_value        
        
    @property
    def status(self):
        """Whether the setting is active or commented."""
        return self._status
    
    @status.setter
    def status(self, value):
        if value not in ["active", "commented"]:
            raise ValueError("status must be either 'active' or 'commented'")
        self._status = value
        
    def __str__(self):
        prepend_str = ""
        if self.status == "commented":
            prepend_str = "# "
        return prepend_str + self.setting_name + ": " + self.setting_value        
            

class Neo4jConfigReader(object):
    
    def __init__(self, neo4j_conf_file):
        """Accesses and prints settings from given Neo4j configuration file.
        
        neo4j_conf_file (File handle): Neo4j configuration file, or open file 
            object.       
        
        """
        self.conf_file = neo4j_conf_file            

        
    def process_config_line(self, line, setting_name):
        """Parse lines in Neo4j config file matching given setting_name.
        
        Args:
            line (str): Line of text from config file.
            setting_name (str): Name of setting to look for.
            
        Returns:
            ConfigLine: Parsed config line.
            
        """
        m = re.search(r"(^|#)" + setting_name + "=(\S*)", line)
        if m:
            if m.group(1) == "#":
                return ConfigLine('commented', setting_name, m.group(2))
            else:
                return ConfigLine('active', setting_name, m.group(2))                   
    

    def get_setting(self, setting_name):
        """Get the value of the specified database setting.
    
        Args:
            neo4j_conf_file (file-like object): The neo4j configuration file.
    
        Returns:
            str: The value of the requested setting.
    
        """
        active_matches = []
        for line in self.conf_file:
            proc_line = self.process_config_line(line, setting_name)
            if proc_line:
                if proc_line.status == "active":
                    active_matches.append(proc_line)
                    if len(active_matches) > 1:
                        raise ValueError("More than one value for " + 
                                         setting_name + " given. " + 
                                         "Check config file.")
                    
        if len(active_matches) == 1:
            return active_matches[0].setting_value
        else:
            if setting_name == "dbms.active_database":
                print("WARNING: No value for dbms.active_database specified " \
                      "in config file. Assumed to be default value graph.db.")
                return "graph.db"
            else:
                raise ValueError("No setting for " + setting_name + 
                                 " found in config file.")