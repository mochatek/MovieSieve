<script>
  import { movies, selectedMovie } from "../../store";

  const addMovie = () => {
    movies.addMovie($selectedMovie);
  };
</script>

<header class="info">
  <p class="alert">
    Details for this movie is unavilable. Please provide the following details :
  </p>
</header>
<form id="add-movie">
  <div class="row">
    <input type="text" placeholder="Name" readonly value={$selectedMovie} />
    <input type="text" placeholder="Certificate" />
    <input type="text" placeholder="Genre" />
    <input type="text" placeholder="Runtime" />
  </div>
  <div class="row">
    <input type="text" placeholder="Release" />
    <input type="text" placeholder="Country" />
    <input type="text" placeholder="Language" />
    <input type="text" placeholder="IMDb Rating" />
  </div>
  <div class="row">
    <input type="text" placeholder="Director" />
    <input type="text" placeholder="Writer" />
    <input type="text" placeholder="Actors" />
    <input type="text" placeholder="Awards" />
  </div>
  <div class="row extend">
    <input type="text" placeholder="Poster URL" />
  </div>
  <div class="row extend">
    <textarea placeholder="Plot Summary" />
  </div>
  <div class="row">
    <button type="submit" on:click|preventDefault={addMovie}>Save</button>
  </div>
</form>
