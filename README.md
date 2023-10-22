# iQ-RIPPER

iQ-RIPPER is capable of downloading videos from the *iq.com* streaming service.

## Legal Warning

This application is not endorsed by or affiliated with *iQ*. This application enables you to download videos for offline viewing which may be forbidden by law in your country. The usage of this application may also cause a violation of the *Terms of Service* between you and the stream provider. This tool is not responsible for your actions; please make an informed decision before using this application.

## Prerequisites

* RE.exe (N_m3u8DL-RE) >= 2.0.0 (https://github.com/nilaoda/N_m3u8DL-RE/)
* ffmpeg >= 6.0.0 (https://www.videohelp.com/software/ffmpeg)
* MKVToolNix >= 78.0.0 (https://www.videohelp.com/software/MKVToolNix)

### Paths Configuration

By default this application uses the following paths to programs (main executables):
* `./mkvmerge.exe`
* `./ffmpeg.exe`
* `./re.exe`

### Authentication

Saves your cookies with this name "iq_cookies.txt".

### Download Video

* `-i` enter the url of the series (if available)

> **Warning**
>
> 1. The script is created by referencing two specific scripts, and direct URLs to these scripts are provided within the Python file.
> 2. It provides options for both H.264 and H.265, each of which cannot be downloaded individually. I did not include code to automatically select a specific codec, as I opted for simplicity.
> 3. Unfortunately, I cannot help if the subtitles or videos in your region are encoded.
> 4. Even with a VIP account, the script is limited to download content up to 720p. The reasons for this limitation are unclear. It could potentially be related to problems with the VF (signature) or maybe it is my limited experience with iQ or iQIYI.
> 5. If you have any solutions to get the m3u8 file in 1080p, any help would be greatly appreciated.
> 6. The script incorporates a vinetrimmer design just for fun, so it is not compatible with that script. I have no plans to create a vinetrimmer compatible version, as I'm pretty lazy and personally don't use that feature.

![image](https://i.ibb.co/TMtkBVb/image.png)
