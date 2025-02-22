import json

# ✅ Define the file path
file_path = r"imdb_top_1000.json"

try:
    # ✅ Load the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        movies = json.load(file)

    # ✅ Get user input
    min_rating = float(input("Enter minimum rating (0-10): "))
    max_year = int(input("Enter latest release year: "))

    # ✅ Filter romantic movies based on user preferences
    romantic_movies = [
        movie for movie in movies
        if "Romance" in movie.get("Genre", "")
        and float(movie.get("IMDB_Rating", 0)) >= min_rating
        and int(movie.get("Released_Year", 0)) <= max_year
    ]

    # ✅ Display results
    if romantic_movies:
        print("\n Recommended Movies:")
        for movie in romantic_movies[:5]:  # Show up to 5 movies
            print(f"- {movie['Series_Title']} ({movie['Released_Year']}) - {movie['IMDB_Rating']}")
    else:
        print("\n No matching romantic movies found.")

except FileNotFoundError:
    print(" JSON file not found! Check the file path.")
except json.JSONDecodeError:
    print(" Invalid JSON format!")
except ValueError:
    print(" Please enter valid numbers.")
