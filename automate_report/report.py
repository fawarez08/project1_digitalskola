from plugins.send_to_slack import send_to_slack
from plugins.transform.read_transform import run_transform
import matplotlib.pyplot as plt


def run():
    file_bytes = "output/sales_per_month.png"

    data_product = run_transform(group_by='product').sort_values('total_price', ascending=False).head(3)
    data_month = run_transform(group_by='month')

    fig, ax = plt.subplots(2)

    ax[0].bar(data_product['Product'], data_product['total_price'])
    ax[0].set_xlabel('Product')
    ax[0].set_ylabel('Total Sales (USD)')
    ax[0].set_yticklabels(data_month['total_price'])

    ax[1].bar(data_month['Order Date'].dt.month.astype(str), data_month['total_price'])
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Total Sales (USD)')
    ax[1].set_yticklabels(data_month['total_price'])

    fig.savefig(file_bytes, bbox_inches='tight')

    message = "This is the Revenue per product performance"
    channel = "#automate_report"

    send_to_slack.execute("This is the Revenue per product performance", "#automate_report", file_bytes)

if __name__ == '__main__':
    run()