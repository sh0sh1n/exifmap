import sys
import os
import webbrowser
import exifmap.exifmap as em
import creds


def help():
    print("Usage: exifmap <command> [<args>]\n")
    print("Commands:")
    print("\tdata\t Outputs space delimited table of data parsed from each file.")
    print(
        "\tmap\t Opens a web browser to display a static image of locations scraped from file."
    )
    # print("\turl\t Outputs the query URL to generate static map.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        sys.exit()

    command = str(sys.argv[1])

    opt = str(sys.argv[2]) if len(sys.argv) > 2 else None
    if command == "data":
        folder = "." if opt is None else opt
        e = em.exif(folder)
        for fn, data in e.items():
            lat = data.get("latitude")
            lon = data.get("longitude")
            print(f"{fn} {lat} {lon}")

    elif command == "map":
        api_key = (
            os.environ["GMAPS_API_KEY"]
            if "GMAPS_API_KEY" in os.environ
            else creds.get_api_key()
        )

        if api_key is None:
            raise Exception(
                "Please set 'GMAPS_API_KEY' environment variable or define"
                "the api_key() function in creds.py to return the API KEY."
            )

        url = em.map_url(em.exif(opt), api_key)
        # print(url)
        webbrowser.open(url)
    else:
        help()
