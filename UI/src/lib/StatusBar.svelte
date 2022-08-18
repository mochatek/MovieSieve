<script>
  import { movies, filteredMovies, processing } from "../store";

  $: total = $movies.length;
  $: filtered = $filteredMovies.length;
  $: na = $filteredMovies.filter((movie) => movie.genre === "N/A").length;

  const formatPlural = (count, itemName) => {
    let result = `${count} ${itemName}`;
    if (count > 1) {
      result += "s";
    }
    return result;
  };
</script>

<p id="statusbar">
  <span id="status">
    {#if $processing}
      <i class="fa fa-spinner loading" /> {$processing}
    {:else}
      {`${formatPlural(total, "Record")} ,  ${filtered} Filtered , ${na} N/A`}
    {/if}
  </span>
  <span id="copyright">&copy; MochaTek 2021</span>
</p>
