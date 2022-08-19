<script>
  import { filteredMovies, selectedMovie, processing } from "../store";
</script>

<section id="sidebar">
  {#if !!$processing && $processing?.progress > -1}
    <div class="progress"><div style="width: {$processing.progress}%;" /></div>
  {:else}
    <ul id="folders">
      {#each $filteredMovies as movie (movie.name)}
        <li
          class:error={movie.genre === "N/A"}
          class:selected={movie.name == $selectedMovie}
          on:click={() => selectedMovie.set(movie.name)}
        >
          <i class="fa fa-folder" />{movie.name}
        </li>
      {/each}
    </ul>
  {/if}
</section>
