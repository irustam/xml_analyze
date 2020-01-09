import os
import sys
import csv
import untangle

xml_file = os.path.join(sys.path[0], 'yml_vse-bez-perehoda.xml')
xmlobj = untangle.parse(xml_file)

result = []


def get_labels_by_vendor():
    for offer in xmlobj.yml_catalog.shop.offers.offer:
        try:
            brand = offer.vendor.cdata.replace(',', '/').replace('\n', '')
        except:
            brand = ''

        if brand == 'Россия':
            offer_data = {}
            offer_data['id'] = offer['id']
            offer_data['url'] = offer.url.cdata
            offer_data['name'] = offer.name.cdata.replace(',', '/').replace('\n', '')
            offer_data['brand'] = offer.vendor.cdata.replace(',', '/').replace('\n', '')
            offer_data['available'] = offer['available']
            offer_data['code'] = offer.param.cdata
            result.append(offer_data)


def get_labels_by_category_id():
    cat_ids = [461, 523, 682, 525, 570, 675, 676, 677, 678, 679, 680, 681,
               3697, 3699, 462, 524, 3700, 3701, 3702, 3703, 3704]
    for offer in xmlobj.yml_catalog.shop.offers.offer:
        if int(offer.categoryId.cdata) in cat_ids:
            offer_data = {}
            offer_data['id'] = offer['id']
            offer_data['url'] = offer.url.cdata
            offer_data['name'] = offer.name.cdata.replace(',', '/').replace('\n', '')
            offer_data['brand'] = offer.vendor.cdata.replace(',', '/').replace('\n', '')
            offer_data['available'] = offer['available']
            offer_data['code'] = offer.param.cdata
            result.append(offer_data)

get_labels_by_vendor()

csv_columns = ['id',
               'url',
               'name',
               'brand',
               'available',
               'code'
               ]

with open(os.path.join(sys.path[0], 'labels_list_rossiya.csv'), 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for data in result:
        writer.writerow(data)
print(1)