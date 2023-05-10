# -*- coding: utf-8 -*-
"""DeBussy_X.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jWNnj6A0EMThQQbbApizvsIL7NQWIqKN

# DeBussy X (ver. 1.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2023

***

# (GPU CHECK)
"""

#@title NVIDIA GPU check
!nvidia-smi

"""# (SETUP ENVIRONMENT)"""

#@title Install dependencies
!git clone https://github.com/asigalov61/DeBussy-X
!pip install torch
!pip install einops
!pip install torch-summary
!pip install sklearn
!pip install tqdm
!pip install matplotlib
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio

# Commented out IPython magic to ensure Python compatibility.
#@title Import modules

print('=' * 70)
print('Loading core DeBussy X modules...')

import os
import pickle
import random
import secrets
import statistics
from time import time
import tqdm

print('=' * 70)
print('Loading main DeBussy X modules...')
import torch

# %cd /content/DeBussy-X

import TMIDIX
from lwa_transformer import *

# %cd /content/
print('=' * 70)
print('Loading aux DeBussy X modeules...')

import matplotlib.pyplot as plt

from torchsummary import summary
from sklearn import metrics

from midi2audio import FluidSynth
from IPython.display import Audio, display

print('=' * 70)
print('Done!')
print('Enjoy! :)')
print('=' * 70)

"""# (LOAD MODEL)"""

# Commented out IPython magic to ensure Python compatibility.
#@title Unzip Pre-Trained DeBussy X Model
print('=' * 70)
# %cd /content/DeBussy-X/Model

print('=' * 70)
print('Unzipping pre-trained DeBussy X model...Please wait...')

!cat /content/DeBussy-X/Model/DeBussy_X_Trained_Model.zip* > /content/DeBussy-X/Model/DeBussy_X_Trained_Model.zip
print('=' * 70)

!unzip -j /content/DeBussy-X/Model/DeBussy_X_Trained_Model.zip
print('=' * 70)

print('Done! Enjoy! :)')
print('=' * 70)
# %cd /content/
print('=' * 70)

#@title Load DeBussy X Model
full_path_to_model_checkpoint = "/content/DeBussy-X/Model/DeBussy_X_Trained_Model_14012_steps_1.4825_loss.pth" #@param {type:"string"}

print('=' * 70)
print('Loading DeBussy X Pre-Trained Model...')
print('Please wait...')
print('=' * 70)
print('Instantiating model...')

SEQ_LEN = 2048

# instantiate the model

model = LocalTransformer(
    num_tokens = 644,
    dim = 1024,
    depth = 32,
    heads=12,
    ff_mult=2,
    causal = True,
    local_attn_window_size = 512,
    max_seq_len = SEQ_LEN
)

model = torch.nn.DataParallel(model)

model.cuda()
print('=' * 70)

print('Loading model checkpoint...')

model.load_state_dict(torch.load(full_path_to_model_checkpoint))
print('=' * 70)

model.eval()

print('Done!')
print('=' * 70)

# Model stats
print('Model summary...')
summary(model)

# Plot Token Embeddings
tok_emb = model.module.token_emb.weight.detach().cpu().tolist()

tok_emb1 = []

for t in tok_emb:
    tok_emb1.append([abs(statistics.median(t))])

cos_sim = metrics.pairwise_distances(
   tok_emb1, metric='euclidean'
)
plt.figure(figsize=(7, 7))
plt.imshow(cos_sim, cmap="inferno", interpolation="nearest")
im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
plt.xlabel("Position")
plt.ylabel("Position")
plt.tight_layout()
plt.plot()
plt.savefig("/content/DeBussy-X-Tokens-Embeddings-Plot.png", bbox_inches="tight")

"""# (GENERATE)"""

#@title Improv Generation

#@markdown Generation settings

number_of_tokens_tp_generate = 256 #@param {type:"slider", min:32, max:4064, step:32}
number_of_batches_to_generate = 4 #@param {type:"slider", min:1, max:16, step:1}

#@markdown Other settings

allow_model_to_stop_generation_if_needed = False #@param {type:"boolean"}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}

print('=' * 70)
print('DeBussy X Improv Model Generator')
print('=' * 70)

if allow_model_to_stop_generation_if_needed:
  min_stop_token = 643
else:
  min_stop_token = 0

outy = [643]

print('Selected Improv sequence:')
print(outy)
print('=' * 70)

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

