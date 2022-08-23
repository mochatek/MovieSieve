<script>
  import { movies, processing, contentKey } from "../store.js";

  $: disabled = !!$processing;

  const getMovies = () => movies.getMovies();
  const exportData = () => movies.exportData();
  const importData = () => movies.importData();
  const saveData = () => movies.saveData();
  const toggleInfo = () => contentKey.set($contentKey === "info" ? "" : "info");
</script>

<section id="toolbar">
  <h1 id="logo">MovieSieve</h1>
  <article class="tool-group">
    <ul class="tool-group-tools">
      <li
        role="button"
        title="Browse Movies"
        class:disabled
        on:click={getMovies}
      >
        <i class="fa fa-folder-open" />
      </li>
      <li
        role="button"
        title="Import Data"
        class:disabled
        on:click={importData}
      >
        <i class="fa fa-arrow-circle-down" />
      </li>
      <li
        role="button"
        title="Export Data"
        class:disabled
        on:click={exportData}
      >
        <i class="fa fa-arrow-circle-up" />
      </li>
      <li role="button" title="Save Data" class:disabled on:click={saveData}>
        <i class="fa fa-save" />
      </li>
    </ul>
    <footer class="tool-group-name">Manage</footer>
  </article>
  <article class="tool-group">
    <nav class="tool-group-tools">
      <a target="_blank" title="GitHub" href="https://github.com/mochatek"
        ><i class="fa fa-github-square" /></a
      >
      <a
        target="_blank"
        title="LinkedIn"
        href="https://in.linkedin.com/in/akash-s-panickar"
        ><i class="fa fa-linkedin-square" /></a
      >
    </nav>
    <footer class="tool-group-name">Social</footer>
  </article>
  <article class="tool-group">
    <ul class="tool-group-tools">
      <li role="button" title="Info" on:click={toggleInfo}>
        <i class="fa fa-info-circle" title="Info" />
      </li>
    </ul>
    <footer class="tool-group-name">Help</footer>
  </article>
</section>
