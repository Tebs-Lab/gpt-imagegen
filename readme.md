# Make Detailed Images From the CLI

A simple command line tool that uses GPT and DALL-E models to perform prompt engineering.

## Installation

Practice safe installation, use a virtual environment.

MacOS, *nix:
```
git clone git@github.com:Tebs-Lab/gpt-imagegen.git
cd gpt-imagegen
python -m venv venv
source ./venv/bin/activate
pip install -r requrements.txt
```

Windows CMD:
```
git clone git@github.com:Tebs-Lab/gpt-imagegen.git
cd gpt-imagegen
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requrements.txt
```

Windows Powershell:
```
git clone git@github.com:Tebs-Lab/gpt-imagegen.git
cd gpt-imagegen
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requrements.txt
```

### OpenAI API Key Required

For this tool to run you need a valid API key saved in an environment variable as `OPENAI_API_KEY`. OpenAI's platform has a good guide here: [https://platform.openai.com/docs/quickstart/account-setup](https://platform.openai.com/docs/quickstart/account-setup)

## Usage

__NOTE THAT__: Running this tool will take credits from your OpenAI account. Using the most expensive models is ~3 cents per run, using the cheapest models is less than 1 cent per run.

### Basic Use

Once you start the tool you'll be prompted to supply a subject, setting, and style using Python's builtin `input` function. Type your desired values and hit enter after each one.

Shebang supporting OSs
```
./gpt_image.py 
Subject: A can of worms being opened
Setting: Suburban kitchen 
Style: pop art
```

Non-shebang supporting OSs
```
python gpt_image.py
Subject: A can of worms being opened
Setting: Suburban kitchen 
Style: pop art
```

Using defaults, the final generated prompt and the URL for the image will be printed to the terminal. If OpenAI rewrote the prompt (which they do often for safety, copyright, and other reasons) the rewritten prompt will be printed as well. With the above example:

```
Final prompt: 
Generate an image in a pop art style illustrating a bizarre scenario in a typical suburban kitchen. The image content should feature an old tin can labeled 'Worms' being opened on an ivory quartz countertop, under soft, pastel-colored light. The can should be rust-speckled, contrasting sharply with the clean and colorful kitchen background. Include details such as hanging coffee mugs, checkered curtains in emerald and white partially veiling the morning vista, and a vintage toaster emitting the fragrance of fresh toast. 

As the can opener breaks the can's rusted seal, represent the immediate aftermath in vibrant, garish detail; earthworms of nauseating browns and grey-pinks wriggling and spilling out, glistening grotesquely under the overhead lights. The domestic tranquility should be disturbed by this macabre sight, providing stark contrast.

Express this scene with the bold color palette, clean lines, and simplicity characteristic of pop art, as if lifted from a comic strip or a vintage advertisement, emphasizing the grotesque humor of the situation.

Prompt rewritten by OpenAI: 

 Create an image depicting a unique scenario in a customary suburban kitchen. The scene should exhibit an old, rust-speckled tin can labelled 'Worms' being opened on a pristine ivory quartz countertop, all under a soft, pastel-colored light. Surrounding elements could include hanging coffee mugs, checkered curtains in emerald and white partially hiding the morning landscape, and an antique toaster emitting the scent of fresh toast. As the can opener disrupts the rusted seal, illustrate the ensuing situation in vibrant and exaggerated detail; earthworms in deep brown and grey-pink colors wriggling and overflowing, shining hideously under the overhead lighting. The tranquil domestic setting should be juxtaposed with this grim sight, amplifying its shocking humor. Use a style that employs bright color contrasts, crisp outlines, and minimalist design reminiscent of comic strips or retro commercials to emulate the pop art aesthetic.


https://oaidalleapiprodscus.blob.core.windows.net/private/org-YEMTlSG5Y2jiuDAMT3coEENq/user-JhC9ueFeiWeyr1PhDNXKR4G3/img-sKspBqbnRBGwODHPS4Q2BmIt.png?st=2024-04-04T14%3A34%3A45Z&se=2024-04-04T16%3A34%3A45Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-03T20%3A19%3A00Z&ske=2024-04-04T20%3A19%3A00Z&sks=b&skv=2021-08-06&sig=98fU6N8DWpg8ln5e3ug2TTlYJogDMsSqOP%2BYMKJiDxM%3D
```

![](assets/can-o-worms.png)

### Get Help

```
./gpt_image -h
```

```
usage: gpt_image.py [-h]
                    [-g {gpt-4,gpt-4-turbo-preview,gpt-3.5-turbo,gpt-3.5-turbo-instruct,babbage-002,davinci-002}]
                    [-d {dall-e-3,dall-e-2}] [-z {1024x1024,1024x1792,1792x1024}]
                    [-q {standard,hd}] [-n {1,2,3,4,5,6,7,8,9,10}] [-t] [-p] [-i] [-s SAVE]
                    [-l {1,2,3,4,5}] [-f LOG_FILE]

options:
  -h, --help            show this help message and exit
  -g {gpt-4,gpt-4-turbo-preview,gpt-3.5-turbo,gpt-3.5-turbo-instruct,babbage-002,davinci-002}, --gpt {gpt-4,gpt-4-turbo-preview,gpt-3.5-turbo,gpt-3.5-turbo-instruct,babbage-002,davinci-002}
                        GPT model version string, default 'gpt-4'
  -d {dall-e-3,dall-e-2}, --dalle {dall-e-3,dall-e-2}
                        DALL-E model version string, default 'dall-e-3'
  -z {1024x1024,1024x1792,1792x1024}, --size {1024x1024,1024x1792,1792x1024}
                        DALL-E image size string, default '1024x1024'. dall-e-2 only supports
                        the default size.
  -q {standard,hd}, --quality {standard,hd}
                        DALL-E image quality string, default 'standard'
  -n {1,2,3,4,5,6,7,8,9,10}, --img_num {1,2,3,4,5,6,7,8,9,10}
                        DALL-E number of images to generate. Warning: Not supported by
                        dall-e-3.
  -t, --text            Only print the final image prompt, do not send it to DALL-E
  -p, --open            Automatically open all URL's returned by DALL-E
  -i, --interim         Print all the interim text results from GPT
  -s SAVE, --save SAVE  Save all the prompts and the generated image.
  -l {1,2,3,4,5}, --log-level {1,2,3,4,5}
                        Log level, 5: critical, 4: error, 3: warning, 2: info, 1: debug.
                        Default: 5
  -f LOG_FILE, --log-file LOG_FILE
                        A filename relative to CWD for the logs. If None logs are sent to
                        stdout. Default: None
```

### Some common/useful patterns

#### Write detailed logging information to a file .log.txt

```
./gpt_image -l 1 -f .log.txt
```

#### Save all the generated interim prompts and the image in a folder called output

```
./gpt_image -s output
```

#### Print all the interim prompts, open the image in a new browser tab

```
./gpt_image -pi 
```