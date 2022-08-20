import { derived, writable } from "svelte/store";

window.eel.expose(update_progress, "update_progress");
function update_progress(progress) {
  processing.update((process) => ({ ...process, progress }));
}

const createMovie = () => {
  const { subscribe, set, update } = writable([]);
  const dataCache = {};
  let movie_directory;

  const getMovies = async (newFolder = true) => {
    newFolder && (movie_directory = "");

    if (!movie_directory) {
      processing.set({ message: "Browsing Movie Directory" });
      movie_directory = await window.eel.browse_movie_directory()();
    }
    if (movie_directory) {
      processing.set({ message: "Retrieving Movies", progress: 0 });
      const movies = await window.eel.get_movies(movie_directory)();
      const tId = setTimeout(() => {
        processing.set(null);
        clearTimeout(tId);
      }, 500);
      set(movies);
    } else {
      processing.set(null);
    }
  };

  const searchImdbId = async (imdbID) => {
    processing.set({ message: `Searching movie for #IMDb: ${imdbID}` });
    const data = await window.eel.search_imdbId(imdbID)();
    processing.set(null);
    return data;
  };

  const addMovie = async (movieName, data, poster_url) => {
    processing.set({ message: "Adding Movie" });
    const { genre } = await window.eel.add_movie(movieName, data, poster_url)();
    update((movies) =>
      movies.map((movie) =>
        movie.name === movieName ? { ...movie, genre } : movie
      )
    );
    processing.set(null);
  };

  const getMovieData = async (movieName) => {
    if (!(movieName in dataCache)) {
      const data = await window.eel.get_movie_data(movieName)();
      dataCache[movieName] = data;
    }
    return dataCache[movieName];
  };

  const exportData = async () => {
    processing.set({ message: "Exporting Data" });
    const exported = await window.eel.export_data()();
    processing.set({ message: `Export ${exported ? "Successful" : "Failed"}` });
    const tId = setTimeout(() => {
      processing.set(null);
      clearTimeout(tId);
    }, 1000);
  };

  const importData = async () => {
    processing.set({ message: "Importing Data" });
    const imported = await window.eel.import_data()();
    processing.set(null);
    imported && (await getMovies(false));
  };

  return {
    subscribe,
    getMovies,
    searchImdbId,
    addMovie,
    getMovieData,
    exportData,
    importData,
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
