import torch
import json
import argparse
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, HfArgumentParser, GenerationConfig
from peft import PeftModel
from typing import Union
import gradio
import pandas as pd
import static_f
from  dynamic_user_generate import process_all_users
import random
import importlib
from config_module import (
    model_config,
    train_config,
    lora_config,
    data_config,
)

input_history = []
count = 1

if torch.cuda.is_available():
    device = torch.device('cuda:1')
else:
    device = torch.device('cpu')

class prompter(object):
    __slots__ = "template"

    def __init__(self, template):
        with open(template) as fp:
            self.template = json.load(fp)

    def generate_prompt(
            self,
            instruction: str,
            output: Union[None, str] = None,
    ) -> str:
        res = self.template["prompt_no_input"].format(
            instruction=instruction
        )
        res = ''.join(input_history) + '\n' + res
        print("-------res!!!!!------", res)
        input_history.append(f'### Demand:{instruction}')
        if output:
            res = f"{res}{output}"
        return res

    def get_response(self, output: str) -> str:
        global count
        response = output.split(self.template["response_split"])[count].strip()
        human_index = output.find("### Demand:")
        if human_index != -1:
            response = response.split("### Demand:")[0].strip()
        count += 1
        input_history.append(f'### Output:{response}')
        print("---------记录------------：", input_history)
        # list_history = '\n'.join(response)
        return response


