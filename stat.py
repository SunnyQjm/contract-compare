import os
import sys
import csv

class ResultChecker:

    @staticmethod
    def performCheck(target_dir: str) -> bool:
        dir_name = os.path.basename(target_dir)
        dir_name = dir_name.replace("-", "")
        # checker = ResultChecker.defaultCheck
        checker = getattr(ResultChecker, f"check{dir_name}")
        if checker is None:
            checker = ResultChecker.defaultCheck
        return checker(target_dir)

    @staticmethod
    def defaultCheck(target_dir: str) -> bool:
        for root2, dirs2, files2 in os.walk(target_dir):
            for file2 in files2:
                if os.path.getsize(os.path.join(root2, file2)) > 0:
                    return True
        return False

    @staticmethod
    def check1Reentrancy(target_dir: str):
        return ResultChecker.defaultCheck(target_dir)

    @staticmethod
    def check2UncheckedCall(target_dir: str):
        step3 = os.path.join(target_dir, "Step3.csv")
        return os.path.exists(step3) and os.path.getsize(step3) > 0

    @staticmethod
    def check3FailedSend(target_dir: str):
        return ResultChecker.defaultCheck(target_dir)

    @staticmethod
    def check4TimestampDependence(target_dir: str):
        return ResultChecker.defaultCheck(target_dir)

    @staticmethod
    def check5UnsecuredBalance(target_dir: str):
        step3 = os.path.join(target_dir, "Step3.csv")
        return os.path.exists(step3) and os.path.getsize(step3) > 0

    @staticmethod
    def check6MisuseOfOrigin(target_dir: str):
        result_file = os.path.join(target_dir, "MisuseOriginResult.csv")
        return os.path.exists(result_file) and os.path.getsize(result_file) > 0

    @staticmethod
    def check7Suicidal(target_dir: str):
        result_file = os.path.join(target_dir, "SuicidalResult.csv")
        return os.path.exists(result_file) and os.path.getsize(result_file) > 0

    @staticmethod
    def check8SecurifyReentrancy(target_dir: str):
        return ResultChecker.defaultCheck(target_dir)


class ResultItem:
    def __init__(self, success: bool, hash: str, targets: dict):
        self.success = success
        self.targets = targets
        self.hash = hash

    def __str__(self):
        return f"ResultItem({self.success}, {self.hash}, {self.targets})"


def stat_item(target_dir: str):
    item = ResultItem(False, os.path.basename(target_dir), {})
    facts_dit = f"{target_dir}/facts"
    if not os.path.exists(facts_dit) or len(os.listdir(facts_dit)) == 1:
        return item
    item.success = True

    # 便利dir下面的所有文件
    for root, dirs, files in os.walk(target_dir):
        for sub_dir in dirs:
            subdir = os.path.join(root, sub_dir)
            print(subdir)
            if not os.path.isdir(subdir):
                continue
            if sub_dir == "facts":
                continue
            rule = sub_dir
            result = ResultChecker.performCheck(subdir)
            item.targets[rule] = result
    return item


if __name__ == '__main__':
    results_dir = sys.argv[1]
    items = []
    # 只遍历一级目录
    for root, dirs, files in os.walk(results_dir):
        for dir in dirs:
            target_dir = os.path.join(results_dir, dir)
            if not os.path.isdir(target_dir):
                continue
            item = stat_item(target_dir)
            items.append(item)

    # output items to csv, targets is a dict, every key as a column
    columns = ["success", "hash"]
    rules = items[0].targets.keys()
    columns.extend(rules)
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for item in items:
            writer.writerow([item.success, item.hash] + [item.targets.get(rule, False) for rule in rules])
