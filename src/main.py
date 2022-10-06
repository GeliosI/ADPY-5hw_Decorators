import csv
import re

from logger import logger, logger_with_file_path


@logger
def read_scv(file):
    with open(file) as f:
        reader = list(csv.DictReader(f))
    return reader

@logger_with_file_path('my_log.csv')
def write_csv(file, content, fieldnames):
    with open(file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(content)

@logger        
def fix_name(reader):
    for row in reader:
        full_name = row['lastname'] + ' ' + row['firstname'] + ' ' + row['surname']
        pars_name = re.search('(\w*)\s(\w*)\s(\w*)', full_name)
        row['lastname'] = pars_name.group(1)
        row['firstname'] = pars_name.group(2)
        row['surname'] = pars_name.group(3)

@logger_with_file_path('my_log.csv')
def fix_phone(reader):
    for row in reader:
        pattern = r'(\+7|8)\s?\(?(\d{3})\)?\s?-?(\d{3})-?(\d{2})-?(\d{2})\s?\(?(доб.)?\s?(\d{4})?\)?'
        repl = r'+7(\2)\3-\4-\5 \6\7'
        row['phone'] = re.sub(pattern, repl, row['phone'])

@logger
def merge_duplicate_rows(reader):
    buf_dict = {}
    for row in reader:
        fullname = row['lastname'] + row['firstname']
        if fullname in buf_dict:
            old_row = buf_dict[fullname]
            old_row['surname'] = old_row['surname'] if old_row['surname'] else row['surname']
            old_row['organization'] = old_row['organization'] if old_row['organization'] else row['organization']
            old_row['position'] = old_row['position'] if old_row['position'] else row['position']
            old_row['phone'] = old_row['phone'] if old_row['phone'] else row['phone']
            old_row['email'] = old_row['email'] if old_row['email'] else row['email']
        else:
            buf_dict[fullname] = row   
    return buf_dict.values()
    
    
def main():
    phonebook = read_scv("phonebook_raw.csv")
    fix_name(phonebook)
    fix_phone(phonebook)
    content = merge_duplicate_rows(phonebook)
    fieldnames = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    write_csv("phonebook.csv", content, fieldnames)


if __name__ == '__main__':
    main()