#start_time = time()

out = model.module.generate(inp, 
                      number_of_tokens_tp_generate, 
                      temperature=temperature, 
                      return_prime=True, 
                      min_stop_token=min_stop_token, 
                      verbose=True)

out0 = out.tolist()

print('=' * 70)
print('Done!')
print('=' * 70)
#print('Generation took', time() - start_time, "seconds")
print('=' * 70)

#======================================================================

print('Rendering results...')
print('=' * 70)

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out1) != 0:
    
      song = out1
      song_f = []
      time = 0
      dur = 0
      vel = 90
      pitch = 0
      channel = 0
                      
      for ss in song:
        
        if ss >= 0 and ss < 256:

            time += ss * 8
          
        if ss >= 256 and ss < 512:

            dur = (ss-256) * 16
            
        if ss >=512 and ss < 640:
            
            pitch = (ss-512)

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'DeBussy X',  
                                                          output_file_name = '/content/DeBussy-X-Music-Composition_'+str(i), 
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)


      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/DeBussy-X-Music-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
      display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# (CUSTOM MIDI)"""

#@title Load Seed MIDI
full_path_to_custom_seed_MIDI = "" #@param {type:"string"}

f = full_path_to_custom_seed_MIDI

print('=' * 70)
print('DeBussy X Seed MIDI Loader')
print('=' * 70)
print('Loading seed MIDI...')
print('=' * 70)
print('File:', f)
print('=' * 70)

#=======================================================
# START PROCESSING

# Convering MIDI to ms score with MIDI.py module
score = TMIDIX.midi2ms_score(open(f, 'rb').read())

# INSTRUMENTS CONVERSION CYCLE
events_matrix1 = []
melody_chords_f = []
melody_chords_f1 = []

itrack = 1

while itrack < len(score):
  for event in score[itrack]:         
      if event[0] == 'note' and event[3] != 9:
          events_matrix1.append(event)
  itrack += 1

events_matrix1.sort(key=lambda x: x[1])

#=======================================================
# PRE-PROCESSING

if len(events_matrix1) > 0:

    # recalculating timings
    for e in events_matrix1:
        e[1] = int(e[1] / 8) # Max 2 seconds for start-times
        e[2] = int(e[2] / 16) # Max 4 seconds for durations

    # Sorting by pitch, then by start-time
    events_matrix1.sort(key=lambda x: x[4], reverse=True)
    events_matrix1.sort(key=lambda x: x[1])

    #=======================================================
    # FINAL PRE-PROCESSING

    melody_chords = []

    pe = events_matrix1[0]

    for e in events_matrix1:
      if e[1] >= 0 and e[2] > 0:

        # Cliping all values...
        time = max(0, min(255, e[1]-pe[1]))             
        dur = max(1, min(255, e[2]))
        cha = 0
        ptc = max(1, min(127, e[4]))

        # Writing final note 
        melody_chords.append([time, dur, ptc])


        pe = e

    if len([y for y in melody_chords if y[2] != 9]) > 12: # Filtering out tiny/bad MIDIs...

      times = [y[0] for y in melody_chords[12:]]
      avg_time = sum(times) / len(times)

      if avg_time < 96: # Filtering out bad MIDIs...

            #=======================================================
            # FINAL PROCESSING
            #=======================================================

            # 

            #=======================================================

            cho = []
            chords = []

            for m in melody_chords:
                if m[0] == 0:
                    if m not in cho:
                        cho.append(m)
                else:
                    if len(cho) > 0:
                        cho.sort(key=lambda x: x[2], reverse=True)
                        chords.append(cho)
                    cho = []
                    if m not in cho:
                        cho.append(m)

            if len(cho) > 0:
                cho.sort(key=lambda x: x[2], reverse=True)
                chords.append(cho)




            #=======================================================
            # MAIN PROCESSING CYCLE
            #=======================================================

            chords_count = 0
            melody_chords_f = []
            melody_chords_f.extend([643]) # Zero token

            for c in chords:
                if len(chords) - chords_count == 200:
                    melody_chords_f.extend([642]) # Outro Token

                if len(c) == 1:
                    melody_chords_f.extend([640]) # Note
                else:
                    melody_chords_f.extend([641]) # Chord

                time = c[0][0]
                dur = c[0][1]

                melody_chords_f.extend([time, dur+256])

                for cc in c:

                    ptc = cc[2]

                    melody_chords_f.extend([ptc+512])
                    melody_chords_f1.extend([ptc+512])

                chords_count += 1

