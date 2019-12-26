import os
import sys
import csv
import imageio
import untangle

xml_file = os.path.join(sys.path[0], 'google_merchant_bez_tp.xml')
xmlobj = untangle.parse(xml_file)

result = []
for itm in xmlobj.rss.channel.item:
    itm_data = {}
    itm_data['link'] = itm.link.cdata.split('?')[0]
    try:
        itm_data['g_brand'] = itm.g_brand.cdata
    except:
        itm_data['g_brand'] = ''
    itm_data['g_availability'] = itm.g_availability.cdata
    itm_data['category1'] = itm.g_custom_label_0.cdata
    itm_data['category2'] = itm.g_custom_label_1.cdata
    itm_data['g_image_link'] = itm.g_image_link.cdata
    itm_data['g_additional_image_link'] = []
    try:
        for img in itm.g_additional_image_link:
            itm_data['g_additional_image_link'].append(img.cdata)
    except:
        pass
    result.append(itm_data)

size_result = []
for itm in result:
    print(itm.get('g_image_link'))
    image = imageio.imread(itm.get('g_image_link'))
    first_img_size = image.shape[0] > 799 and image.shape[1] > 799
    itm['g_image_size'] = first_img_size

    itm['g_additional_image_goodsize'] = ''
    if not first_img_size:
        for add_img_itm in itm['g_additional_image_link']:
            print(add_img_itm)
            if add_img_itm[-4:] != '.gif':
                add_im = imageio.imread(add_img_itm)
                if (add_im.shape[0] > 799 and add_im.shape[1] > 799):
                    itm['g_additional_image_goodsize'] = add_img_itm
                    break
    itm.pop('g_additional_image_link')
    size_result.append(itm)
print(len(size_result))

csv_columns = ['link',
               'g_brand',
               'g_availability',
               'category1',
               'category2',
               'g_image_link',
               'g_image_size',
               'g_additional_image_goodsize'
               ]
with open('image_size_result.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for data in size_result:
        writer.writerow(data)
print(1)