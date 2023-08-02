import os
import numpy as np

import torch
import torch.nn as neuralnetwork
from torch.nn import functional as functional

import tiktoken
from model import GenerativePretrainedTransformer, Config

from halo import Halo



# hyperparameters #
encodeMethod = 'r50k_base'
maxNewTokens = 32 # number of tokens per sample
printConsole = False
writeToFile = True

resumeDir = os.path.join('gpt', 'resume')
outDir = os.path.join('gpt', 'output')
contextDir = os.path.join('gpt', 'context')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
###################



# model init
ckpt_path = os.path.join(resumeDir, os.listdir(resumeDir)[0])
checkpoint = torch.load(ckpt_path, map_location=device)

print(f"Loaded model from {ckpt_path}")

config = Config(**checkpoint['modelArgs'])
model = GenerativePretrainedTransformer(config)

model.load_state_dict(checkpoint['model'])

model.to(device)

print('Model has', sum(p.numel() for p in model.parameters()), 'parameters')


# sampling
def sample():
    samplingLoading = Halo(text='Sampling: ', spinner='line', color='white', placement='right')
    samplingLoading.start()

    encoding = tiktoken.get_encoding(encodeMethod)

    contextFile = os.path.join(contextDir, os.listdir(contextDir)[0])

    with open(contextFile, 'r', encoding='utf-8') as file:
        contextString = file.read()

    contextIds = encoding.encode(contextString, allowed_special={'<|endoftext|>'})
    contextIds = contextIds[-96:]

    contextInput = (torch.tensor(contextIds, dtype=torch.long, device=device)[None, ...])


    with torch.no_grad():

        y = encoding.decode(model.generate(contextInput, maxNewTokens)[0].tolist()[-32:])

        if printConsole:
            print(f'\n{y}')
        
        if writeToFile:
            newFile = os.path.join(outDir, 'sample.txt')

            open(newFile, 'w', encoding="utf-8").write(y)


    samplingLoading.stop()