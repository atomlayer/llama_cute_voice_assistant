

#the name of one of your characters in oobabooga text generation web UI (Paremeters > Character tab)
oobabooga_api_name = "Lisa"

oobabooga_api_host = 'localhost:5000'
wake_words = ["lisa"]

#region additional voice commands
delete_history = "delete history" #delete all dialog history
delete_the_last_message = "delete the last message"
#endregion


#region Whisper settings
whisper_model = "medium"  #"tiny", "base", "small", "medium", "large"
energy_threshold = 0      #Energy level for mic to detect.
record_timeout = 5        #How real time the recording is in seconds.
phrase_timeout = 4        #How much empty space between recordings before we consider it a new line in the transcription.
#endregion


wave_file_name = "sound.wav"
device = "cuda"
history_file_name = "history.json"
