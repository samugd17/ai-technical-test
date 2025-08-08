import pandas as pd
from evaluate_tickets import evaluate_tickets

INPUT_FILE = 'data/tickets.csv'
OUTPUT_FILE = 'data/tickets_evaluated.csv'


def write_results_to_csv(dataframe: pd.DataFrame, output_file: str) -> None:
    dataframe.to_csv(output_file, index=False, encoding='utf-8')
    print(f'Evaluation completed. Saved in {output_file}')


def main():
    """Main function to read tickets, evaluate them, and write results to CSV."""
    dataframe = pd.read_csv(INPUT_FILE, encoding='utf-8')
    dataframe_evaluated = evaluate_tickets(dataframe)
    write_results_to_csv(dataframe_evaluated, OUTPUT_FILE)


if __name__ == '__main__':
    main()
