import os
import pickle
import argparse
from pytorch_transformers.tokenization_roberta import RobertaTokenizer
from pytorch_transformers import BertTokenizer
from mspan_roberta_gcn.drop_roberta_dataset import DropReader
from tag_mspan_robert_gcn.drop_roberta_mspan_dataset import DropReader as TDropReader

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
parser.add_argument("--model_path", type=str)
parser.add_argument("--output_dir", type=str)
parser.add_argument("--passage_length_limit", type=int, default=463)
parser.add_argument("--question_length_limit", type=int, default=46)
parser.add_argument("--tag_mspan", action="store_true")
parser.add_argument("--eng", type=int, default=1)

args = parser.parse_args()
if args.eng != 0:
    tokenizer = RobertaTokenizer.from_pretrained(args.model_path)
else:
    # import pdb; pdb.set_trace()
    tokenizer = BertTokenizer.from_pretrained(args.model_path)

if args.tag_mspan:
    dev_reader = TDropReader(
        tokenizer, args.passage_length_limit, args.question_length_limit,
        is_eng=args.eng
    )

    train_reader = TDropReader(
        tokenizer, args.passage_length_limit, args.question_length_limit,
        skip_when_all_empty=["passage_span", "question_span", "addition_subtraction", "counting", "multi_span"],
        is_eng=args.eng
    )

    data_format = "drop_dataset_{}.json"

    data_mode = ["train"]
    for dm in data_mode:
        dpath = os.path.join(args.input_path, data_format.format(dm))
        data = train_reader._read(dpath)
        print("Save data to {}.".format(os.path.join(args.output_dir, "tmspan_cached_roberta_{}.pkl".format(dm))))
        with open(os.path.join(args.output_dir, "tmspan_cached_roberta_{}.pkl".format(dm)), "wb") as f:
            pickle.dump(data, f)

    data_mode = ["dev"]
    for dm in data_mode:
        dpath = os.path.join(args.input_path, data_format.format(dm))
        data = dev_reader._read(dpath) if dm == "dev" else train_reader._read(dpath)
        print("Save data to {}.".format(os.path.join(args.output_dir, "tmspan_cached_roberta_{}.pkl".format(dm))))
        with open(os.path.join(args.output_dir, "tmspan_cached_roberta_{}.pkl".format(dm)), "wb") as f:
            pickle.dump(data, f)
else:
    dev_reader = DropReader(
        tokenizer, args.passage_length_limit, args.question_length_limit
    )
    train_reader = DropReader(
        tokenizer, args.passage_length_limit, args.question_length_limit,
        skip_when_all_empty=["passage_span", "question_span", "addition_subtraction", "counting", ]
    )

    data_format = "drop_dataset_{}.json"

    data_mode = ["train"]
    for dm in data_mode:
        dpath = os.path.join(args.input_path, data_format.format(dm))
        data = train_reader._read(dpath)
        print("Save data to {}.".format(os.path.join(args.output_dir, "cached_roberta_{}.pkl".format(dm))))
        with open(os.path.join(args.output_dir, "cached_roberta_{}.pkl".format(dm)), "wb") as f:
            pickle.dump(data, f)

    data_mode = ["dev"]
    for dm in data_mode:
        dpath = os.path.join(args.input_path, data_format.format(dm))
        data = dev_reader._read(dpath) if dm == "dev" else train_reader._read(dpath)
        print("Save data to {}.".format(os.path.join(args.output_dir, "cached_roberta_{}.pkl".format(dm))))
        with open(os.path.join(args.output_dir, "cached_roberta_{}.pkl".format(dm)), "wb") as f:
            pickle.dump(data, f)