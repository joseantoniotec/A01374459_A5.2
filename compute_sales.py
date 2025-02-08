#!/usr/bin/env python3
'''
Computes sales from products and sales json files.
'''


import json
import sys
import time
from typing import Dict, List


def load_json_file(file_path: str) -> List[Dict]:
    ''' opens and reads json file '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []


def create_price_catalogue(products: List[Dict]) -> Dict[str, float]:
    ''' creates price catalogue '''
    return {product['title']: product['price'] for product in products}


def compute_cost(price_cat: Dict[str, float], sales: List[Dict]) -> float:
    ''' computes total cost '''
    total_cost = 0
    for sale in sales:
        product_name = sale.get("Product", "")
        quantity = sale.get("Quantity", 0)

        if product_name in price_cat:
            price = price_cat[product_name]
            total_cost += price * quantity
        else:
            print(f"Warning: Product '{product_name}' not found")

    return total_cost


def write_results(total_cost: float, execution_time: float):
    ''' Writes results into SalesResults.txt '''
    result = (
        f"Total cost of all sales: ${total_cost:.2f}\n"
        f"Execution time: {execution_time:.4f} seconds"
    )
    print(result)

    with open("SalesResults.txt", "w", encoding='utf-8') as file:
        file.write(result)


def main():
    ''' main function of the program '''

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    start_time = time.time()

    products = load_json_file(price_catalogue_file)
    sales = load_json_file(sales_record_file)

    if not products or not sales:
        print("Error: Unable to process files. Exiting.")
        sys.exit(1)

    price_catalogue = create_price_catalogue(products)
    total_cost = compute_cost(price_catalogue, sales)

    end_time = time.time()
    execution_time = end_time - start_time

    write_results(total_cost, execution_time)


if __name__ == "__main__":
    main()
