import wikipedia
from pywikihow import search_wikihow
from asktanya.clean import clean_text

from bs4 import BeautifulSoup
import requests
import wikipedia

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}


def wiki_summary_google(keyword):
    try:
        # Wikipedia
        result1 = wikipedia.summary(keyword, sentences=2)

    except:
        # Google - Oxford Dictionary
        html = requests.get(
            f'https://www.google.com/search?q=what+is+the+definition+of+"{keyword}',
            headers=headers,
        )
        soup = BeautifulSoup(html.text, "html.parser")
        try:
            result1 = soup.select_one(".LTKOO .sY7ric").text
        except:
            result1 = ""
    return result1


def how_to(question):
    max_results = 1  # default for optional argument is 10
    how_tos = search_wikihow(question, max_results)
    assert len(how_tos) == 1
    # how_tos[0].print()
    res = how_tos[0].summary
    return res


def wiki_summary(keyword):
    try:
        result = wikipedia.summary(keyword, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        # Option 1: Wikipedia Suggest
        suggest = wikipedia.suggest(keyword)
        result = wikipedia.summary(suggest)
    return result


def try_ask(soup, question):
    q = question.lower()
    try:
        answer1 = soup.select_one(".ILfuVd").text
        # print('Q: why is ___ cond? ')
        return answer1
    except:
        try:
            answer1 = soup.select_one(".IZ6rdc").text
            answer2 = soup.select_one(".NFQFxe").text.strip(answer1)
            # print('Q: ___ belongs to which ____?, exp:Google belongs to which country?')
            if answer2 != "":
                return f"{answer1} - {answer2}"
            return answer1
        except:
            try:
                answer1 = soup.select_one(".RqBzHd").text
                # print('Q: What is the most ____ NOUN? - list')
                return answer1
            except:
                try:
                    answer1 = soup.select_one(".d9FyLd").text
                    print("cond4")
                    return answer1
                except:
                    try:
                        answer1 = soup.select_one(".hgKElc").text
                        print("TRY - Q: where is? what is the most __ ?")
                        return answer1
                    except:
                        try:
                            answer1 = soup.select_one(
                                ".FLP8od"
                            ).text  # "LEsW6e DVGBBd"><div class="wDYxhc NFQFxe oHglmf xzPb7d"
                            answer2 = soup.select_one(".NFQFxe").text
                            print(
                                "TRY - Who is ___, exp: Who is the president of United States?"
                            )
                            if answer2 != "":
                                return f"{answer1} - {answer2}"
                            return answer1
                        except:
                            try:
                                # is __ better than ___?
                                answer1 = soup.select_one(".iKJnec").text
                                print("cond is __ better than ___? ")
                                return answer1
                            except:
                                try:
                                    answer1 = soup.select_one(".zCubwf").text
                                    print("TRY - Q: when is? ")
                                    return answer1
                                except:
                                    # answer1=soup.select_one('.LTKOO').text
                                    # print('TRY - Q: what is definition of? ')
                                    # return answer1

                                    if (
                                        q.split()[0] == "what"
                                        or "meaning" in q
                                        or "definition" in q
                                    ):
                                        # print("TRY - ask wiki now, so it might be shitty")
                                        # if "what is" in question.lower():
                                        # answer1 = wiki_summary(question.strip('?').upper().strip('WHAT IS'))
                                        key = " ".join(clean_text(question))
                                        # print('key',key)
                                        # search_list=[x.lower() for x in wikipedia.search(key)]
                                        # if key.lower() in search_list:
                                        answer1 = wiki_summary_google(key)
                                        # print(answer1)
                                        if answer1 != "":
                                            return answer1
                                        answer1 = f"I am sorry I don't know about the answer to the question - {question}. I will keep learning"

                                    else:
                                        answer1 = f"I am sorry I don't know about the answer to the question - {question}. I will keep learning"
    return answer1
