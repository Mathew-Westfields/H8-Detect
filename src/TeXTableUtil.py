import pandas as pd
import numpy as np

def report_to_df(report:str):
    arr = report.split()
    class2name = {0:"hateful",1:"offensive",2:"neither"}
    cls_cols = ["class"] + arr[0:4] # split of column names and add column name class
    avg_cols = ["metric"]  + arr[0:4]
    num_of_classes = 3
    num_of_col = 5

    cls_rows = arr[4:4+num_of_classes*(num_of_col)]
    avg_rows = arr[4+num_of_classes*(num_of_col):]

    def handle_classifer_row(cls_rows): # this changes with the number of classes
        cls_rows = [float(el)  for el in cls_rows]
        cls_rows = [cls_rows[num_of_col*i:num_of_col*(i+1)] for i in range(num_of_classes)] #basicly index stuff
        cls_data = []
        for i in range(num_of_classes): # change class_id to to class_name via class2name for every class
            cls = cls_rows[i][0]
            name = class2name[cls]
            cls_rows[i][0] = name
            cls_data.append(cls_rows[i])
        return cls_data

    def handle_average_rows(avg_rows): # this can be completely hardcoded since this never changes with size!
        acc_row = avg_rows[0:3]
        acc_name = acc_row[0] # this row is different than the other two since it contains more whitespace
        acc_row = acc_row[1:]
        acc_row = [float(el) for el in acc_row]
        acc_row = [acc_name] + [np.nan,np.nan] + acc_row # fixing acc_row so it looks like every other row

        macro_row = avg_rows[3:9]
        macro_name = macro_row[0] # whitespace in "macro avg" creates two elements
        macro_row = macro_row[2:]
        macro_row = [float(el) for el in macro_row]
        macro_row = [macro_name] + macro_row #put everything together so numbers are floats and name is at index 0

        weighted_row = avg_rows[9:]
        weighted_name = weighted_row[0]
        weighted_row = weighted_row[2:]
        weighted_row = [float(el) for el in weighted_row]
        weighted_row = [weighted_name] + weighted_row

        avg_data = [acc_row,macro_row,weighted_row]
        return avg_data

    cls_data = handle_classifer_row(cls_rows)
    avg_data = handle_average_rows(avg_rows)
    cls_df = pd.DataFrame(data = cls_data , columns = cls_cols).set_index("class")
    avg_df = pd.DataFrame(data = avg_data , columns = avg_cols).set_index("metric")
    return cls_df,avg_df

def report_to_LaTeX(report,table_name:str,mode=None):
    cls_df,avg_df = report_to_df(report)
    begin_str = "\\resizebox{\\linewidth}{!}{\n\\begin{tabular}{c| c c c c}\n"
    end_str = "\\end{tabular}}\n"

    def build_TeX(df,index_str):
        cols  = list(df.columns)
        out_str= index_str

        for el in cols:
            out_str = out_str + " & " + str(el)
        out_str = out_str + " \\\\" + "\n" + "\\hline" + "\n"

        for row in df.iterrows():
            class_name = row[0]
            row_str = class_name
            data = list(row[1])
            for el in data:
                row_str = row_str + " & " + str(el)
            row_str = row_str + " \\\\" + "\n"
            out_str = out_str + row_str
        return begin_str + out_str + end_str
     
    cls_TeX = build_TeX(cls_df,"class")
    avg_TeX = build_TeX(avg_df,"metric")
    if mode == "save":
        with open("../report/tables-figures/"+table_name+".txt","w") as output_file:
            output_file.write(cls_TeX + "\n" + avg_TeX)
    else:
        return cls_TeX,avg_TeX

if __name__ == "__main__":
    print("in main:")
