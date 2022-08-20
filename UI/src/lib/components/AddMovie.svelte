<script>
  import { movies, selectedMovie } from "../../store";

  const addMovie = () => {
    movies.addMovie(
      $selectedMovie,
      {
        Rated,
        Genre,
        Runtime,
        Released,
        Country,
        Language,
        imdbRating,
        Director,
        Writer,
        Actors,
        Awards,
        Plot,
      },
      Poster
    );
  };

  let Rated = "";
  let Genre = "";
  let Runtime = "";
  let Released = "";
  let Country = "";
  let Language = "";
  let imdbRating = "";
  let Director = "";
  let Writer = "";
  let Actors = "";
  let Awards = "";
  let Poster = "";
  let Plot = "";

  $: disabled = [
    Rated,
    Genre,
    Runtime,
    Released,
    Country,
    Language,
    imdbRating,
    Director,
    Writer,
    Actors,
    Awards,
    Poster,
    Plot,
  ].some((input) => input.trim() == "");
</script>

<header class="info">
  <p class="alert">
    Details for this movie is unavilable. Please provide the following details :
  </p>
</header>
<form id="add-movie">
  <div class="row">
    <input type="text" readonly value={$selectedMovie} />
    <input type="text" placeholder="Certificate" bind:value={Rated} />
    <input type="text" placeholder="Genre" bind:value={Genre} />
    <input type="text" placeholder="Runtime" bind:value={Runtime} />
  </div>
  <div class="row">
    <input type="text" placeholder="Released" bind:value={Released} />
    <input type="text" placeholder="Country" bind:value={Country} />
    <input type="text" placeholder="Language" bind:value={Language} />
    <input type="text" placeholder="IMDb Rating" bind:value={imdbRating} />
  </div>
  <div class="row">
    <input type="text" placeholder="Director" bind:value={Director} />
    <input type="text" placeholder="Writer" bind:value={Writer} />
    <input type="text" placeholder="Actors" bind:value={Actors} />
    <input type="text" placeholder="Awards" bind:value={Awards} />
  </div>
  <div class="row extend">
    <input type="text" placeholder="Poster URL" bind:value={Poster} />
  </div>
  <div class="row extend">
    <textarea placeholder="Plot Summary" bind:value={Plot} />
  </div>
  <div class="row">
    <button type="submit" class:disabled on:click|preventDefault={addMovie}
      >Save</button
    >
  </div>
</form>
