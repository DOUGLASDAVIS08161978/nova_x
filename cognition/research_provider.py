#!/usr/bin/env python3
"""
===========================================================
NOVA-X Research Provider Layer v1.0
===========================================================

Multi-source research interface.

Providers:
- DuckDuckGo
- Wikipedia fallback

===========================================================
"""

import requests

from urllib.parse import quote


class DuckDuckGoProvider:


    def search(self, topic):

        url = (
            "https://api.duckduckgo.com/"
            f"?q={quote(topic)}"
            "&format=json"
            "&no_html=1"
            "&skip_disambig=1"
        )

        try:

            response = requests.get(

                url,

                timeout=10,

                headers={

                    "User-Agent":
                    "NOVA-X Research Bot/1.0"

                }

            )

            response.raise_for_status()

            data = response.json()


            summary = (

                data.get("AbstractText")

                or

                data.get("Heading")

            )


            if summary:

                return {

                    "success": True,

                    "summary": summary,

                    "source": "DuckDuckGo",

                    "url":
                    data.get("AbstractURL")

                }


        except Exception:

            pass


        return {

            "success": False,

            "source": "DuckDuckGo"

        }



class WikipediaProvider:


    def search(self, topic):

        url = (

            "https://en.wikipedia.org/api/rest_v1/page/summary/"

            + quote(topic.replace(" ", "_"))

        )


        try:

            response = requests.get(

                url,

                timeout=15,

                headers={

                    "User-Agent":
                    "NOVA-X Research Bot/1.0"

                }

            )


            response.raise_for_status()

            data = response.json()


            summary = data.get(
                "extract"
            )


            if summary:

                return {

                    "success": True,

                    "summary": summary,

                    "source": "Wikipedia",

                    "url":
                    data.get("content_urls", {})
                    .get("desktop", {})
                    .get("page")

                }


        except Exception:

            pass


        return {

            "success": False,

            "source": "Wikipedia"

        }



class ResearchProviderManager:


    def __init__(self):

        self.providers = [

            DuckDuckGoProvider(),

            WikipediaProvider()

        ]



    def search(self, topic):

        for provider in self.providers:

            result = provider.search(
                topic
            )

            if result["success"]:

                return result


        return {

            "success": False,

            "summary":
            "No research provider returned results.",

            "source":
            "none"

        }



if __name__ == "__main__":


    manager = ResearchProviderManager()


    result = manager.search(
        "Nikola Tesla"
    )


    print()

    print(
        "NOVA-X Research Provider Test"
    )

    print(
        "============================="
    )

    print()

    print(result)

