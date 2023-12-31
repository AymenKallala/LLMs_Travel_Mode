import argparse

from ChatGPT.model import OpenAI_Tweet_Analyzer, predict_dataset
from data.load import load


def main(args):
    dataset = load(args.data_path_1, args.data_path_2, start=args.start, end=args.end)
    model = OpenAI_Tweet_Analyzer(
        model_name="gpt-3.5-turbo-1106",
        max_tokens=300,
        temperature=0.7,
        prompt_technique=args.technique,
    )
    output = predict_dataset(model, dataset, sleep=False)
    if args.save:
        output.to_excel(f"./results/{args.start}_{args.end}_{args.technique}.xlsx")
        output.to_csv(f"./results/{args.start}_{args.end}_{args.technique}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        default=0,
        type=int,
        help="starting index in data file",
    )
    parser.add_argument(
        "--end",
        default=1000,
        type=int,
        help="starting index in data file",
    )
    parser.add_argument(
        "--data_path_1",
        default="../data/configs/fashionpedia.yaml",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--data_path_2",
        default="../data/configs/fashionpedia.yaml",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--technique",
        default="in_context",
        type=str,
        help="Prompt engineering technique",
    )
    parser.add_argument(
        "--sleep", default=False, type=bool, help="Sleeping time during inference"
    )
    parser.add_argument(
        "--save",
        default=True,
        type=bool,
        help="Save output file",
    )

    args = parser.parse_args()

    main(args)
