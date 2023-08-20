

oobabooga_api_name = "Lisa"

wake_words = ["lisa"]

device = "cuda"


#region Whisper settings

whisper_model = "medium"  #"tiny", "base", "small", "medium", "large"
non_english = False       #True - don't use the english model.
energy_threshold = 1000   #Energy level for mic to detect.
record_timeout = 5        #How real time the recording is in seconds.
phrase_timeout = 4        #How much empty space between recordings before we consider it a new line in the transcription.


#endregion

wave_file_name = "sound.wav"

