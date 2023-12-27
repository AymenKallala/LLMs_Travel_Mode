import argparse

from ChatGPT.model import OpenAI_Tweet_Analyzer, verify_dataset
from ChatGPT.correction import correcter_rate
from data.load import load_for_correction


def main(args):
    dataset,groundtruth = load_for_correction(args.data_path, start=args.start, end=args.end)
    model = OpenAI_Tweet_Analyzer(
        model_name="gpt-3.5-turbo-1106",
        max_tokens=300,
        temperature=0.7,
        prompt_technique="self_verification",
    )
    output = verify_dataset(model,dataset,sleep = False)
    trust_rate =correcter_rate(output,groundtruth)

    print('-'*59)
    print(f"Correction trustworthiness: {trust_rate*100}%")
    if args.save:
        output.to_excel(f"./results/Correction_{args.technique}.xlsx")


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
        default=40,
        type=int,
        help="starting index in data file",
    )
    parser.add_argument(
        "--data_path",
        default="../data/configs/fashionpedia.yaml",
        type=str,
        help="Path for the data file 1",
    )
    parser.add_argument(
        "--technique",
        default="../data/configs/fashionpedia.yaml",
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
