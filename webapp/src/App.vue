<template>
  <div class="app">
    <router-view/>
  </div>
</template>

<style>

::-webkit-scrollbar{
  display: none;
}

  body {
    padding: 0;
    margin: 0;
  }

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #434343;
    height: 100vh;
    width: 100vw;
  }

  /* Card */

  .card {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    border-radius: 10px;
    width: fit-content;
    height: fit-content;
    padding: 10px;
  }

  /* Alignement */

  .align-fixed-center {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
  }

  /* Text */
  .title {
    font-size: 1.4rem; 
  }

  .subtitle {
    font-size: 1rem;
    opacity: 0.8;
  }

</style>
