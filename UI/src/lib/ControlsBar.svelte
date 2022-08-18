<script>
  import { filterOptions, selectedFilter, search, movies } from "../store";

  $: disabled = !$movies.length;
</script>

<section id="controlsbar">
  <div class="control-wrapper">
    <i class="fa fa-filter" />
    <select class="control" bind:value={$selectedFilter} {disabled}>
      {#each $filterOptions as option}
        <option value={option}>{option}</option>
      {/each}
    </select>
  </div>
  <div class="control-wrapper">
    <i class="fa fa-search" />
    <input
      type="search"
      class="control"
      placeholder="Search"
      bind:value={$search}
      {disabled}
    />
  </div>
</section>
