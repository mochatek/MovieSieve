<script>
  export let message;
  export let status;
</script>

<article class="toast">
  <div class="container">
    <div class="icon">
      {#if status == "success"}
        <i class="fa fa-check-circle" />
      {:else}
        <i class="fa fa-warning error" />
      {/if}
    </div>
    <div class="message">
      {message}
    </div>
  </div>
  <div class={status == "success" ? "timer" : "timer error"} />
</article>
