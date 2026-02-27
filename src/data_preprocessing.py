import os
import yaml


CLASS_MAPPING = {
    3: 0,   # no-helmet → 0
    2: 1    # helmet → 1
}

LABEL_SPLITS = ["train", "valid", "test"]


class DataPreprocessing:
    def __init__(self, dataset_root):
        self.dataset_root = dataset_root

    def filter_label_file(self, label_path):
        with open(label_path, "r") as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            parts = line.strip().split()
            old_class = int(parts[0])

            if old_class in CLASS_MAPPING:
                parts[0] = str(CLASS_MAPPING[old_class])
                new_lines.append(" ".join(parts))

        with open(label_path, "w") as f:
            f.write("\n".join(new_lines))

    def process_labels(self):
        for split in LABEL_SPLITS:
            label_dir = os.path.join(self.dataset_root, split, "labels")

            if not os.path.exists(label_dir):
                continue

            for file in os.listdir(label_dir):
                if file.endswith(".txt"):
                    self.filter_label_file(os.path.join(label_dir, file))

        print("Labels filtered successfully!")

    def update_yaml(self):
        yaml_path = os.path.join(self.dataset_root, "data.yaml")

        with open(yaml_path, "r") as f:
            data_yaml = yaml.safe_load(f)

        data_yaml["nc"] = 2
        data_yaml["names"] = ["no-helmet", "helmet"]

        with open(yaml_path, "w") as f:
            yaml.safe_dump(data_yaml, f)

        print("data.yaml updated!")