import pandas as pd
import glob
import os

# Mendefinisikan home directory di laptop kita
HOME = os.path.expanduser("~")

# Untuk append semua csv, function ini tidak untuk di read di lain python file
def __append_all_files(extension, directory):
    # read semua object file di directory data
    all_filenames = [i for i in glob.glob(
        '{directory}/*.{ext}'.format(directory=directory, ext=extension))]

    # append semua file ke dalam satu dataframe
    combined_csv = pd.concat([pd.read_csv(f)
                             for f in all_filenames], ignore_index=True)

    # cleaning kolom Quantity Ordered yang bernilai tidak valid
    combined_csv.drop(
        combined_csv[combined_csv["Quantity Ordered"] == "Quantity Ordered"].index, inplace=True)

    return combined_csv

# transformasi data, group by bisa di isi dengan product atau month
def run_transform(group_by):
    data = __append_all_files(
        'csv', 'data/sales_product_data')

    # group by product and summarize by quantity * price

    data["total_price"] = data["Quantity Ordered"].astype(
        float) * data["Price Each"].astype(float)
    data["Order Date"] = pd.to_datetime(data["Order Date"])

    # drop Date yang null
    data.drop(
        data[data["Order Date"].isna()].index, inplace=True)

    if group_by.lower().strip() == 'product':
        # group by product
        data_transformed = data.groupby('Product').agg({"total_price": "sum"}).reset_index()
    elif group_by.lower().strip() == 'month':
        # group by month
        data_transformed = data.groupby(pd.Grouper(key='Order Date', freq='M')).agg({"total_price": "sum"}).reset_index()

    print(data_transformed)

    return data_transformed


if __name__ == '__main__':
    run_transform('product')