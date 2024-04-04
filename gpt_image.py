#!python

import argparse
import logging
import pathlib
import sys
from urllib.request import urlretrieve
import webbrowser

import prompts

from openai import OpenAI

def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()

    # Model type options
    parser.add_argument("-g", "--gpt", help="GPT model version string, default 'gpt-4'", type=str, default="gpt-4", choices=['gpt-4', 'gpt-4-turbo-preview', 'gpt-3.5-turbo', 'gpt-3.5-turbo-instruct', 'babbage-002', 'davinci-002'])
    parser.add_argument("-d", "--dalle", help="DALL-E model version string, default 'dall-e-3'", type=str, default="dall-e-3", choices=['dall-e-3', 'dall-e-2'])

    # Image generation parameters
    parser.add_argument("-z", "--size", help="DALL-E image size string, default '1024x1024'. dall-e-2 only supports the default size.", type=str, default='1024x1024', choices=['1024x1024', '1024x1792', '1792x1024'])
    parser.add_argument("-q", "--quality", help="DALL-E image quality string, default 'standard'", type=str, default='standard', choices=['standard', 'hd'])
    
    # Warning, n isn't well supported on the dall-e-3 api
    parser.add_argument("-n", "--img_num", help="DALL-E number of images to generate. Warning: Not supported by dall-e-3.", type=int, default=1, choices=range(1,11))

    # Output options
    parser.add_argument("-t", "--text", help="Only print the final image prompt, do not send it to DALL-E", action='store_true')
    parser.add_argument("-p", "--open", help="Automatically open all URL's returned by DALL-E", action='store_true')
    parser.add_argument("-i", "--interim", help="Print all the interim text results from GPT", action='store_true')
    parser.add_argument("-s", "--save", help="Save all the prompts and the generated image. You must specify a file path for a directory that will be created.", type=str, default=None)

    # Logging
    parser.add_argument("-l", "--log-level", help="Log level, 5: critical, 4: error, 3: warning, 2: info, 1: debug. Default: 5", type=int, choices=[1,2,3,4,5], default=5)
    parser.add_argument("-f", "--log-file",  help="A filename relative to CWD for the logs. If None logs are sent to stdout. Default: None", type=str, default=None)

    args = parser.parse_args()

    if args.log_file is None:
        logging.basicConfig(stream=sys.stdout, level=10 * args.log_level)
    else:
        logging.basicConfig(filename=args.log_file, level=10 * args.log_level)
    
    logging.info(f'Command Run As: {" ".join(sys.argv)}')

    if args.save:
        save_directory = pathlib.Path(args.save)
        save_directory.mkdir(parents=True, exist_ok=False)

    # Your API key must be saved in an env variable for this to work.
    client = OpenAI()

    image_subject = input("Subject: ")
    logger.debug("Subject stored as %s", image_subject)

    image_setting = input("Setting: ")
    logger.debug("Setting stored as %s", image_setting)
    
    image_style = input("Style: ")
    logger.debug("Style stored as %s", image_style)

    text_to_save = f'Subject: {image_subject}\nSetting: {image_setting}\nStyle: {image_style}\n\n'
    content_details = prompts.fetch_scene_details(client, args.gpt, image_subject, image_setting)

    text_to_save += f'Content Detail:\n{content_details}\n\n'
    if args.interim:
        print(f'Content details:\n{content_details}\n\n')

    ## Common Prompts
    style_details = prompts.fetch_style_detail(client, args.gpt, image_style)
    text_to_save += f'Style details:\n{style_details}\n\n'
    if args.interim:
        print(f'Style details:\n{style_details}\n')

    image_prompt = prompts.fetch_dalle_prompt(client, args.gpt, content_details, style_details)
    text_to_save += f'Final prompt:\n{image_prompt}\n\n'

    # dall-e-2 has a 1000 character max for prompt, dall-e-3 is 4000 characters
    # TODO: handle this more gracefully?
    if args.dalle == 'dall-e-2' and len(image_prompt) > 1000:
        logger.warning('Prompt was too long for dall-e-2, clipping')
        image_prompt = image_prompt[:1000]
    elif args.dalle == 'dall-e-3' and len(image_prompt) > 4000:
        logger.warning('Prompt was too long for dall-e-3, clipping')
        image_prompt = image_prompt[:4000]
    
    print(f'Final prompt: \n{image_prompt}\n')

    # Note, the manual addition of 'I NEED ...' is from OpenAI's docs to reduce prompt rewriting.
    # https://platform.openai.com/docs/guides/images/prompting
    if not args.text:
        img_response = client.images.generate(
            model=args.dalle,
            prompt=f'I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {image_prompt}',
            size=args.size,
            quality=args.quality,
            n=args.img_num
        )

        for idx, img_data in enumerate(img_response.data):
            if img_data.revised_prompt:
                rewritten_output = f'Prompt rewritten by OpenAI: \n\n {img_data.revised_prompt}\n\n'
                print(rewritten_output)
                text_to_save += rewritten_output

            print(img_data.url)
            text_to_save += f'{img_data.url} \n\n'

            if args.open:
                webbrowser.open_new_tab(img_data.url)
            
            if args.save:
                img_save_path = save_directory / f'{idx}.png' # TODO: more robust
                urlretrieve(img_data.url, img_save_path)

    if args.save:
        save_text_path = save_directory / "prompts.txt"
        with save_text_path.open("w", encoding ="utf-8") as f:
            f.write(text_to_save)



if __name__ == '__main__':
    main()