<script>
  export let movies;

  import { selectedMovie } from "../store";
</script>

<section id="sidebar">
  <ul id="folders">
    {#each movies as movie (movie.name)}
      <li
        class:error={movie.genre === "N/A"}
        class:selected={movie.name == $selectedMovie}
        on:click={() => selectedMovie.set(movie.name)}
      >
        <i class="fa fa-folder" />{movie.name}
      </li>
    {/each}
  </ul>
</section>
