import pysubs2
import os
import io
from datetime import datetime


def create_subs_with_actors(filepath):
    subtitles = pysubs2.load(filepath)

    output_directory = f"{os.path.splitext(os.path.basename(filepath))[0]}_{datetime.now():%Y-%m-%d_%H-%M-%S}"
    os.makedirs(output_directory, exist_ok=True)

    actors_dialogues = {}
    actor_name = None

    def convert_to_srt_time(time_integer):
        milliseconds = time_integer % 1000
        time_integer //= 1000
        seconds = time_integer % 60
        time_integer //= 60
        minutes = time_integer % 60
        hours = time_integer // 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    for line in subtitles:
        if line.name:
            actor_name = line.name.strip()
            if actor_name not in actors_dialogues:
                actors_dialogues[actor_name] = []
        if actor_name:
            srt_start = convert_to_srt_time(line.start)
            srt_end = convert_to_srt_time(line.end)
            actors_dialogues[actor_name].append((srt_start, srt_end, line.text))

    for actor, dialogues in actors_dialogues.items():
        srt_filename = os.path.join(output_directory, f"{actor}.srt")

        with io.open(srt_filename, "w", encoding="utf-8") as srt_file:
            i = 1
            for start, end, dialogue in dialogues:
                srt_file.write(f"{i}\n")
                srt_file.write(f"{start} --> {end}\n")
                srt_file.write(dialogue + "\n\n")
                i += 1

    with io.open(os.path.join(output_directory, f"full_subtitles.srt"), "w", encoding="utf-8") as srt_file:
        srt_file.write(f"{subtitles.to_string('srt')}")
