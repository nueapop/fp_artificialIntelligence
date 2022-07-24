from serial_mlx90640_scraping import main

if __name__ == '__main__':
    try:
        main.scraping().process()
    except:
        print("Error")
        main.scraping().process()