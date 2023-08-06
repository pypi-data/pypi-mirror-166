import pandas as pd
from matplotlib_venn import venn2, venn3
from uniprotparser.betaparser import UniprotParser, UniprotSequence
from io import StringIO


class Analysis:
    def __init__(self):
        self.data = []
        self.labels = []
        pass

    def add_data(self, filename, accession_id_column="", label="", gene_name_column="Gene names", has_gene_name=False):
        if len(self.data) <3:
            if type(filename) == str or type(filename) == pd.DataFrame:
                if type(filename) == str:
                    df = pd.read_csv(filename, sep="\t")
                else:
                    df = filename
                if not has_gene_name:
                    parser = UniprotParser()
                    acc_set = set()
                    for accession in df[accession_id_column]:
                        for acc in accession.split(";"):
                            uni = UniprotSequence(acc, parse_acc=True)
                            acc_set.add(uni.accession)
                    data = []
                    for d in parser.parse(acc_set):
                        data.append(pd.read_csv(StringIO(d.text), sep="\t"))
                    if len(data) > 0:
                        if len(data) > 1:
                            data = pd.concat(data, ignore_index=True)
                        else:
                            data = data[0]
                        self.data.append(set(data["Gene Names"].unique()))
                else:
                    self.data.append(set(df[gene_name_column].unique()))
            elif type(filename) == list:
                if has_gene_name:
                    self.data.append(set(filename))
                else:
                    parser = UniprotParser()
                    acc_set = set()
                    for accession in filename:
                        for acc in accession.split(";"):
                            uni = UniprotSequence(acc, parse_acc=True)
                            acc_set.add(uni.accession)
                    data = []
                    for d in parser.parse(acc_set):
                        data.append(pd.read_csv(StringIO(d.text), sep="\t"))
                    if len(data) > 0:
                        if len(data) > 1:
                            data = pd.concat(data, ignore_index=True)
                        else:
                            data = data[0]
                        self.data.append(set(data["Gene Names"].unique()))

            if label == "":
                self.labels.append(f"Dataset #{len(self.data)}")
            else:
                self.labels.append(label)
        else:
            raise ValueError("Number of datasets can not be greater than 3.")

    def create_venn_diagram(self, ax=None):
        if 1 < len(self.data) < 4:
            if len(self.data) == 2:
                if ax is not None:
                    return venn2(self.data, set_labels=self.labels, ax=ax)
                return venn2(self.data, set_labels=self.labels)
            else:
                if ax is not None:
                    return venn3(self.data, set_labels=self.labels, ax=ax)
                return venn3(self.data, set_labels=self.labels)
        else:
            raise ValueError("Number of datasets have to be 2 or 3.")




