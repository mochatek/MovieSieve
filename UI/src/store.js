import { derived, writable } from "svelte/store";
import { getMovies, addMovie, getMovieData } from "./services/api";

const createMovie = () => {
  const { subscribe, set, update } = writable([]);
  const dataCache = {};

  return {
    subscribe,
    getMovies: async () => {
      processing.set({ message: "Retrieving Movies...", progress: 0 });
      const movies = await getMovies();
      processing.set({ message: "Retrieving Movies...", progress: 100 });
      setTimeout(() => processing.set(null), 1000);
      set(movies);
    },
    addMovie: async (movieName, data, poster_url) => {
      processing.set({ message: "Adding Movie..." });
      const { genre } = await addMovie(movieName, data, poster_url);
      update((movies) =>
        movies.map((movie) =>
          movie.name === movieName ? { ...movie, genre } : movie
        )
      );
      processing.set(null);
    },
    getMovieData: async (movieName) => {
      if (!(movieName in dataCache)) {
        const data = await getMovieData(movieName);
        dataCache[movieName] = data;
      }
      return dataCache[movieName];
    },
  };
};

const createContentKey = () => {
  const _writableKey = writable("");
  const _readableKey = derived(
    [selectedMovie, selectedFilter, filteredMovies, _writableKey],
    ([$selectedMovie, $selectedFilter, $filteredMovies, $_writableKey]) => {
      if ($_writableKey) {
        return "info";
      }

      if ($selectedMovie) {
        const selected = $filteredMovies.find(
          (movie) => movie.name === $selectedMovie
        );
        if (selected) {
          return selected.genre === "N/A" ? "add" : "details";
        } else {
          return $selectedFilter === "N/A"
            ? $filteredMovies.length
              ? "error"
              : ""
            : "";
        }
      }
      return $selectedFilter === "N/A"
        ? $filteredMovies.length
          ? "error"
          : ""
        : "";
    }
  );

  return {
    ..._readableKey,
    set: (key) => ["info", ""].includes(key) && _writableKey.set(key),
  };
};

export const movies = createMovie();
export const selectedMovie = writable("");
export const filterOptions = derived([movies], ([$movies]) => [
  "All",
  "N/A",
  ...$movies
    .reduce((uniqueGenres, movie) => {
      const currentGenres = movie.genre.split(",").map((genre) => genre.trim());
      currentGenres.forEach(
        (genre) =>
          genre !== "N/A" &&
          !uniqueGenres.includes(genre) &&
          uniqueGenres.push(genre)
      );
      return uniqueGenres;
    }, [])
    .sort(),
]);
export const selectedFilter = writable("All");
export const search = writable("");
export const filteredMovies = derived(
  [movies, selectedFilter, search],
  ([$movies, $selectedFilter, $search]) =>
    ($selectedFilter == "All"
      ? $movies
      : $movies.filter((movie) => movie.genre.includes($selectedFilter))
    ).filter((movie) =>
      movie.name.toLowerCase().includes($search.toLowerCase())
    )
);
export const contentKey = createContentKey();
export const processing = writable(null);

// clean genres while adding movie details in backend
