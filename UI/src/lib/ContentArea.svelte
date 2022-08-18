<script>
  import MovieDetails from "./components/MovieDetails.svelte";
  import Information from "./components/Information.svelte";
  import MovieError from "./components/MovieError.svelte";
  import AddMovie from "./components/AddMovie.svelte";
  import { contentKey } from "../store";

  const componentMap = {
    info: Information,
    error: MovieError,
    details: MovieDetails,
    add: AddMovie,
  };
</script>

<aside id="contentarea">
  <svelte:component this={componentMap[$contentKey]} />
</aside>
