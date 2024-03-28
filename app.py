from bot.bot import Bot


if __name__ == "__main__":
    try:
        b = Bot()
        ninety = b.ninety_minutes(
            "https://www.90min.com/categories/football-news")
    except KeyboardInterrupt:
        print('Interrupted by your keyboard')
    except Exception as e:
        print(e)
