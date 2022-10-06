import csv
from datetime import datetime
import os.path


def logger(decor_funk):
    def funk_logger(*args, **kwargs):
        date_time = datetime.now()
        funk_name = decor_funk.__name__
        result = decor_funk(*args, **kwargs)

        if os.path.exists('log.csv'):
            with open('log.csv', 'a') as log_file:
                writer = csv.DictWriter(
                    log_file, 
                    fieldnames=['funk_call_datetime', 'funk_name', 'funk_args', 'funk_result'], 
                    extrasaction='ignore'
                    )
                writer.writerow({'funk_call_datetime': date_time, 'funk_name': funk_name, 'funk_args': f'{args} {kwargs}', 'funk_result': result})   
        else:
            with open('log.csv', 'w') as log_file:
                writer = csv.DictWriter(
                    log_file, 
                    fieldnames=['funk_call_datetime', 'funk_name', 'funk_args', 'funk_result'], 
                    extrasaction='ignore'
                    )
                writer.writeheader()
                writer.writerow({'funk_call_datetime': date_time, 'funk_name': funk_name, 'funk_args': f'{args} {kwargs}', 'funk_result': result})

        return result
    return funk_logger


def logger_with_file_path(file_path):
    def logger(decor_funk):
        def funk_logger(*args, **kwargs):
            date_time = datetime.now()
            funk_name = decor_funk.__name__
            result = decor_funk(*args, **kwargs)

            if os.path.exists(file_path):
                with open(file_path, 'a') as log_file:
                    writer = csv.DictWriter(
                        log_file, 
                        fieldnames=['funk_call_datetime', 'funk_name', 'funk_args', 'funk_result'], 
                        extrasaction='ignore'
                        )
                    writer.writerow({'funk_call_datetime': date_time, 'funk_name': funk_name, 'funk_args': f'{args} {kwargs}', 'funk_result': result})   
            else:
                with open(file_path, 'w') as log_file:
                    writer = csv.DictWriter(
                        log_file, 
                        fieldnames=['funk_call_datetime', 'funk_name', 'funk_args', 'funk_result'], 
                        extrasaction='ignore'
                        )
                    writer.writeheader()
                    writer.writerow({'funk_call_datetime': date_time, 'funk_name': funk_name, 'funk_args': f'{args} {kwargs}', 'funk_result': result})

            return result
        return funk_logger
    return logger