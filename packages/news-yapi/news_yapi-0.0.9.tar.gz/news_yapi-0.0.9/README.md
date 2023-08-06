# news_yapi
this is a news feed provider of [newsapi](https://newsapi.org) for [uninews](https://pypi.org/project/uninews)

## Dependency
```
pip install newsapi-python
```

## Installation
```
pip install news_api
```

## register a app_key

go to [newsapi](https://newsapi.org) to bay a plan

## Usage

```
from news_api import set_app_info
from uninews import NewsFeed

set_app_info(YOUR_APP_KEY)
nf = NewsFeed('news_api')
nf.news()
nf.headline()
nf.topstory()
```


