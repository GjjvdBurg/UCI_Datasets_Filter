# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import xlwt

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(bytes(line, 'utf-8'))
        return item


class XlsWriterPipeline(object):

    def __init__(self):
        self.filename = 'items.xls'
        self.workbook = xlwt.Workbook(encoding='latin-1')
        self.worksheet = self.workbook.add_sheet('datasets')
        self.worksheet.write(0, 0, 'Name')
        self.worksheet.write(0, 1, 'Dataset Characteristics')
        self.worksheet.write(0, 2, 'Attribute Characteristics')
        self.worksheet.write(0, 3, 'Tasks')
        self.worksheet.write(0, 4, 'Instances')
        self.worksheet.write(0, 5, 'Attributes')
        self.worksheet.write(0, 6, 'Missings')
        self.worksheet.write(0, 7, 'Area')
        self.worksheet.write(0, 8, 'Hits')
        self.worksheet.write(0, 9, 'Date')
        self.row_idx = 1
        print("Opened XlsWriter")

    def process_item(self, item, spider):
        self.worksheet.write(self.row_idx, 0, item['name'])
        self.worksheet.write(self.row_idx, 1, item['dset_characteristics'])
        self.worksheet.write(self.row_idx, 2, item['attr_characteristics'])
        self.worksheet.write(self.row_idx, 3, item['tasks'])
        self.worksheet.write(self.row_idx, 4, item['instances'])
        self.worksheet.write(self.row_idx, 5, item['attributes'])
        self.worksheet.write(self.row_idx, 6, item['missings'])
        self.worksheet.write(self.row_idx, 7, item['area'])
        self.worksheet.write(self.row_idx, 8, item['hits'])
        self.worksheet.write(self.row_idx, 9, item['date'])
        self.row_idx += 1
        return item

    def open_spider(self, spider):
        print("XLS: Opened spider")

    def close_spider(self, spider):
        self.workbook.save(self.filename)
        print("Saved workbook.")

