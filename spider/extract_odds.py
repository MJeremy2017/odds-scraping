import scrapy
import json
import urllib.parse


class OddsSpider(scrapy.Spider):
    name = "oddsExtractor"
    file_name = "data.txt"
    base_url = "https://live.leisu.com/"
    start_urls = [
        "https://live.leisu.com/saicheng?date=20191215",
        # "https://live.leisu.com/3in1-2689382/",
    ]

    def parse(self, response):
        xp = response.xpath
        match_indices = xp('//li[@data-status="1"]/@data-id').extract()

        for match_id in match_indices:
            match_url = urllib.parse.urljoin(self.base_url,  '3in1-' + match_id)
            print("Making request to ", match_url)
            yield scrapy.Request(match_url, callback=self.parse_odds_unified)

    def parse_odds(self, response):
        with open(self.file_name, "w") as f:
            for i, odds in enumerate(response.css("div.begin")):
                res = {}
                odds_list = odds.css("span.float-left::text").getall()
                if i % 3 == 0:
                    res["eu_index"] = {
                        "home": odds_list[0],
                        "draw": odds_list[1],
                        "away": odds_list[2]
                    }
                elif i % 3 == 1:
                    res["handicap"] = {
                        "home": odds_list[0],
                        "handicap": odds_list[1],
                        "away": odds_list[2]
                    }
                else:
                    res["scoring"] = {
                        "big": odds_list[0],
                        "draw": odds_list[1],
                        "small": odds_list[2]
                    }
                json.dump(res, f, indent=2)
                f.write("\n")

        print("Saved to file {}".format(self.file_name))
        f.close()

    def parse_odds_unified(self, response):
        for i, odds in enumerate(response.css("div.begin")):
            res = {}
            odds_list = odds.css("span.float-left::text").getall()
            if i % 3 == 0:
                res["eu_index"] = {
                    "home": odds_list[0],
                    "draw": odds_list[1],
                    "away": odds_list[2]
                }
            elif i % 3 == 1:
                res["handicap"] = {
                    "home": odds_list[0],
                    "handicap": odds_list[1],
                    "away": odds_list[2]
                }
            else:
                res["scoring"] = {
                    "big": odds_list[0],
                    "draw": odds_list[1],
                    "small": odds_list[2]
                }
            yield res