#=======================================================

if len(melody_chords_f) != 0:
  
    song = melody_chords_f
    song_f = []
    time = 0
    dur = 0
    vel = 90
    pitch = 0
    channel = 0
                    
    for ss in song:
      
      if ss >= 0 and ss < 256:

          time += ss * 8
        
      if ss >= 256 and ss < 512:

          dur = (ss-256) * 16
          
      if ss >=512 and ss < 640:
          
          pitch = (ss-512)

          song_f.append(['note', time, dur, channel, pitch, vel ])

detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                      output_signature = 'DeBussy X',  
                                                      output_file_name = '/content/DeBussy-X-Seed-Composition',
                                                      track_name='Project Los Angeles',
                                                      list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                      number_of_ticks_per_quarter=500)
    
#=======================================================

print('=' * 70)
print('Composition stats:')
print('Composition has', len(melody_chords_f1), 'notes')
print('Composition has', len(melody_chords_f), 'tokens')
print('=' * 70)

print('Displaying resulting composition...')
print('=' * 70)

fname = '/content/DeBussy-X-Seed-Composition'

x = []
y =[]
c = []

colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

for s in song_f:
  x.append(s[1] / 1000)
  y.append(s[4])
  c.append(colors[s[3]])

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
display(Audio(str(fname + '.wav'), rate=16000))

plt.figure(figsize=(14,5))
ax=plt.axes(title=fname)
ax.set_facecolor('black')

plt.scatter(x,y, c=c)
plt.xlabel("Time")
plt.ylabel("Pitch")
plt.show()

#@title Standard/Simple Continuation

number_of_prime_tokens = 256 #@param {type:"slider", min:4, max:2048, step:4}
number_of_tokens_to_generate = 256 #@param {type:"slider", min:32, max:2048, step:32}
number_of_batches_to_generate = 4 #@param {type:"slider", min:1, max:16, step:1}
include_prime_tokens_in_generated_output = True #@param {type:"boolean"}
allow_model_to_stop_generation_if_needed = False #@param {type:"boolean"}
temperature = 0.8 #@param {type:"slider", min:0.1, max:1, step:0.1}

print('=' * 70)
print('DeBussy X Standard Model Generator')
print('=' * 70)

if allow_model_to_stop_generation_if_needed:
  min_stop_token = 643
else:
  min_stop_token = 0

outy = melody_chords_f[:number_of_prime_tokens]

inp = [outy] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

#start_time = time()

out = model.module.generate(inp, 
                      number_of_tokens_to_generate, 
                      temperature=temperature, 
                      return_prime=include_prime_tokens_in_generated_output, 
                      min_stop_token=min_stop_token, 
                      verbose=True)

out0 = out.tolist()
print('=' * 70)
print('Done!')
print('=' * 70)
#======================================================================
print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out1) != 0:
  
      song = out1
      song_f = []
      time = 0
      dur = 0
      vel = 90
      pitch = 0
      channel = 0
                      
      for ss in song:
        
        if ss >= 0 and ss < 256:

            time += ss * 8
          
        if ss >= 256 and ss < 512:

            dur = (ss-256) * 16
            
        if ss >=512 and ss < 640:
            
            pitch = (ss-512)

            song_f.append(['note', time, dur, channel, pitch, vel ])

      detailed_stats = TMIDIX.Tegridy_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'DeBussy X',  
                                                          output_file_name = '/content/DeBussy-X-Music-Composition_'+str(i), 
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=[0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 53, 19, 0, 0, 0, 0],
                                                          number_of_ticks_per_quarter=500)
      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/DeBussy-X-Music-Composition_'+str(i)

      x = []
      y =[]
      c = []

      colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'pink', 'orange', 'purple', 'gray', 'white', 'gold', 'silver']

      for s in song_f:
        x.append(s[1] / 1000)
        y.append(s[4])
        c.append(colors[s[3]])

      FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
      display(Audio(str(fname + '.wav'), rate=16000))

      plt.figure(figsize=(14,5))
      ax=plt.axes(title=fname)
      ax.set_facecolor('black')

      plt.scatter(x,y, c=c)
      plt.xlabel("Time")
      plt.ylabel("Pitch")
      plt.show()

"""# Congrats! You did it! :)"""