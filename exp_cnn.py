import json 
import sys 
import OpenAttack
import datasets
import os 
import time

import DefenseEval.victim 
import DefenseEval.attacker
import DefenseEval.defender
from DefenseEval.utils import utils



def dataset_mapping(x):
    """
    preprocess sst dataset to the format of OpenAttack
    """
    return {
        "x": x["sentence"],
        "y": 1 if x["label"] > 0.5 else 0,
    }


def main():

## 1. Load config file
    config_file = "config/config-example.json"
    with open(config_file) as f:
        config = json.load(f)

    if not os.path.exists(os.path.join("logs", config["experiment_name"])):
        os.makedirs(os.path.join(
            "logs", config["experiment_name"]
        ))

    stdout_path = os.path.join("logs", config["experiment_name"], "stdout.log")
    stderr_path = os.path.join("logs", config["experiment_name"], "stderr.log")

    # utils.Tee allow us to both print the log to the console and save it to the log files
    with utils.Tee(stdout_path, stderr_path):
        # Print config file
        utils.print_block("Config file" )
        utils.print_pretty(config)

        # the dataset used by this example is stoed in a website with an expired SSL certificate,
        # which is why we disable SSL verification in this example.
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        

        print("Start time: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))



## 2. TODO: Load dataset
        utils.print_block("Dataset")
        # load some examples of SST-2 for evaluation
        dataset_name = config["dataset"]["name"]
        dataset = datasets.load_dataset(dataset_name, split="train[:20]").map(function=dataset_mapping)
        

## 3. create victim model
        utils.print_block("Victim model")
        print("Creating victim model using class name: {}".format(config["victim"]["model"]))
        victim_model_name = config["victim"]["model"]
        # get class by name
        clsf = getattr(sys.modules["DefenseEval.victim"], victim_model_name)()
        print(clsf)

## 4. create attacker
        utils.print_block("Attacker")
        attacker_model_name = config["attacker"]["model"]
        attacker = getattr(sys.modules["DefenseEval.attacker"], attacker_model_name)()
        print(attacker)


## 5. TODO: create defender
        # utils.print_block("Defender")
        # defender_model_name = config["defender"]["model"]
        # defender = getattr(sys.modules["DefenseEval.defender"], defender_model_name)()
        # defended_clsf = defender.defend()
        # print(clsf)


## 6. Evaluate victim model under attack
        utils.print_block("Victim model under attack")
        # prepare for attacking
        attack_eval = OpenAttack.AttackEval(attacker, clsf)
        # launch attacks and print attack results 
        attack_eval.eval(dataset, visualize=True)


## 7. TODO: Evaluate defended victim model under attack
        # utils.print_block("Defended victim model under attack")
        # # prepare for attacking
        # attack_eval = OpenAttack.AttackEval(attacker, defended_clsf)
        # # launch attacks and print attack results

        print("End time: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


if __name__ == "__main__":
    main()