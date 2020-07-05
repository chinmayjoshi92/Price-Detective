from Configurations import *

# datetime object containing current date and time
now = datetime.now()

# Workbook is created
wb = xlwt.Workbook()

# add_sheet is used to create sheet.
sheet = wb.add_sheet('Current Price sheet')

# Applying multiple styles
style_for_part = xlwt.easyxf('font: bold 1, color blue;')
style_for_value_up = xlwt.easyxf('font: bold 1, color red;')
style_for_value_down = xlwt.easyxf('font: bold 1, color green;')

row = 0
coloum = 0

for part, part_list in component_dict.items():
    row += 1
    coloum = 0
    print("*" * 50)
    print("Main Part : " + part)
    print("*" * 50)
    sheet.write(row, coloum, part, style_for_part)
    for specific_part in part_list:
        coloum = 1
        sheet.write(row, coloum, specific_part)
        for site in search_element.keys():
            print("Searching part {0} on {1}".format(specific_part, site))
            search_query = site + " " + specific_part
            site_link = search_on_google(search_query)
            GET_return = send_get_request(site_link)
            coloum = 2
            formula = 'HYPERLINK("{0}", "{1}")'.format(site_link, site)
            # formula = '"{0} " & HYPERLINK("{1}")'.format(site, link)
            sheet.write(row, coloum, xlwt.Formula(formula))
            coloum += 1

            if isinstance(GET_return, list):
                print("Error : " + str(GET_return[1]))
                print("=" * 50)
                continue

            if GET_return.status_code != 200:
                row += 1
                print("Incorrect Status code : " + str(GET_return.status_code))
                print("=" * 50)
                continue

            section = search_element[site][0]
            section_attr = search_element[site][1]
            ret_content = GET_return.content
            current_price = find_price(ret_content, section, section_attr)

            if current_price is None:
                row += 1
                continue
            if current_price.text is None:
                row += 1
                continue

            print("Site Link : " + site_link)
            print("Price : " + str(current_price.text))
            print("=" * 50)
            coloum += 1
            row += 1

dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
wb.save("%s.xls" % dt_string)
