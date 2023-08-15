# llama_cute_voice_assistent

Disclaimer: This is a pre-alpha version.

Motivation: Many voice assistants with artificial intelligence have an unpleasant voice. While it may be a matter of personal preference. I aim to create a more human assistant that allows you to plug in cute anime character voices and vtuber voices.
<br>
<br>
<br>
Solution diagram:

![](media/2858db90ced343578868eeafaf30ee79.png)
<br>
<br>
# How to install

*This guide may not be the most detailed. It will need to be improved.*
<br>
<br>
## Step 1 - Install oobabooga Text generation web UI

1) [https://github.com/oobabooga/text-generation-webui\#one-click-installers](https://github.com/oobabooga/text-generation-webui#one-click-installers)

2) Open the oobabooga Text Generation web UI using the **-api** parameter.

3) On the model tab: download and run your favorite AI model.

4) On the Chat settings \> Character tab: set your character name and description.
<br>
<br>

## Step 2 - Install Realtime Voice Changer

Instruction - <https://www.youtube.com/watch?v=_JXbvSTGPoo>
<br>
<br>

## Step 3 – Install the virtual microphone

1) Download and install VB-CABLE Virtual Audio Device <https://vb-audio.com/Cable/>

2) Open Realtime Voice Changer

3) Set up an audio input: Cable Output (VB-Audio Virtual Cable)

![](media/6b7f24ec79fe7fb7ab599c5ee15e1a88.png)

4) Press start button
<br>
<br>

## Step 4 - Install llama_cute_voice_assistent

1) git clone https://github.com/atomlayer/llama_cute_voice_assistent.git
2) Install the conda environment
<br>
<br>

## Step 5 - Change the settings in the settings.py file

1) Replace the wake words.
<br>
<br>

# How to use

1) Open conda console in the project folder
2) Run the command: 
```
python voice_chat.py
```
3) Say the wake word and the command for your assistant.
