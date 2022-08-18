<script>
  import { movies, selectedMovie } from "../../store";

  const extractNameYear = (name) =>
    name.split("(").map((_) => _.replace(")", ""));

  let data = {};

  $: {
    (async () => {
      const movie = $movies.find((movie) => movie.name === $selectedMovie);
      if (movie.genre !== "N/A") {
        data = await movies.getMovieData($selectedMovie);
      }
    })();
  }

  $: [Title, Year] = extractNameYear(data?.name || "");
  $: Rated = data?.Rated;
  $: imdbRating = data?.imdbRating;
  $: Genre = data?.Genre;
  $: Runtime = data?.Runtime;
  $: Released = data?.Released;
  $: Country = data?.Country;
  $: Language = data?.Language;
  $: Director = data?.Director;
  $: Writer = data?.Writer;
  $: Actors = data?.Actors;
  $: Awards = data?.Awards;
  $: Plot = data?.Plot;
</script>

<header id="movie-header">
  <h3 id="details-1">
    <span id="title">{Title}</span>
    <span id="year">( {Year} )</span>
    <span id="imdb"><i class="fa fa-imdb" />{imdbRating}</span>
  </h3>
  <ul id="details-2">
    <li>{Rated}</li>
    <li>{Genre}</li>
    <li>{Runtime}</li>
    <li>{Released}</li>
    <li>{Country}</li>
    <li>{Language}</li>
  </ul>
</header>
<div id="movie-content">
  <div id="details-3">
    <img
      src="https://m.media-amazon.com/images/M/MV5BZTM2NmZlOTEtYTI5NS00N2JjLWJkNzItMmZkNDBlYmQzNDA2XkEyXkFqcGdeQXVyMTAxODYyODI@._V1_SX300.jpg"
      alt="Poster"
    />
    <table id="technical-details">
      <tbody>
        <tr>
          <th>Director</th>
          <td>{Director}</td>
        </tr>
        <tr>
          <th>Writer</th>
          <td>{Writer}</td>
        </tr>
        <tr>
          <th>Actors</th>
          <td>{Actors}</td>
        </tr>
        <tr>
          <th>Awards</th>
          <td>{Awards}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div id="summary-container">
    <p id="movie-summary">{Plot}</p>
  </div>
</div>
