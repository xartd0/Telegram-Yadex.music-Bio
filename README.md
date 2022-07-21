# Telegram-Yandex.music-Bio
Automatic change of bio telegram


## Getting Started

This script puts the name and author of the video in bio telegram, which you are currently watching on youtube or yandex.music

![изображение](https://user-images.githubusercontent.com/43171120/180196802-77b66b89-6b94-4a19-b10d-49168906a458.png)


### Installation

1. Clone the repo

   ```bash
   $ https://github.com/xartd0/Telegram-Youtube-Yandex-Bio.git
   ```
2. Before launching, replace api_id and api_hash with yours, you can get them here https://my.telegram.org/apps.

   ```bash
   $ cd Telegram-Youtube-Yandex-Bio
   $ nano core.py
   $ api_id = 'YOUR api_id'
   $ api_hash = 'YOUR api_hash'
   $ media_url = 'https://www.youtube.com/' or 'https://music.yandex.ru/'
   ```

## Usage

* Before the first launch, you will need to log in to your telegram account.

   ```bash
   $ python3 core.py
   ```
