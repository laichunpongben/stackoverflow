#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
from lxml import etree
import csv

repository = r'E:\stackoverflow' #Your repository
file_names = ['Badges', 'Comments', 'Posts', 'PostLinks', 'Tags', 'Users', 'Votes']
header_dict = {
    'Badges': ('Id', 'UserId', 'Name', 'Date', 'Class', 'TagBased'),
    'Comments': ('Id', 'PostId', 'Score', 'Text', 'CreationDate', 'UserId'),
    'Posts': ('Id', 'PostTypeId', 'ParentId', 'AcceptedAnswerId', 'CreationDate', 'Score', 'ViewCount', 'Body', 'OwnerUserId', 
                'LastEditorUserId', 'LastEditorDisplayName', 'LastEditorDisplayName', 'LastEditDate', 'LastActivityDate', 'CommunityOwnedDate', 'ClosedDate', 
                'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount'),
    'PostLinks': ('Id', 'CreationDate', 'PostId', 'RelatedPostId', 'LinkTypeId'),
    'Tags': ('Id', 'TagName', 'Count', 'ExcerptPostId', 'WikiPostId'),
    'Users': ('Id', 'Reputation', 'CreationDate', 'DisplayName', 'LastAccessDate', 'WebSiteUrl', 'Location', 'Age', 'Views', 'UpVotes', 'DownVotes'),
    'Votes': ('Id', 'PostId', 'VoteTypeId', 'CreationDate')
}
convert_dict = { 
    'Badges': False, 
    'Comments': False, 
    'Posts': False, 
    'PostLinks': False, 
    'Tags': False, 
    'Users': False,
    'Votes': False
} #Set to True if convert xml to csv 

class Stackoverflow(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.xml_file = os.path.join(repository, str(self)+'.xml')
        self.csv_file = os.path.join(repository, str(self)+'.csv')
        self.header = header_dict[str(self)]
        
    def __str__(self):
        return self.file_name
        
    def make_csv(self):
        with open(self.csv_file, 'wb') as file_:
            writer = csv.writer(file_, delimiter=',')
            writer.writerow(self.header)
            
            parser = etree.iterparse(self.xml_file)
            for event, row in parser:
                if row.tag=='row':
                    row_content = (row.attrib.get(attribute, '') for attribute in self.header)
                    writer.writerow([unicode(x).encode('utf-8') for x in row_content])
                row.clear()
                while row.getprevious() is not None:
                    del row.getparent()[0]
            del parser
    
if __name__=='__main__':
    stackoverflows = [Stackoverflow(file_name) for file_name in file_names]
    for stackoverflow in stackoverflows:
        if convert_dict[str(stackoverflow)]:
            stackoverflow.make_csv()
