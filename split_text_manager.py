max_silero_text_length = 140


def split_text_into_chunks(text, delimiters):
    output = []
    current_sentence = ""
    for n in text:
        current_sentence += n
        if n in delimiters:
            output.append(current_sentence.strip())
            current_sentence = ""
    if len(current_sentence) > 0:
        output.append(current_sentence.strip())
    output = [n for n in output if len(n) > 0]
    return output


def split_text_array(text_array, delimiters):
    output_array = []
    for n in text_array:
        if len(n) > max_silero_text_length:
            output_array.extend(split_text_into_chunks(n, delimiters))
        else:
            output_array.append(n)
    output_array = [n for n in output_array if len(n) > 0]
    return output_array


def split_text(text):
    if len(text) < max_silero_text_length:
        return [text]

    text_array = split_text_into_chunks(text, [".", "?", "!", "\n"])
    text_array = split_text_array(text_array, [",", "-", "—", ":"])
    text_array = split_text_array(text_array, [" "])

    output_array = []

    current_text = ""
    for n in text_array:
        if len(" ".join([current_text, n])) < max_silero_text_length:
            current_text = " ".join([current_text, n])
        else:
            output_array.append(current_text)
            current_text = n

    if current_text:
        output_array.append(current_text)

    output_array = [x.strip() for x in output_array]
    return output_array
