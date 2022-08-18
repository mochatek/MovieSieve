const movies = [
  {
    name: "Memento (2000)",
    imdbRating: "8.5",
    Genre: "Thriller, Psychology",
    Rated: "R",
    Runtime: "126 min",
    Released: "21 August 2000",
    Country: "USA",
    Language: "English",
    Director: "Mocha",
    Writer: "Wacha",
    Actors: "Nandu, Anto, Vasco",
    Awards: "Golden Globe (Best Cinematography), Oscar (Best Picture)",
    Plot: "A funny good movie",
  },
  {
    name: "Apocalypto (2002)",
    imdbRating: "8.5",
    Genre: "Thriller",
    Rated: "R",
    Runtime: "126 min",
    Released: "21 August 2000",
    Country: "USA",
    Language: "English",
    Director: "Mocha",
    Writer: "Wacha",
    Actors: "Nandu, Anto, Vasco",
    Awards: "Golden Globe (Best Cinematography), Oscar (Best Picture)",
    Plot: "A funny good movie",
  },
  { name: "Prey (2000)", Genre: "N/A" },
  {
    name: "Titanic (2008)",
    imdbRating: "8.5",
    Genre: "Fantasy, Drama",
    Rated: "R",
    Runtime: "126 min",
    Released: "21 August 2000",
    Country: "USA",
    Language: "English",
    Director: "Mocha",
    Writer: "Wacha",
    Actors: "Nandu, Anto, Vasco",
    Awards: "Golden Globe (Best Cinematography), Oscar (Best Picture)",
    Plot: "A funny good movie",
  },
];

export const getMovies = () => {
  return new Promise((resolve) => {
    setTimeout(
      () => resolve(movies.map((_) => ({ name: _.name, genre: _.Genre }))),
      3000
    );
  });
};

export const addMovie = async (movieName, data, poster_url) => {
  const index = movies.findIndex((movie) => movie.name === movieName);
  movies[index] = {
    name: movieName,
    imdbRating: "8.5",
    Genre: "Thriller, War",
    Rated: "R",
    Runtime: "126 min",
    Released: "21 August 2000",
    Country: "USA",
    Language: "English",
    Director: "Mocha",
    Writer: "Wacha",
    Actors: "Nandu, Anto, Vasco",
    Awards: "Golden Globe (Best Cinematography), Oscar (Best Picture)",
    Plot: "A funny good movie",
  };
  return { name: movieName, genre: movies[index].Genre };
};

export const getMovieData = async (movieName) => {
  return movies.find((_) => _.name === movieName);
};
