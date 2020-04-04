import json
import torch
import options
import argparse
from tqdm import tqdm
from mspan_roberta_gcn.inference_batch_gen import DropBatchGen
from mspan_roberta_gcn.mspan_roberta_gcn import NumericallyAugmentedBertNet
from mspan_roberta_gcn.drop_roberta_dataset import DropReader
from tag_mspan_robert_gcn.drop_roberta_mspan_dataset import DropReader as TDropReader
from tag_mspan_robert_gcn.inference_batch_gen import DropBatchGen as TDropBatchGen
from tag_mspan_robert_gcn.tag_mspan_roberta_gcn import NumericallyAugmentedBertNet as TNumericallyAugmentedBertNet
from pytorch_transformers import RobertaTokenizer, RobertaModel, RobertaConfig
from pytorch_transformers import AutoTokenizer, BertModel

parser = argparse.ArgumentParser("Bert inference task.")
options.add_bert_args(parser)
options.add_model_args(parser)
options.add_inference_args(parser)
parser.add_argument("--eng", type=int, required=False)

args = parser.parse_args()

args.cuda = torch.cuda.device_count() > 0


print("Build bert model.")
if args.eng == 0:
    bert_model = BertModel.from_pretrained(args.roberta_model)
else:
    bert_model = RobertaModel.from_pretrained(args.roberta_model)
print("Build Drop model.")
if args.tag_mspan:
    network = TNumericallyAugmentedBertNet(bert_model,
                                          hidden_size=bert_model.config.hidden_size,
                                          dropout_prob=0.0,
                                          use_gcn=args.use_gcn,
                                          gcn_steps=args.gcn_steps,
                                          is_eng=args.eng)
else:
    network = NumericallyAugmentedBertNet(bert_model,
                hidden_size=bert_model.config.hidden_size,
                dropout_prob=0.0,
                use_gcn=args.use_gcn,
                gcn_steps=args.gcn_steps)

if args.cuda: network.cuda()
print("Load from pre path {}.".format(args.pre_path))
network.load_state_dict(torch.load(args.pre_path))

print("Load data from {}.".format(args.inf_path))
if args.eng != 0:
    tokenizer = RobertaTokenizer.from_pretrained(args.roberta_model)
else:
    # import pdb; pdb.set_trace()
    tokenizer = AutoTokenizer.from_pretrained(args.roberta_model)
if args.tag_mspan:
    inf_iter = TDropBatchGen(args, tokenizer,
                            TDropReader(tokenizer, passage_length_limit=463, question_length_limit=46, is_eng=args.eng)
                                ._read(args.inf_path))
else:
    inf_iter = DropBatchGen(args, tokenizer, DropReader(tokenizer, passage_length_limit=463, question_length_limit=46)._read(args.inf_path))

print("Start inference...")
result = {}
network.eval()
# myf = open(args.dump_path, 'w', encoding="utf8")
# myf.close()
# myf = open(args.dump_path, 'a', encoding="utf8")
with torch.no_grad():
    for batch in tqdm(inf_iter):
        output_dict = network(**batch)
        # json.dump(output_dict, myf, ensure_ascii=False)
        # myf.write('\n')
        for i in range(len(output_dict["question_id"])):
            result[output_dict["question_id"][i]] =  output_dict["answer"][i]["predicted_answer"]
# myf.close()
with open(args.dump_path, "w", encoding="utf8") as f:
    json.dump(result, f, ensure_ascii=False)