def main():
    # 从文件夹中获取人数与国籍
    with open('people_input.txt', 'r') as file:
        # 读取第一行
        first_line = file.readline().strip()

        # 假设第一行的格式为 "number:2"，我们可以分割字符串
        number_str = first_line.split(':')[1]

        # 将提取出来的字符串转换为整数
        number = int(number_str)

        # 读取第二行
        second_line = file.readline().strip()

        # 假设第二行的格式为 "nation:'china'"，我们可以分割字符串并去除引号
        nation = second_line.split(':')[1].strip("'")

    # 获取昵称
    with open('./nikename.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        nikename = random.choice(lines).strip()  # 随机选择一行并去除两端的空白字符

    # 向输出文件里写入昵称和国籍
    nikename = '\t' + '* nikename：' + nikename
    nation = '\t' + '* nation：' + nation
    with open('person_output.txt', 'a') as file:
        file.write('1、虚拟人静动态特征如下：' + '\n')
        # 写入第一个字符串，并换行
        file.write(nikename + '\n')
        # 写入第二个字符串，并换行
        file.write(nation + '\n')


    # 创建 parser 并指定数据类
    parser = HfArgumentParser(
        (model_config, train_config, lora_config, data_config)
    )

    # 从命令行解析参数到数据类
    (
        model_args,
        train_args,
        lora_args,
        data_args,
    ) = parser.parse_args_into_dataclasses()

    args = argparse.Namespace(
        **vars(model_args), **vars(train_args), **vars(lora_args), **vars(data_args)
    )

    # 导入模型
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        load_in_8bit=False,  # 修改为True可以加快运行速度和优化显存占用，修改为False则运行效果更好
        device_map=device,
        torch_dtype=torch.float16,
    )

    # 把lora和原模型组合
    if os.path.exists(args.output_dir):
        model = PeftModel.from_pretrained(
            model,
            args.output_dir,
            torch_dtype=torch.float16,
        )

    tokenizer = AutoTokenizer.from_pretrained(
        args.tokenizer,
        # padding_side="left",
    )

    model.config.pad_token_id = tokenizer.unk_token_id = 0
    model.config.eos_token_id = tokenizer.eos_token_id = 2
    model.config.bos_token_id = tokenizer.bos_token_id = 1
    template_path = "prompt_F.json"
    # template_path = "prompt.json"
    # 模型提示文本由此输入
    Prompter = prompter(template_path)

    model_vocab_size = model.get_input_embeddings().weight.size(0)
    tokenizer_vocab_size = len(tokenizer)
    print(f"Vocab of the base model: {model_vocab_size}")
    print(f"Vocab of the tokenizer: {tokenizer_vocab_size}")

    @torch.no_grad()
    def evaluate(
            instruction,
            temperature=0.1,
            top_p=0.75,
            top_k=40,
            repetition_penalty=1.0,
            max_new_tokens=256,
            do_sample=True,
    ):
        generation_params = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            do_sample=do_sample,
        )

        print("------123-------", instruction)
        # print("-----instruction-------", instruction)
        prompt = Prompter.generate_prompt(instruction)
        # print("-----Prompt-------", prompt)
        input_tokenizer = tokenizer(prompt, return_tensors="pt")
        # print("-----input_tokenizer-------", input_tokenizer)
        input_ids = input_tokenizer["input_ids"].to(device)
        # print("-----input_ids-------", input_ids)

        # 使用cuda进行forward计算输出
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_params,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )

        s = generation_output.sequences[0]
        # 模型生成部分静态属性
        output = tokenizer.decode(s, skip_special_tokens=True)
        return Prompter.get_response(output)

    feature = evaluate('Only output a set of six characteristics of a person\'s personality, Writing tone, topics of interest, job title, place of work, and hobbies as key-value pairs.Each key is preceded by a symbol *.')
    print(f"feature:{feature}\n")
    # 提取带有 '*' 符号的行
    lines_with_asterisk = [line for line in feature.splitlines() if '*' in line]
    print(f"\nlines_with_asterisk :{lines_with_asterisk}\n")
    # 将结果组合成一个字符串
    result = "\n\t".join(lines_with_asterisk)
    s_feature = '\t* ' + static_f.generate_feature()

    # ===============动态特征生成=================
    # 读取五个静态属性进行匹配
    f_static = static_f.dynamic_characteristics
    print(f"f_static:{f_static}")
    age = f_static["Age"]
    gender = f_static['Gender']
    job_title = lines_with_asterisk[3].split(':', 1)[1].strip()
    hobbies = lines_with_asterisk[5].split(':', 1)[1].strip()
    topics_of_interest = lines_with_asterisk[2].split(':', 1)[1].strip()

    # 将五个特征转换为字典
    person_features = {
        'Age': age,
        'Gender': gender,
        'job_title': job_title,
        'hobbies': hobbies,
        'topics_of_interest': topics_of_interest
    }
    result_d_f = process_all_users(person_features)
    print(f"result_d_f:{result_d_f}")
    # 将字典转换为带有 '\t* ' 前缀的多行字符串
    formatted_output = "\n".join(f"\t* {key}: {value}" for key, value in result_d_f.items())
    # ================end=======================

    with open('person_output.txt', 'a') as file:
        file.write('\t' + result + '\n')
        file.write(s_feature + '\n')
        file.write(formatted_output + '\n')
    number -= 1

    # 生成多个人
    num = 1
    while number > 0:
        num += 1
        with open('./nikename.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            nikename = random.choice(lines).strip()  # 随机选择一行并去除两端的空白字符
        nikename = '\t' + '* nikename：' + nikename
        op1 = str(num)

        feature1 = evaluate(
            'Output another set of six characteristics of a person\'s personality, Writing tone, topics of interest, job title, place of work, and hobbies as key-value pairs.Each key is preceded by a symbol *.')
        print(feature1)
        # Each key-value pair is preceded by the symbol *
        # 提取带有 '*' 符号的行
        lines_with_asterisk = [line for line in feature1.splitlines() if '*' in line]
        # 将结果组合成一个字符串
        result1 = "\n\t".join(lines_with_asterisk)
        importlib.reload(static_f)
        s_feature = '\t* ' + static_f.generate_feature()

        # ===============动态特征生成=================
        # 读取五个静态属性进行匹配
        f_static = static_f.dynamic_characteristics
        print(f"f_static:{f_static}")
        age = f_static["Age"]
        gender = f_static['Gender']
        job_title = lines_with_asterisk[3].split(':', 1)[1].strip()
        hobbies = lines_with_asterisk[5].split(':', 1)[1].strip()
        topics_of_interest = lines_with_asterisk[2].split(':', 1)[1].strip()
        # 将五个特征转换为字典
        person_features = {
            'Age': age,
            'Gender': gender,
            'job_title': job_title,
            'hobbies': hobbies,
            'topics_of_interest': topics_of_interest
        }
        result_d_f = process_all_users(person_features)
        print(f"result_d_f:{result_d_f}")
        # 将字典转换为带有 '\t* ' 前缀的多行字符串
        formatted_output = "\n".join(f"\t* {key}: {value}" for key, value in result_d_f.items())
        # ================end=======================

        with open('person_output.txt', 'a') as file:
            file.write(op1 + '、虚拟人静动态特征如下：' + '\n')
            # 写入第一个字符串，并换行
            file.write(nikename + '\n')
            # 写入第二个字符串，并换行
            file.write(nation + '\n')
            file.write('\t' + result1 + '\n')
            file.write(s_feature + '\n')
            file.write(formatted_output + '\n')


        number -= 1

if __name__ == "__main__":
    main()