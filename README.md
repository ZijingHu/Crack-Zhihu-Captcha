
# Crack Zhihu Captcha

A tool to bypass captcha while scraping Zhihu.com.

## Demo

<img src="demo/demo2.png" width=70%>

## Usage

```
import pickle
from predict_captcha import predict

with open('img_dict.pkl', 'rb') as f:
    img_dict = pickle.load(f)

# Get Captcha
# img = get_captcha()

predict(img, img_dict)
```

## Detail

It is very likely that characters or numbers in the captcha overlap with each other. A solution is to reduce the influence of those overlapping parts. Notice that most of times these parts locate at the margin of a character, so here I use 2D Gaussian Distribution as the weight to increase importance of center and decrease importance of margin.

<br>

<center>
<img src="demo/demo.png" width=70%>
</center>

<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)