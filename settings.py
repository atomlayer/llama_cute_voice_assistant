

oobabooga_api_name = "Miku"

# This is how you will address the voice assistant.
# Sometimes the recognition may not work correctly, so you can add multiple address options.
wake_words = ["miku", "miko", "mikko"]

device = "cuda"


#region Whisper settings

whisper_model = "medium"  #"tiny", "base", "small", "medium", "large"
non_english = False       #True - don't use the english model.
energy_threshold = 1000   #Energy level for mic to detect.
record_timeout = 2        #How real time the recording is in seconds.
phrase_timeout = 3        #How much empty space between recordings before we consider it a new line in the transcription.

#endregion

wave_file_name = "sound.wav"

