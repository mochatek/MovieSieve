import { writable } from "svelte/store";
import { getMovies, addMovie, getMovieData } from "./services/api";

const createMovie = () => {
  const { subscribe, set, update } = writable([]);
  const dataCache = {};

  return {
    subscribe,
    getMovies: async () => {
      processing.set("Retrieving Movies...");
      const movies = await getMovies();
      processing.set("");
      set(movies);
    },
    addMovie: async (movieName, data, poster_url) => {
      const { genre } = await addMovie(movieName, data, poster_url);
      update((movies) =>
        movies.map((movie) =>
          movie.name === movieName ? { ...movie, genre } : movie
        )
      );
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

export const processing = writable("");
export const movies = createMovie();
export const selectedMovie = writable("");
export const contentKey = writable("");

// clean genres while adding movie details in backend
// loading in contentarea
