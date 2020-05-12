docker run -p 8050:8050 -v ../ads-block:/etc/splash/filters scrapinghub/splash
python web.py
open http://0.0.0.0:8080
