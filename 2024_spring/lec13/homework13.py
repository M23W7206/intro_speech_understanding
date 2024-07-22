import requests
import bs4
from gtts import gTTS
import librosa
import IPython.display

def extract_stories_from_NPR_text(text):
  
    soup = bs4.BeautifulSoup(text, 'html.parser')
    stories = []
    for div_tag in soup.find_all('div', 'story-text'):
        titletag = div_tag.find('h3', 'title')
        teasertag = div_tag.find('p', 'teaser')
        
        if titletag is not None:
            title = titletag.text.strip()
            teaser = teasertag.text.strip() if teasertag else ""
            stories.append((title, teaser))
    
    return stories

def read_nth_story(stories, n, filename):
 
    if n < 0 or n >= len(stories):
        raise IndexError("故事索引超出范围。")
    
    story = stories[n]
    text_to_read = story[0] + ". " + story[1]  # 合并标题和预告
    tts = gTTS(text=text_to_read, lang='en')
    tts.save(filename)

# 获取网页并提取故事
webpage = requests.get("https://npr.org")
stories = extract_stories_from_NPR_text(webpage.text)

# 读取第一个故事并保存为 'test.mp3'
read_nth_story(stories, 0, 'test.mp3')

# 加载音频文件并播放
x, fs = librosa.load('test.mp3')
IPython.display.Audio(data=x, rate=fs)
