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

  const searchImdbId = async () => {
    const data = await movies.searchImdbId(imdbID);
    if (data) {
      Rated = data.Rated;
      Genre = data.Genre;
      Runtime = data.Runtime;
      Released = data.Released;
      Country = data.Country;
      Language = data.Language;
      imdbRating = data.imdbRating;
      Director = data.Director;
      Writer = data.Writer;
      Actors = data.Actors;
      Awards = data.Awards;
      Poster = data.Poster;
      Plot = data.Plot;
    }
  };

  let imdbID = "";
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

  $: {
    if ($selectedMovie) {
      imdbID = "";
      Rated = "";
      Genre = "";
      Runtime = "";
      Released = "";
      Country = "";
      Language = "";
      imdbRating = "";
      Director = "";
      Writer = "";
      Actors = "";
      Awards = "";
      Poster = "";
      Plot = "";
    }
  }

  $: save_disabled = [
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
  ].some((input) => !input.trim());

  $: search_disabled = !imdbID;
</script>

<header class="info">
  <p class="alert">
    Details for this movie is unavilable. Please provide the following details :
  </p>
</header>
<form id="add-movie">
  <div class="row">
    <input type="text" placeholder="IMDb ID" bind:value={imdbID} id="imdbID" />
    <button
      class:disabled={search_disabled}
      on:click|preventDefault={searchImdbId}><i class="fa fa-search" /></button
    >
  </div>
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
    <button
      type="submit"
      class:disabled={save_disabled}
      on:click|preventDefault={addMovie}>Save</button
    >
  </div>
</form>
