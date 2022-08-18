<script>
  export let total;
  export let filtered;
  export let na;

  import { processing } from "../store";

  $: status = $processing;

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
    {#if status}
      <i class="fa fa-spinner loading" /> {status}
    {:else}
      {`${formatPlural(total, "Record")} ,  ${filtered} Filtered , ${na} N/A`}
    {/if}
  </span>
  <span id="copyright">&copy; MochaTek 2021</span>
</p>
