
# Crack Zhihu Captcha

A tool to bypass captcha while scraping Zhihu.com.

## Demo

<img src="demo/demo2.png" width=50%>

## Usage

```
from predict_captcha import predict

predict(img)
```

## Detail

This project uses travelsal to calculate the difference between each character in our [dictionary](/dictionary) and every sub block in the picture of captcha, and concludes in characters with top four smallest difference as our final answer.

<br>

<center>
<img src="demo/anime.gif" width=30%>
</center>

<br>

It is very likely that characters or numbers in the captcha overlap with each other. A solution is to reduce the influence of those overlapping parts. Notice that most of times these parts locate at the margin of a character, so here I use 2D Gaussian Distribution as the weight to increase importance of center and decrease importance of margin.

<br>

<center>
<img src="demo/demo.png" width=70%>
</center>

<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)