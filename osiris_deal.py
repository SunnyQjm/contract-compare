import os
import json
import csv

# 设置osiris目录的路径
osiris_dir = './osiris'

# 创建一个新的csv文件，并写入列名
with open('osiris.csv', 'w', newline='') as csvfile:
    fieldnames = ['contract_address', 'callstack', 'reentrancy', 'time_dependency', 'integer_underflow',
                  'integer_overflow', 'money_concurrency']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    # 遍历osiris目录下的所有文件
    for filename in os.listdir(osiris_dir):
        # 检查文件是否为json文件
        if filename.endswith('.json'):
            # 打开并读取json文件
            with open(os.path.join(osiris_dir, filename), 'r') as jsonfile:
                data = json.load(jsonfile)

                # 从json数据中提取所需的数据
                row = {
                    'contract_address': filename[:-5],  # 去掉.json后缀
                    'callstack': data['callstack'] is not False,
                    'reentrancy': data['reentrancy'] is not False,
                    'time_dependency': data['time_dependency'] is not False,
                    'integer_underflow': data['underflow'] is not False,
                    'integer_overflow': data['overflow'] is not False,
                    'money_concurrency': data['money_concurrency'] is not False
                }

                # 将数据写入csv文件
                writer.writerow(row)
