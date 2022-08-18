<script>
  import "./css/App.css";
  import "./css/font-awesome.min.css";
  import ToolBar from "./lib/ToolBar.svelte";
  import ControlsBar from "./lib/ControlsBar.svelte";
  import SideBar from "./lib/SideBar.svelte";
  import ContentArea from "./lib/ContentArea.svelte";
  import StatusBar from "./lib/StatusBar.svelte";
</script>

<header>
  <ToolBar />
  <ControlsBar />
</header>
<main>
  <SideBar />
  <ContentArea />
</main>
<footer>
  <StatusBar />
</footer>
