import argparse

from ChatGPT.correction import correcter_rate
from ChatGPT.model import OpenAI_Tweet_Analyzer, verify_dataset
from data.load import load_for_verification


def main(args):
    dataset = load_for_verification(
        args.data_path,
    )
    model = OpenAI_Tweet_Analyzer(
        model_name="gpt-3.5-turbo-1106",
        max_tokens=300,
        temperature=0.7,
        prompt_technique="self_verification",
    )
    output = verify_dataset(model, dataset, sleep=False)

    if args.save:
        output.to_excel(f"./results/Correction_{args.technique}.xlsx")
        output.to_csv(f"./results/Correction_{args.technique}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        default="../data/configs/fashionpedia.yaml",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--technique",
        default="no_technique_specified",
        type=str,
        help="Path for the data file 1",
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
