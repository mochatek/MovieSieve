<script>
  import "./css/App.css";
  import "./css/font-awesome.min.css";
  import ToolBar from "./lib/ToolBar.svelte";
  import ControlsBar from "./lib/ControlsBar.svelte";
  import SideBar from "./lib/SideBar.svelte";
  import ContentArea from "./lib/ContentArea.svelte";
  import StatusBar from "./lib/StatusBar.svelte";
  import { movies, selectedMovie, contentKey } from "./store";

  let search = "";
  let filter = "All";

  $: filterOptions = [
    "All",
    ...$movies.reduce((uniqueGenres, movie) => {
      const currentGenres = movie.genre.split(",").map((genre) => genre.trim());
      currentGenres.forEach((genre) => uniqueGenres.add(genre));
      return uniqueGenres;
    }, new Set(["N/A"])),
  ];

  $: filteredMovies = (
    filter == "All"
      ? $movies
      : $movies.filter((movie) => movie.genre.includes(filter))
  ).filter((movie) => movie.name.toLowerCase().includes(search.toLowerCase()));

  $: {
    if ($selectedMovie) {
      const selected = filteredMovies.find(
        (movie) => movie.name === $selectedMovie
      );
      if (selected) {
        contentKey.set(selected.genre === "N/A" ? "add" : "details");
      } else {
        contentKey.set("");
      }
    }
  }
</script>

<header>
  <ToolBar />
  <ControlsBar
    {filterOptions}
    bind:filter
    bind:search
    disabled={!$movies.length}
  />
</header>
<main>
  <SideBar movies={filteredMovies} />
  <ContentArea />
</main>
<footer>
  <StatusBar
    total={$movies.length}
    filtered={filteredMovies.length}
    na={filteredMovies.filter((movie) => movie.genre === "N/A").length}
  />
</footer>
